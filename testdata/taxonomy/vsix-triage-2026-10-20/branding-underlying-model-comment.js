"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.activate = activate;
exports.deactivate = deactivate;
const path = __importStar(require("path"));
const fs = __importStar(require("fs"));
const os = __importStar(require("os"));
const child_process_1 = require("child_process");
const fs_1 = require("fs");
const vscode = __importStar(require("vscode"));
const util_1 = require("util");
const agent_core_1 = require("@burtson-labs/agent-core");
const agent_adapters_vscode_1 = require("@burtson-labs/agent-adapters-vscode");
const host_kit_1 = require("@burtson-labs/host-kit");
const stealth_core_runtime_1 = require("@burtson-labs/stealth-core-runtime");
const agentRuntime_1 = require("./agent/agentRuntime");
const nodeToolContext_1 = require("./agent/nodeToolContext");
const promptPipeline_1 = require("./agent/promptPipeline");
const conversationService_1 = require("./services/conversationService");
const environmentService_1 = require("./agent/environmentService");
const pythonEnvironment_1 = require("./agent/pythonEnvironment");
const feedbackService_1 = require("./agent/feedbackService");
const diffContentProvider_1 = require("./diffContentProvider");
const API_KEY_SECRET_KEY = 'banditStealth.apiKey';
// Ollama auth token stored in VS Code's encrypted secret store. When
// set, the provider layer auto-injects it as `Authorization: Bearer
// <value>` on every Ollama request (including /api/tags for model
// discovery), unless `banditStealth.ollamaHeaders.Authorization` is
// already explicitly set — an explicit header in settings always wins
// so power users can mix schemes.
const OLLAMA_AUTH_SECRET_KEY = 'banditStealth.ollamaAuthToken';
const CONVERSATION_STORAGE_KEY = 'banditStealth.conversation';
const CONVERSATION_HISTORY_STORAGE_KEY = 'banditStealth.conversationHistory';
const MODE_STORAGE_KEY = 'banditStealth.mode';
const INTENT_MEMORY_STORAGE_KEY = 'banditStealth.intentHistory';
class BanditStealthViewProvider {
    // ── Delegation properties for ConversationService ───────────────────────────
    // These bridge existing call sites to the extracted service without changing
    // every reference. They'll be removed when the full migration is complete.
    get conversationHistory() { return this.conversations['history']; }
    get currentConversationId() { return this.conversations.currentId; }
    set currentConversationId(v) { this.conversations['_currentId'] = v; }
    get conversation() { return this.conversations.messages; }
    set conversation(v) { }
    get historyVisible() { return this.conversations.historyVisible; }
    set historyVisible(v) { this.conversations.historyVisible = v; }
    get activePlan() { return this.conversations.activePlan; }
    set activePlan(v) { }
    get planStates() { return this.conversations.planStates; }
    get activePlanRunId() { return this.conversations.activePlanRunId; }
    set activePlanRunId(v) { this.conversations.activePlanRunId = v; }
    constructor(context, agentRuntime, promptPipeline, diffContentProvider) {
        this.context = context;
        this.agentRuntime = agentRuntime;
        this.promptPipeline = promptPipeline;
        this.diffContentProvider = diffContentProvider;
        this.isBusy = false;
        this.pendingOpenSettings = false;
        this.statusText = 'Ready';
        this.ollamaStatus = 'unknown';
        /** Per-session "always allow for this session" permission grants. */
        this.permissionStore = new host_kit_1.SessionPermissionStore();
        /** Outstanding permission prompts awaiting a click from the webview card.
         * Keyed by request id so multiple concurrent prompts (rare but possible
         * with parallel tool calls) don't collide. */
        this.pendingPermissions = new Map();
        this.intentMemory = [];
        this.pendingDiffPreviews = [];
        this.diffPreviewSessions = new Map();
        this.agentActivityQueue = Promise.resolve();
        this.syncScheduled = false;
        this.accountProfile = null;
        this.accountProfileStatus = 'idle';
        this.accountProfileError = null;
        this.undoSnapshotsAvailable = false;
        /** Fires whenever the provider's busy/status state changes. */
        this._onDidChangeStatus = new vscode.EventEmitter();
        this.onDidChangeStatus = this._onDidChangeStatus.event;
        /**
         * Upgrade a conversation's auto-derived name (first N chars of the
         * first user message) to a short, semantic summary the user is more
         * likely to remember. Runs ONCE per conversation, in the background,
         * after the first assistant response has been persisted. Silent
         * failures — if the LLM call errors or times out, we just keep the
         * original first-message name.
         */
        this.conversationNameUpgradeAttempted = new Set();
        this.undoManager = this.agentRuntime.getUndoManager();
        const storedMode = context.workspaceState.get(MODE_STORAGE_KEY, 'ask');
        this.activeMode = storedMode === 'agent' ? 'agent' : 'ask';
        // ConversationService handles all state loading, normalization, and persistence.
        this.conversations = new conversationService_1.ConversationService({
            storage: context.workspaceState,
            historyStorageKey: CONVERSATION_HISTORY_STORAGE_KEY,
            legacyStorageKey: CONVERSATION_STORAGE_KEY
        });
        const storedIntentMemory = context.workspaceState.get(INTENT_MEMORY_STORAGE_KEY) ?? [];
        this.intentMemory = this.normalizeIntentMemory(storedIntentMemory);
        this.undoSnapshotsAvailable = this.undoManager.hasSnapshots();
        const snapshotSubscription = this.undoManager.onDidUpdateSnapshots((count) => {
            const nextAvailable = count > 0;
            if (nextAvailable === this.undoSnapshotsAvailable) {
                return;
            }
            this.undoSnapshotsAvailable = nextAvailable;
            void this.syncState();
        });
        context.subscriptions.push(snapshotSubscription);
        this.agentEnvironmentSubscription = environmentService_1.environmentService.subscribe((message) => {
            this.handleAgentEnvironmentMessage(message);
        });
        context.subscriptions.push(this.agentEnvironmentSubscription);
        void this.loadWorkspaceFileIndex().catch(() => {
            // Ignore index warmup failures; we'll retry lazily when needed.
        });
        void this.refreshAccountProfile();
    }
    async reveal(presetPrompt) {
        this.pendingPrompt = presetPrompt ?? this.pendingPrompt;
        await vscode.commands.executeCommand('banditStealth.chat.focus');
        if (this.view) {
            this.view.show?.(true);
            await this.syncState();
        }
    }
    async promptForApiKey() {
        const secret = await vscode.window.showInputBox({
            prompt: 'Enter your Bandit AI key',
            placeHolder: 'bai_...',
            ignoreFocusOut: true,
            password: true
        });
        if (!secret) {
            return;
        }
        await this.context.secrets.store(API_KEY_SECRET_KEY, secret.trim());
        await this.syncState();
        // silent — the settings surface flips to "key set".
        void this.refreshAccountProfile();
    }
    async clearApiKey() {
        this.cancelActiveStream();
        await this.context.secrets.delete(API_KEY_SECRET_KEY);
        await this.syncState();
        // silent success — key-removed confirmation was a reliable noise source.
        void this.refreshAccountProfile();
    }
    async setOllamaAuthToken(rawValue) {
        // Prompt when called without a value (from the Command Palette). The
        // inline settings panel passes the value directly via postMessage.
        const value = typeof rawValue === 'string'
            ? rawValue
            : await vscode.window.showInputBox({
                title: 'Ollama Auth Token',
                prompt: 'Bearer token or proxy credential for your custom Ollama endpoint. Sent as Authorization: Bearer <token>.',
                password: true,
                ignoreFocusOut: true,
                placeHolder: 'Paste your token (stored in VS Code secrets)'
            });
        const trimmed = (value ?? '').trim();
        if (!trimmed)
            return;
        await this.context.secrets.store(OLLAMA_AUTH_SECRET_KEY, trimmed);
        await this.syncState();
    }
    async clearOllamaAuthToken() {
        await this.context.secrets.delete(OLLAMA_AUTH_SECRET_KEY);
        await this.syncState();
    }
    async showApiKeyOverlay() {
        this.pendingOpenSettings = true;
        await this.reveal();
        if (this.view) {
            this.postMessage({ type: 'openSettings' });
            this.pendingOpenSettings = false;
        }
    }
    async setPendingPrompt(prompt) {
        this.pendingPrompt = prompt;
        await this.syncState();
    }
    setOllamaStatus(status, missingModel) {
        this.ollamaStatus = status;
        this.ollamaModelMissing = missingModel;
        void this.syncState();
    }
    async toggleMode() {
        const nextMode = this.activeMode === 'agent' ? 'ask' : 'agent';
        await this.updateActiveMode(nextMode, { announce: true });
    }
    async updateActiveMode(mode, options) {
        if (mode !== 'ask' && mode !== 'agent') {
            return;
        }
        if (this.activeMode === mode) {
            return;
        }
        this.activeMode = mode;
        await this.context.workspaceState.update(MODE_STORAGE_KEY, mode);
        await this.syncState();
        if (options?.announce) {
            const label = mode === 'agent' ? 'Agent' : 'Ask';
            void vscode.window.showInformationMessage(`Bandit Stealth switched to ${label} mode.`);
        }
    }
    resolveWebviewView(view) {
        this.view = view;
        view.webview.options = {
            enableScripts: true
        };
        environmentService_1.environmentService.setWebview(view.webview);
        view.webview.html = this.getHtml(view.webview);
        view.webview.onDidReceiveMessage((message) => {
            void this.handleMessage(message);
        });
        void this.syncState();
    }
    async handleMessage(message) {
        if (message.type === 'requestState') {
            await this.syncState();
            return;
        }
        if (message.type === 'setApiKey') {
            const trimmed = message.value.trim();
            if (!trimmed) {
                this.postMessage({ type: 'notification', message: 'API key cannot be empty.' });
                return;
            }
            this.cancelActiveStream();
            this.isBusy = false;
            await this.context.secrets.store(API_KEY_SECRET_KEY, trimmed);
            await this.syncState();
            // silent success — the settings panel already reflects the saved state.
            void this.refreshAccountProfile();
            return;
        }
        if (message.type === 'setOllamaAuthToken') {
            await this.setOllamaAuthToken(message.value);
            return;
        }
        if (message.type === 'clearOllamaAuthToken') {
            await this.clearOllamaAuthToken();
            return;
        }
        if (message.type === 'setOllamaBaseUrl') {
            const trimmed = (message.value ?? '').trim();
            const config = vscode.workspace.getConfiguration('banditStealth');
            await config.update('ollamaBaseUrl', trimmed, vscode.ConfigurationTarget.Global);
            // Keep legacy alias in sync so older code paths (and the picker's
            // readiness probe) pick up the new URL without a reload.
            await config.update('ollamaUrl', trimmed, vscode.ConfigurationTarget.Global);
            await this.syncState();
            return;
        }
        if (message.type === 'clearApiKey') {
            await this.clearApiKey();
            return;
        }
        if (message.type === 'clearConversation') {
            await this.clearCurrentConversation();
            return;
        }
        if (message.type === 'startNewConversation') {
            await this.startNewConversation();
            return;
        }
        if (message.type === 'selectConversation') {
            await this.selectConversation(message.id);
            return;
        }
        if (message.type === 'deleteConversation') {
            await this.deleteConversation(message.id);
            return;
        }
        if (message.type === 'archiveConversation') {
            await this.setConversationArchived(message.id, message.archived);
            return;
        }
        if (message.type === 'showHistory') {
            if (message.value) {
                await this.openHistoryView();
            }
            else {
                if (this.historyVisible) {
                    this.historyVisible = false;
                    await this.syncState();
                }
            }
            return;
        }
        if (message.type === 'setMode') {
            // Mode toggle removed — single agent mode. Ignore legacy messages.
            return;
        }
        if (message.type === 'clearAllConversations') {
            await this.clearAllConversations();
            return;
        }
        if (message.type === 'requestClearAll') {
            await this.confirmAndClearAll();
            return;
        }
        if (message.type === 'submitFeedback') {
            await this.handleFeedbackSubmission(message.messageId, message.rating);
            return;
        }
        if (message.type === 'dismissIntent') {
            await this.clearLatestIntentFromConversation();
            await this.setIntentInsight(undefined);
            return;
        }
        if (message.type === 'dismissIntentSuggestions') {
            const configuration = vscode.workspace.getConfiguration('banditStealth');
            await configuration.update('intent.showSuggestions', false, vscode.ConfigurationTarget.Global);
            // silent — toggling visibility is self-evident in the UI.
            await this.syncState();
            return;
        }
        if (message.type === 'replayPlanStep') {
            await this.agentRuntime.replayStep(message.id, 'replay');
            return;
        }
        if (message.type === 'refinePlanStep') {
            await this.agentRuntime.replayStep(message.id, 'refine');
            return;
        }
        if (message.type === 'openFileFromDiff') {
            await this.openFileFromWorkspacePath(message.path);
            return;
        }
        if (message.type === 'openContextFile') {
            await this.openFileFromWorkspacePath(message.path);
            return;
        }
        if (message.type === 'diffPreviewAction') {
            await this.handleDiffPreviewAction(message);
            return;
        }
        if (message.type === 'undoAgentChange') {
            await this.handleUndoAgentChange();
            return;
        }
        if (message.type === 'requestAccountProfile') {
            void this.refreshAccountProfile();
            return;
        }
        if (message.type === 'permissionResponse') {
            const resolver = this.pendingPermissions.get(message.id);
            if (resolver)
                resolver(message.choice, message.notes);
            return;
        }
        if (message.type === 'requestSkillList') {
            void this.sendSkillList();
            return;
        }
        if (message.type === 'setConfig') {
            const configuration = vscode.workspace.getConfiguration('banditStealth');
            if (message.key === 'agent.autoApproveEdits') {
                await configuration.update('agent.autoApproveEdits', message.value === true, vscode.ConfigurationTarget.Workspace);
                await this.syncState();
            }
            return;
        }
        if (message.type === 'updatePreference') {
            const configuration = vscode.workspace.getConfiguration('banditStealth');
            if (message.key === 'intent.showSuggestions') {
                await configuration.update('intent.showSuggestions', message.value !== false, vscode.ConfigurationTarget.Global);
                await this.syncState();
            }
            if (message.key === 'feedback.enabled') {
                await configuration.update('feedback.enabled', message.value !== false, vscode.ConfigurationTarget.Global);
                await this.syncState();
            }
            if (message.key === 'debug.emitPlanJson') {
                await configuration.update('debug.emitPlanJson', message.value !== false, vscode.ConfigurationTarget.Workspace);
                await this.syncState();
            }
            if (message.key === 'agent.skipValidationInDev') {
                await configuration.update('agent.skipValidationInDev', message.value === true, vscode.ConfigurationTarget.Global);
                await this.syncState();
            }
            if (message.key === 'enableToolUse') {
                await configuration.update('enableToolUse', message.value === true, vscode.ConfigurationTarget.Workspace);
                await this.syncState();
            }
            if (message.key === 'agent.createBranchBeforeRun') {
                await configuration.update('agent.createBranchBeforeRun', message.value === true, vscode.ConfigurationTarget.Workspace);
                await this.syncState();
            }
            return;
        }
        if (message.type === 'setProvider') {
            const normalized = message.value;
            if (normalized !== 'bandit' && normalized !== 'ollama') {
                return;
            }
            const configuration = vscode.workspace.getConfiguration('banditStealth');
            await configuration.update('provider', normalized, vscode.ConfigurationTarget.Global);
            if (normalized !== 'ollama') {
                const apiKey = await this.context.secrets.get(API_KEY_SECRET_KEY);
                if (!apiKey) {
                    this.postMessage({ type: 'requireApiKey' });
                }
            }
            // Silent provider switch — the active-provider pill already reflects it.
            await this.syncState();
            void this.refreshAccountProfile();
            return;
        }
        if (message.type === 'editModel') {
            // Delegate to banditStealth.switchModel so the composer chip and the
            // status bar share one picker. v1.5.46 made switchModel Ollama-aware
            // (/api/tags discovery, free-text fallback for remote endpoints);
            // this handler used to open a dumb InputBox, which is why clicking
            // the composer chip bypassed discovery entirely.
            await vscode.commands.executeCommand('banditStealth.switchModel');
            await this.syncState();
            return;
        }
        if (message.type === 'editOllamaUrl') {
            const configuration = vscode.workspace.getConfiguration('banditStealth');
            const current = configuration.get('ollamaBaseUrl', '') ||
                configuration.get('ollamaUrl', 'http://localhost:11434') ||
                'http://localhost:11434';
            const input = await vscode.window.showInputBox({
                title: 'Set Ollama URL',
                prompt: 'Enter the Ollama base URL (e.g. http://localhost:11434).',
                value: current,
                ignoreFocusOut: true
            });
            if (input && input.trim()) {
                const normalized = input.trim().replace(/\/+$/, '');
                await configuration.update('ollamaBaseUrl', normalized, vscode.ConfigurationTarget.Global);
                await configuration.update('ollamaUrl', normalized, vscode.ConfigurationTarget.Global);
                // silent — settings panel reflects the new URL.
                await this.syncState();
            }
            return;
        }
        if (message.type === 'cancelResponse') {
            if (this.activeMode === 'agent') {
                this.agentRuntime.cancel();
                await environmentService_1.environmentService.postToWebview({ type: 'agent:log', entry: { message: 'Cancellation requested…', level: 'warn' } });
                await this.setBusy(false, 'Agent cancelled');
                return;
            }
            this.cancelActiveStream();
            await this.setBusy(false, 'Cancelled');
            return;
        }
        if (message.type === 'sendPrompt') {
            await this.handlePrompt(message.text, message.images, message.mode ?? 'ask', message.files, message.autoContext);
            return;
        }
        if (message.type === 'requestContextFiles') {
            await this.handleContextFileRequest();
        }
        if (message.type === 'searchWorkspaceFiles') {
            await this.handleWorkspaceFileSearch(message.query);
        }
    }
    /**
     * Lightweight fuzzy file search for @ mention autocomplete. Returns up
     * to 12 workspace-relative paths matching the query. Empty query
     * returns the most-recently-touched paths (best-effort from VS Code's
     * recent-files list) or a broad sampling. Intentionally avoids the
     * heavier pickContextAttachments flow — this fires on every keystroke
     * while a user types `@<token>` so it needs to be cheap.
     */
    async handleWorkspaceFileSearch(rawQuery) {
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (!workspaceFolder) {
            this.postMessage({ type: 'workspaceFileSuggestions', files: [] });
            return;
        }
        const query = rawQuery.trim();
        const workspaceRoot = workspaceFolder.uri.fsPath;
        // When the token is empty, show a sensible default: recently-edited
        // text files in the workspace. Otherwise use a glob that biases
        // toward the basename match that the user is probably aiming for.
        const pattern = query.length === 0
            ? new vscode.RelativePattern(workspaceFolder, '**/*')
            : new vscode.RelativePattern(workspaceFolder, `**/*${query}*`);
        try {
            const uris = await vscode.workspace.findFiles(pattern, '**/node_modules/**', 80);
            const rel = uris
                .map(u => path.relative(workspaceRoot, u.fsPath))
                .filter(p => p.length > 0 && !p.includes('/.git/'))
                .map(p => ({ path: p, basename: path.basename(p) }));
            // Rank: exact basename prefix match > basename contains > full-path contains.
            const lower = query.toLowerCase();
            const ranked = rel.sort((a, b) => {
                const aBase = a.basename.toLowerCase();
                const bBase = b.basename.toLowerCase();
                const aPrefix = aBase.startsWith(lower);
                const bPrefix = bBase.startsWith(lower);
                if (aPrefix !== bPrefix)
                    return aPrefix ? -1 : 1;
                const aContains = aBase.includes(lower);
                const bContains = bBase.includes(lower);
                if (aContains !== bContains)
                    return aContains ? -1 : 1;
                return a.path.localeCompare(b.path);
            });
            const files = ranked.slice(0, 12).map(r => r.path);
            this.postMessage({ type: 'workspaceFileSuggestions', files });
        }
        catch {
            this.postMessage({ type: 'workspaceFileSuggestions', files: [] });
        }
    }
    async handlePrompt(rawText, images, mode, files, autoContext) {
        const prompt = rawText.trim();
        if (!prompt) {
            this.postMessage({ type: 'notification', message: 'Enter a prompt to continue.' });
            return;
        }
        const configuration = vscode.workspace.getConfiguration('banditStealth');
        const providerKind = this.getProviderKind(configuration);
        const apiKey = await this.context.secrets.get(API_KEY_SECRET_KEY);
        const requestedImages = Array.isArray(images)
            ? images.map((image) => (typeof image === 'string' ? image.trim() : '')).filter((image) => image.length > 0)
            : [];
        const askModel = this.resolveChatModel(configuration, requestedImages.length > 0);
        const allowInlineImages = this.canUseInlineImages(configuration, askModel);
        // OCR-first fallback: when the active model can't see images but the
        // user attached one, try local OCR (Apple Vision on mac, tesseract
        // otherwise) to extract text and inline it — keeps the user on their
        // chosen model (e.g. bandit-logic for code work) and avoids the
        // cost/latency of a model swap for the most common case (screenshot
        // of code / stack trace / dialog text). If OCR yields nothing useful,
        // we leave `allowInlineImages: false` as before and fall through to
        // the existing vision-model path.
        let ocrExtractedText = '';
        let ocrEngineUsed = null;
        if (!allowInlineImages && requestedImages.length > 0) {
            const ocrMode = configuration.get('ocrFallback', 'ocr-first');
            const ocrWorkspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath ?? process.cwd();
            if (ocrMode !== 'off') {
                // Images from the webview arrive as base64 data URLs (Ctrl+V
                // paste) OR plain workspace paths (@-mention attach). OCR
                // engines need a real file, so decode data URLs to a tempfile
                // first. Track temp paths for cleanup after the OCR call.
                const tempPaths = [];
                for (let idx = 0; idx < requestedImages.length; idx++) {
                    const raw = requestedImages[idx];
                    let resolvedPath = '';
                    let displayLabel = '';
                    try {
                        if (/^data:image\//i.test(raw)) {
                            const commaIdx = raw.indexOf(',');
                            const b64 = commaIdx >= 0 ? raw.slice(commaIdx + 1) : '';
                            const mimeMatch = /^data:(image\/[\w+.-]+)/i.exec(raw);
                            const ext = mimeMatch ? mimeMatch[1].split('/')[1].split('+')[0] : 'png';
                            const tmpPath = path.join(os.tmpdir(), `bandit-ocr-${Date.now()}-${idx}.${ext}`);
                            fs.writeFileSync(tmpPath, Buffer.from(b64, 'base64'));
                            tempPaths.push(tmpPath);
                            resolvedPath = tmpPath;
                            displayLabel = `pasted.${ext}`;
                        }
                        else if (/^https?:/i.test(raw)) {
                            // Remote URLs — skip OCR (would require a fetch roundtrip).
                            continue;
                        }
                        else {
                            resolvedPath = path.isAbsolute(raw) ? raw : path.resolve(ocrWorkspaceRoot, raw);
                            displayLabel = path.basename(raw);
                        }
                        const result = await (0, agent_core_1.extractImageText)(resolvedPath);
                        if ((0, agent_core_1.ocrYieldedUsefulText)(result.text)) {
                            ocrExtractedText += (ocrExtractedText ? '\n\n' : '')
                                + `[Image text (OCR via ${result.engine}): ${displayLabel}]\n${result.text}`;
                            ocrEngineUsed = result.engine;
                        }
                    }
                    catch {
                        // Silent skip — fall through to existing notification path.
                    }
                }
                for (const tmp of tempPaths) {
                    try {
                        fs.unlinkSync(tmp);
                    }
                    catch { /* best-effort cleanup */ }
                }
            }
        }
        const normalizedImages = allowInlineImages
            ? requestedImages
            // OCR succeeded → consume the images (don't also send them as
            // inline content to a non-vision model where they'd be rejected).
            : (ocrExtractedText ? [] : requestedImages);
        if (!allowInlineImages && requestedImages.length > 0 && !ocrExtractedText) {
            this.postMessage({
                type: 'notification',
                message: providerKind === 'ollama'
                    ? `Inline images are disabled because "${askModel}" is not configured as a vision model. Set banditStealth.ollamaVisionModel to gemma3 or another vision-capable model.`
                    : 'Inline images are only supported for Bandit AI bandit-core models.'
            });
        }
        if (ocrEngineUsed) {
            this.postMessage({
                type: 'notification',
                message: `Extracted text from image via ${ocrEngineUsed} — staying on ${askModel} for this turn.`
            });
        }
        if (this.historyVisible) {
            this.historyVisible = false;
        }
        if (!apiKey && providerKind === 'bandit') {
            this.postMessage({ type: 'requireApiKey' });
            await this.showApiKeyOverlay();
            return;
        }
        const currentConversation = this.ensureActiveConversation();
        if (currentConversation.archived) {
            currentConversation.archived = false;
        }
        const autoContextRequested = autoContext !== false;
        const manualContextFiles = Array.isArray(files) ? files.slice() : [];
        const manualContextProvided = manualContextFiles.length > 0;
        let contextFiles = manualContextFiles;
        const heuristicsAllowAuto = this.shouldInjectContext(prompt);
        const allowAutoContext = autoContextRequested && heuristicsAllowAuto;
        const semanticContextPromise = providerKind === 'bandit' && apiKey
            ? this.fetchSemanticKnowledge(prompt, configuration, apiKey).catch((error) => {
                console.warn('Semantic context fetch failed', error);
                return '';
            })
            : Promise.resolve('');
        if (contextFiles.length === 0) {
            if (allowAutoContext) {
                void this.setStatusMessage('Selecting context files…');
                const autoFiles = await this.autoSelectContextFiles(prompt);
                if (autoFiles.length > 0) {
                    contextFiles = autoFiles;
                    // Silent — the chip row underneath the input already shows attached files.
                }
            }
            else if (!autoContextRequested) {
                // user disabled auto context; no action
            }
            else {
                const contextMessage = {
                    type: 'contextInjectionSkipped',
                    reason: 'simple-prompt',
                    prompt: prompt.slice(0, 160)
                };
                this.postMessage(contextMessage);
            }
        }
        const contextSource = contextFiles.length > 0 ? (manualContextProvided ? "manual" : "auto") : undefined;
        const contextExpansion = contextFiles.length > 0
            ? await (async () => {
                void this.setStatusMessage('Preparing attached context…');
                return this.expandPromptWithFiles(prompt, contextFiles, {
                    source: contextSource
                });
            })()
            : { display: prompt, payload: prompt, warnings: [], contextFiles: [] };
        for (const warning of contextExpansion.warnings) {
            this.postMessage({ type: 'notification', message: warning });
        }
        const entryImages = normalizedImages
            .map((image) => this.extractImagePayload(image))
            .filter((image) => image.length > 0);
        const semanticContext = await semanticContextPromise;
        const payloadWithKnowledge = semanticContext
            ? `${semanticContext}\n\n${contextExpansion.payload}`
            : contextExpansion.payload;
        const userEntry = createConversationEntry('user', contextExpansion.display, {
            images: entryImages,
            payload: payloadWithKnowledge,
            contextFiles: contextExpansion.contextFiles,
            contextSource
        });
        const usageCheck = this.calculateContextUsage(configuration, [...this.conversation, userEntry]);
        if (usageCheck && usageCheck.used > usageCheck.limit) {
            this.postMessage({ type: 'notification', message: `Message would exceed Bandit AI context window (${usageCheck.used.toLocaleString()} / ${usageCheck.limit.toLocaleString()} tokens).` });
            return;
        }
        await this.updateConversation([...this.conversation, userEntry]);
        await this.syncState();
        // Single execution path: always use the tool-use loop.
        // The model decides whether to use tools (for code tasks) or just answer (for questions).
        await this.performCompletion(apiKey ?? '', configuration);
    }
    async handleContextFileRequest() {
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (!workspaceFolder) {
            this.postMessage({ type: 'notification', message: 'Open a workspace to attach files.' });
            return;
        }
        const selection = await this.pickContextAttachments();
        if (!selection) {
            return;
        }
        const attachments = selection.files.length > 0
            ? await this.loadContextFileAttachments(workspaceFolder, selection.files)
            : [];
        if (attachments.length > 0) {
            this.postMessage({ type: 'contextFilesAdded', files: attachments });
        }
        if (selection.addImage) {
            const images = await this.pickImageAttachments(workspaceFolder);
            if (images.length > 0) {
                this.postMessage({ type: 'imageAttachmentsAdded', images });
            }
        }
    }
    async expandPromptWithFiles(prompt, files, options) {
        if (!files || files.length === 0) {
            return { display: prompt, payload: prompt, warnings: [], contextFiles: [] };
        }
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (!workspaceFolder) {
            return {
                display: prompt,
                payload: prompt,
                warnings: ['Context files require an open workspace.'],
                contextFiles: []
            };
        }
        const uniquePaths = Array.from(new Set(files.map((file) => file.trim()).filter((file) => file.length > 0)));
        if (uniquePaths.length === 0) {
            return { display: prompt, payload: prompt, warnings: [], contextFiles: [] };
        }
        const workspaceRoot = path.resolve(workspaceFolder.uri.fsPath);
        const decoder = new util_1.TextDecoder('utf-8', { fatal: false });
        const blocks = [];
        const warnings = [];
        const includedPaths = [];
        const limit = 5;
        if (uniquePaths.length > limit) {
            // Silent cap: pushing this as a warning floods the notification area.
        }
        const pathsToProcess = uniquePaths.slice(0, limit);
        for (const relativePath of pathsToProcess) {
            const absolutePath = path.resolve(workspaceRoot, relativePath);
            if (!absolutePath.startsWith(workspaceRoot)) {
                warnings.push(`Skipping ${relativePath} (outside workspace).`);
                continue;
            }
            try {
                const uri = vscode.Uri.file(absolutePath);
                const stat = await vscode.workspace.fs.stat(uri);
                // Sniff the first 4KB to detect binary without reading the full file —
                // a 400KB JPG shouldn't incur a full-file read just to classify it.
                const headBuf = await vscode.workspace.fs.readFile(uri).then(b => b.slice(0, 4096));
                if (this.isLikelyBinary(headBuf)) {
                    // Silent skip — user sees the absent attachment, no toast needed.
                    continue;
                }
                // Reference-only: list path + size so the model knows the file
                // exists and how big it is, but DOES NOT inline the content.
                // The model has `read_file` and will fetch on demand. Previously
                // we inlined up to ~40KB per file, which for a typical 3-file
                // auto-context attachment burned 30-120k tokens before the turn
                // even started — on a 16k num_ctx Ollama model that deleted the
                // system prompt via compaction before iteration 1 finished.
                blocks.push(`- \`${relativePath}\` (${stat.size} bytes) — use read_file when needed`);
                includedPaths.push(relativePath);
            }
            catch (error) {
                const message = error instanceof Error ? error.message : String(error);
                warnings.push(`Unable to read ${relativePath}: ${message}`);
            }
        }
        if (blocks.length === 0) {
            return { display: prompt, payload: prompt, warnings, contextFiles: [] };
        }
        // The deliberation phrasing we used to ship here ("briefly reason whether
        // they are required … if unnecessary, ignore them and explain why") gave
        // small models a free escape hatch: when the task felt big, they'd write
        // a reasoning paragraph instead of calling tools. Action-worded prompts
        // need action-worded framing. We still allow read-only questions to skip
        // edits — the tools themselves are optional — but we no longer prompt
        // the model to talk about the files instead of touching them.
        const instructions = options?.source === 'auto'
            ? [
                'The files below are the target of this request.',
                'Use `read_file` to load them, then `write_file` (or the relevant edit tool) to apply the changes.',
                'Do not stop after describing the code — complete the task by invoking tools.'
            ].join(' ')
            : '';
        const payloadSections = [];
        if (prompt.length > 0) {
            payloadSections.push(prompt);
        }
        if (instructions) {
            payloadSections.push(instructions);
        }
        payloadSections.push(`---\nRelevant files (read them with \`read_file\` before editing):\n${blocks.join('\n')}`);
        const payload = payloadSections.join('\n\n');
        const display = prompt;
        return { display, payload, warnings, contextFiles: includedPaths };
    }
    shouldTreatAsQuestion(prompt) {
        const normalized = prompt.trim().toLowerCase();
        if (!normalized) {
            return false;
        }
        const questionIndicators = normalized.endsWith('?')
            || normalized.startsWith('what ')
            || normalized.startsWith('where ')
            || normalized.startsWith('when ')
            || normalized.startsWith('who ')
            || normalized.startsWith('should ')
            || normalized.startsWith('why ')
            || normalized.startsWith('how ')
            || normalized.startsWith('which ')
            || normalized.startsWith('explain ')
            || normalized.startsWith('describe ')
            || normalized.startsWith('show me')
            || normalized.startsWith('tell me')
            || normalized.includes('what is ')
            || normalized.includes('how do i');
        if (!questionIndicators) {
            return false;
        }
        const actionPhrases = [
            'can you update',
            'please update',
            'can you add',
            'please add',
            'can you implement',
            'please implement',
            'could you update',
            'would you update',
            'could you add',
            'would you add'
        ];
        for (const phrase of actionPhrases) {
            if (normalized.includes(phrase)) {
                return false;
            }
        }
        const actionKeywords = [
            'update',
            'implement',
            'fix',
            'add',
            'create',
            'modify',
            'refactor',
            'remove',
            'replace',
            'build',
            'improve',
            'adjust',
            'optimize',
            'rewrite',
            'change',
            'edit',
            'refine'
        ];
        const tokens = new Set(normalized
            .split(/[^a-z0-9]+/)
            .map((token) => token.trim())
            .filter((token) => token.length > 0));
        for (const keyword of actionKeywords) {
            if (normalized.startsWith(`${keyword} `) || tokens.has(keyword)) {
                return false;
            }
        }
        return true;
    }
    shouldInjectContext(prompt) {
        const lower = prompt.trim().toLowerCase();
        if (!lower) {
            return true;
        }
        const short = lower.split(/\s+/).filter((token) => token.length > 0).length < 6;
        const simple = /\b(who|what|where|when|hi|hello|hey|are you)\b/.test(lower);
        return !(short && simple);
    }
    async autoSelectContextFiles(prompt, limit = 3) {
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0];
        if (!workspaceFolder) {
            return [];
        }
        const index = await this.loadWorkspaceFileIndex();
        if (!Array.isArray(index) || index.length === 0) {
            return [];
        }
        const normalizedPrompt = prompt.trim().toLowerCase();
        const tokens = normalizedPrompt.split(/[^a-z0-9]+/).filter((token) => token.length > 0);
        const wordCount = tokens.length;
        const questionStarters = ['who', 'what', 'where', 'when', 'why', 'how', 'which'];
        const looksQuestion = normalizedPrompt.endsWith('?') ||
            questionStarters.some((starter) => normalizedPrompt.startsWith(`${starter} `));
        const added = new Set();
        const selected = [];
        const addFile = (file) => {
            if (!file || added.has(file) || selected.length >= limit) {
                return;
            }
            added.add(file);
            selected.push(file);
        };
        const pathPattern = /(?:[^\s"'`]+\/)*[A-Za-z0-9_.-]+\.(?:tsx|ts|jsx|js|json|md|css|scss|html|yml|yaml)/gi;
        const explicitMatches = new Map();
        let pathMatch;
        while ((pathMatch = pathPattern.exec(prompt)) !== null) {
            const sanitized = pathMatch[0]
                .replace(/\\/g, '/')
                .replace(/^\.\/+/, '')
                .replace(/^\/+/, '')
                .replace(/\s+$/, '');
            if (sanitized) {
                explicitMatches.set(sanitized.toLowerCase(), sanitized);
            }
        }
        for (const raw of explicitMatches.values()) {
            const lower = raw.toLowerCase();
            const exact = index.find((entry) => entry.toLowerCase() === lower);
            if (exact) {
                addFile(exact);
            }
            else {
                const partial = index.find((entry) => entry.toLowerCase().endsWith(lower));
                if (partial) {
                    addFile(partial);
                }
            }
            if (selected.length >= limit) {
                return selected;
            }
        }
        const hasExplicitMatches = explicitMatches.size > 0;
        if (!hasExplicitMatches && (looksQuestion || wordCount < 4 || prompt.trim().length < 24)) {
            return [];
        }
        const tokenMatches = prompt.toLowerCase().match(/[a-z0-9][a-z0-9_-]{2,}/g) ?? [];
        const stopWords = new Set([
            'the', 'and', 'for', 'with', 'that', 'this', 'there', 'about', 'please', 'could', 'would', 'should',
            'bandit', 'stealth', 'agent', 'mode', 'question', 'repo', 'code', 'file', 'files',
            'explain', 'describe', 'thank', 'thanks', 'have', 'need', 'maybe', 'really', 'just', 'like', 'into',
            'from', 'your', 'you', 'what', 'where', 'when', 'why', 'which', 'how', 'does', 'make', 'using', 'are',
            'roughly', 'currently', 'actually', 'around', 'after', 'before'
        ]);
        const keywords = tokenMatches
            .filter((token) => token.length >= 3 && !stopWords.has(token))
            .slice(0, 24);
        if (!hasExplicitMatches && keywords.length < 2) {
            return selected;
        }
        if (keywords.length > 0) {
            const wantsTests = /\b(test|tests|spec|jest|vitest|xunit|nunit|integration|unit)\b/.test(normalizedPrompt);
            const wantsDocs = /\b(doc|docs|documentation|readme|changelog|guide)\b/.test(normalizedPrompt);
            const wantsConfig = /\b(config|configuration|settings?|env|dotenv|tsconfig|eslint|prettier|package\.json)\b/.test(normalizedPrompt);
            const wantsInfra = /\b(ci|cd|workflow|deploy|deployment|docker|kubernetes|k8s|helm|yaml|yml)\b/.test(normalizedPrompt);
            const looksBugReport = /\b(error|failed|failing|fails|bug|exception|stack|trace|regression)\b/.test(normalizedPrompt);
            const allowTestFiles = wantsTests || looksBugReport;
            const allowInfraFiles = wantsConfig || wantsInfra;
            const scored = [];
            const allowedExtensions = /\.(tsx|ts|jsx|js|json|md|css|scss|sass|less|html|yml|yaml|vue|svelte|cs|csx|java|kt|kts|sql|go|py|rb|php|c|cc|cpp|h|hpp|rs|swift|sh|bash|ps1|psm1)$/;
            const buildArtifactPattern = /(^|\/)(node_modules|dist|build|coverage|out|tmp|temp|\.next|target)(\/|$)/;
            const docsPattern = /(^|\/)(docs?|documentation)(\/|$)|(^|\/)readme(\.|$)|\.(md|mdx)$/;
            const testsPattern = /(^|\/)(test|tests|__tests__|spec|specs|e2e|integration)(\/|$)|\.(test|spec)\.[^.]+$/;
            const infraPattern = /(^|\/)(\.github|\.vscode|helm|charts?|k8s|kubernetes|config)(\/|$)|(^|\/)(dockerfile|docker-compose|compose)(\.|$)|\.ya?ml$/;
            const lockFilePattern = /(^|\/)(pnpm-lock\.yaml|package-lock\.json|yarn\.lock|bun\.lockb?|cargo\.lock)$/;
            for (const file of index) {
                if (added.has(file) || !allowedExtensions.test(file.toLowerCase())) {
                    continue;
                }
                const lower = file.toLowerCase();
                if (buildArtifactPattern.test(lower)) {
                    continue;
                }
                const isDocFile = docsPattern.test(lower);
                const isTestFile = testsPattern.test(lower);
                const isInfraFile = infraPattern.test(lower);
                const isLockFile = lockFilePattern.test(lower);
                if (isLockFile && !allowInfraFiles) {
                    continue;
                }
                if (isDocFile && !wantsDocs) {
                    continue;
                }
                if (isTestFile && !allowTestFiles) {
                    continue;
                }
                const pathParts = lower.split(/[\/._-]+/).filter((part) => part.length > 0);
                const basename = lower.split('/').pop() ?? lower;
                const extIndex = basename.lastIndexOf('.');
                const basenameStem = extIndex > 0 ? basename.slice(0, extIndex) : basename;
                let score = 0;
                let matches = 0;
                for (const keyword of keywords) {
                    if (!lower.includes(keyword)) {
                        continue;
                    }
                    matches += 1;
                    score += keyword.length;
                    if (basenameStem === keyword) {
                        score += 6;
                    }
                    if (pathParts.includes(keyword)) {
                        score += 3;
                    }
                }
                if (!hasExplicitMatches && matches < 2 && score < 10) {
                    continue;
                }
                if (isInfraFile && !allowInfraFiles) {
                    score -= 3;
                }
                if (/^(src|app|apps|packages|services)\//.test(lower)) {
                    score += 2;
                }
                if (/\.(tsx|ts|jsx|js|cs|csx|java|kt|go|py|rb|php|rs|swift)$/i.test(lower)) {
                    score += 2;
                }
                if (isTestFile && allowTestFiles) {
                    score += 2;
                }
                if (isDocFile && wantsDocs) {
                    score += 2;
                }
                if (/\/(examples?|samples?|demo)\//.test(lower) && !/\b(example|demo|sample)\b/.test(normalizedPrompt)) {
                    score -= 2;
                }
                if (score > 0) {
                    scored.push({ file, score, matches });
                }
            }
            scored.sort((a, b) => {
                if (a.score !== b.score) {
                    return b.score - a.score;
                }
                if (a.matches !== b.matches) {
                    return b.matches - a.matches;
                }
                return a.file.length - b.file.length;
            });
            for (const candidate of scored) {
                addFile(candidate.file);
                if (selected.length >= limit) {
                    break;
                }
            }
        }
        // Filesystem sanity check. The workspace index is loaded once and
        // cached for the life of the panel — files deleted/renamed after
        // that load can still appear as candidates, and the extension would
        // attach "src/utils/scoring.ts" (from the cached index) even though
        // the real file no longer exists. Confirm every selected path still
        // resolves before handing the list back. If any path is missing, we
        // drop it AND force a fresh index scan so subsequent prompts don't
        // keep offering the ghost path. Observed in pburg-bowl on 2026-04-21.
        if (selected.length === 0) {
            return selected;
        }
        const workspaceRoot = workspaceFolder.uri.fsPath;
        const verified = [];
        let anyMissing = false;
        for (const relPath of selected) {
            try {
                const absolute = path.resolve(workspaceRoot, relPath);
                if (!absolute.startsWith(workspaceRoot)) {
                    anyMissing = true;
                    continue;
                }
                await vscode.workspace.fs.stat(vscode.Uri.file(absolute));
                verified.push(relPath);
            }
            catch {
                anyMissing = true;
            }
        }
        if (anyMissing) {
            // Invalidate the cache so the next auto-context pass picks up the
            // real filesystem state — otherwise we keep handing out the same
            // stale paths every prompt.
            this.workspaceFileIndex = undefined;
        }
        return verified;
    }
    async pickContextAttachments() {
        const files = await this.loadWorkspaceFileIndex();
        if (files.length === 0) {
            // silent — the empty state is self-evident (chip row stays empty).
            return undefined;
        }
        const items = files.map((relativePath) => {
            const normalized = relativePath.replace(/\\/g, '/');
            const segments = normalized.split('/');
            const label = segments.pop() ?? normalized;
            const description = segments.join('/');
            return {
                label,
                description,
                detail: normalized,
                value: normalized
            };
        });
        const addImageItem = {
            label: '$(file-media) Add image…',
            description: 'Attach an image from disk.',
            detail: '',
            value: '__add_image__',
            alwaysShow: true
        };
        const quickPick = vscode.window.createQuickPick();
        quickPick.canSelectMany = true;
        quickPick.matchOnDescription = true;
        quickPick.matchOnDetail = true;
        quickPick.placeholder = 'Search workspace files to attach…';
        quickPick.title = 'Add Bandit context';
        quickPick.items = [addImageItem, ...items];
        const selection = await new Promise((resolve) => {
            let resolved = false;
            const finalize = (value) => {
                if (resolved) {
                    return;
                }
                resolved = true;
                resolve(value);
            };
            quickPick.onDidAccept(() => {
                finalize([...quickPick.selectedItems]);
                quickPick.hide();
            });
            quickPick.onDidHide(() => finalize(undefined));
            quickPick.show();
        });
        quickPick.dispose();
        if (!selection || selection.length === 0) {
            return undefined;
        }
        const addImage = selection.some((item) => item.value === '__add_image__');
        const filesToAttach = selection
            .filter((item) => item.value !== '__add_image__')
            .map((item) => item.value)
            .filter((value, index, array) => array.indexOf(value) === index);
        return { files: filesToAttach, addImage };
    }
    async loadWorkspaceFileIndex(force = false) {
        if (!force && Array.isArray(this.workspaceFileIndex) && this.workspaceFileIndex.length > 0) {
            return this.workspaceFileIndex;
        }
        const folder = vscode.workspace.workspaceFolders?.[0];
        if (!folder) {
            this.workspaceFileIndex = [];
            return [];
        }
        const exclude = '{**/node_modules/**,**/.git/**,**/dist/**,**/build/**,**/out/**,**/.bandit/**}';
        const uris = await vscode.workspace.findFiles('**/*', exclude, 6000);
        const root = folder.uri.fsPath;
        const files = uris
            .map((uri) => path.relative(root, uri.fsPath).replace(/\\/g, '/'))
            .filter((relative) => relative && !relative.endsWith('/'));
        files.sort((a, b) => a.localeCompare(b));
        this.workspaceFileIndex = files;
        return files;
    }
    async loadContextFileAttachments(workspaceFolder, files) {
        if (files.length === 0) {
            return [];
        }
        const workspaceRoot = path.resolve(workspaceFolder.uri.fsPath);
        const decoder = new util_1.TextDecoder('utf-8', { fatal: false });
        const attachments = [];
        for (const relativePath of files) {
            const normalized = relativePath.replace(/\\/g, '/');
            const absolutePath = path.resolve(workspaceRoot, normalized);
            if (!absolutePath.startsWith(workspaceRoot)) {
                this.postMessage({ type: 'notification', message: `Skipping ${normalized} (outside workspace).` });
                continue;
            }
            const uri = vscode.Uri.file(absolutePath);
            try {
                const stat = await vscode.workspace.fs.stat(uri);
                let preview = '';
                if (stat.size <= 200000) {
                    const buffer = await vscode.workspace.fs.readFile(uri);
                    if (this.isLikelyBinary(buffer)) {
                        preview = 'Binary file — preview unavailable.';
                    }
                    else {
                        const decoded = decoder.decode(buffer);
                        preview = this.buildContextPreview(decoded);
                    }
                }
                else {
                    preview = 'Preview unavailable (file larger than 200 KB).';
                }
                attachments.push({ path: normalized, preview });
            }
            catch (error) {
                const message = error instanceof Error ? error.message : String(error);
                this.postMessage({ type: 'notification', message: `Unable to read ${normalized}: ${message}` });
            }
        }
        return attachments;
    }
    async pickImageAttachments(workspaceFolder) {
        const uris = await vscode.window.showOpenDialog({
            canSelectMany: true,
            openLabel: 'Add image',
            defaultUri: workspaceFolder.uri,
            filters: { Images: ['png', 'jpg', 'jpeg', 'gif', 'webp', 'bmp', 'svg'] }
        });
        if (!uris || uris.length === 0) {
            return [];
        }
        const maxBytes = 4000000; // ~4 MB
        const images = [];
        for (const uri of uris) {
            try {
                const stat = await vscode.workspace.fs.stat(uri);
                if (stat.size > maxBytes) {
                    this.postMessage({ type: 'notification', message: `${path.basename(uri.fsPath)} is larger than 4 MB and was skipped.` });
                    continue;
                }
                const buffer = await vscode.workspace.fs.readFile(uri);
                const ext = path.extname(uri.fsPath).toLowerCase();
                const mime = this.getImageMimeType(ext);
                const base64 = Buffer.from(buffer).toString('base64');
                images.push(`data:${mime};base64,${base64}`);
            }
            catch (error) {
                const message = error instanceof Error ? error.message : String(error);
                this.postMessage({ type: 'notification', message: `Unable to load image ${path.basename(uri.fsPath)}: ${message}` });
            }
        }
        return images;
    }
    getImageMimeType(ext) {
        switch (ext) {
            case '.jpg':
            case '.jpeg':
                return 'image/jpeg';
            case '.gif':
                return 'image/gif';
            case '.webp':
                return 'image/webp';
            case '.bmp':
                return 'image/bmp';
            case '.svg':
            case '.svgz':
                return 'image/svg+xml';
            case '.png':
            default:
                return 'image/png';
        }
    }
    buildContextPreview(content) {
        const normalized = content.replace(/\r\n/g, '\n').trim();
        if (!normalized) {
            return '';
        }
        const lines = normalized.split('\n');
        const snippet = lines.slice(0, 3).join(' · ');
        if (snippet.length <= 120) {
            return snippet;
        }
        return `${snippet.slice(0, 119)}…`;
    }
    truncateContextAttachment(content, maxLines = 120, maxLength = 6000) {
        const normalized = content.replace(/\r\n/g, '\n');
        const lines = normalized.split('\n');
        const selected = lines.slice(0, maxLines);
        let joined = selected.join('\n');
        if (lines.length > maxLines) {
            joined += '\n…';
        }
        if (joined.length > maxLength) {
            joined = `${joined.slice(0, maxLength - 1)}…`;
        }
        return joined;
    }
    isLikelyBinary(buffer) {
        const sampleLength = Math.min(buffer.length, 1024);
        for (let index = 0; index < sampleLength; index += 1) {
            if (buffer[index] === 0) {
                return true;
            }
        }
        return false;
    }
    async startAgentGoal(goal) {
        this.cancelActiveStream();
        this.activeMode = 'agent';
        const conversation = this.ensureActiveConversation();
        environmentService_1.environmentService.setRunContext({
            conversationId: conversation.id,
            conversationName: conversation.name,
            runId: undefined
        });
        if (this.historyVisible) {
            this.historyVisible = false;
        }
        await this.context.workspaceState.update(MODE_STORAGE_KEY, this.activeMode);
        await this.setBusy(true, 'Agent running…');
        try {
            const report = await this.promptPipeline.execute(goal, 'agent');
            const summary = this.formatAgentReport(report);
            const agentReply = await this.generateAgentReply(goal, report).catch((replyError) => {
                void environmentService_1.environmentService.postToWebview({ type: 'agent:log', entry: { message: `Reply error: ${replyError instanceof Error ? replyError.message : String(replyError)}`, level: 'warn' } });
                return undefined;
            });
            const trimmedReply = agentReply?.trim() ?? null;
            const primaryContent = trimmedReply ?? this.buildAgentSummaryHeadline(report);
            await this.appendAssistantMessage(primaryContent, {
                payload: this.buildAgentSummaryPayload(report, summary, trimmedReply)
            });
            await this.setBusy(false);
            void this.presentDiffFeedback(report).catch((error) => {
                console.warn('Unable to present diff feedback', error);
            });
        }
        catch (error) {
            const message = error instanceof Error ? error.message : 'Unknown issue.';
            this.postMessage({ type: 'error', message: `Agent error: ${message}` });
            void vscode.window.showErrorMessage(`Agent error: ${message}`);
            await environmentService_1.environmentService.postToWebview({ type: 'agent:log', entry: { message: `Error: ${message}`, level: 'error' } });
            await environmentService_1.environmentService.postToWebview({ type: 'agent:status', text: 'Agent failed', phase: 'error' });
            await environmentService_1.environmentService.postToWebview({ type: 'agent:final', report: { evaluation: { success: false } } });
            await this.appendAssistantMessage(`Agent run failed: ${message}`);
            await this.setBusy(false, 'Agent failed');
        }
        finally {
            environmentService_1.environmentService.setRunContext(undefined);
        }
    }
    async previewAgentPlan(goal) {
        const conversation = this.ensureActiveConversation();
        environmentService_1.environmentService.setRunContext({
            conversationId: conversation.id,
            conversationName: conversation.name,
            runId: undefined
        });
        try {
            const report = await this.promptPipeline.preview(goal);
            if (Array.isArray(report.plan?.steps) && report.plan.steps.length > 0) {
                // silent — the Plan tab itself surfaces the new preview.
            }
        }
        catch (error) {
            const message = error instanceof Error ? error.message : 'Preview failed.';
            console.warn('Plan preview error', error);
            this.postMessage({ type: 'notification', message: `Plan preview failed: ${message}` });
        }
        finally {
            environmentService_1.environmentService.setRunContext(undefined);
        }
    }
    deriveAgentSummary(report) {
        const confidence = Number.isFinite(report.evaluation?.confidence) ? report.evaluation.confidence : null;
        const success = report.evaluation?.success ?? false;
        const iterations = report.iterations;
        const planSteps = Array.isArray(report.plan?.steps) ? report.plan.steps : [];
        const planLookup = new Map(planSteps.map((step) => [step.id, step]));
        const contextPathSet = new Set();
        const steps = [];
        const filesMap = new Map();
        const ensureFileEntry = (path, placeholder, status) => {
            const existing = filesMap.get(path);
            if (!existing) {
                const entry = {
                    path,
                    status,
                    placeholder,
                    diff: null,
                    summary: null,
                    confidence: null,
                    backupPath: null,
                    review: null
                };
                filesMap.set(path, entry);
                return entry;
            }
            if (status === 'error') {
                existing.status = 'error';
            }
            else if (existing.status !== 'error') {
                existing.status = status;
            }
            if (!placeholder) {
                existing.placeholder = false;
            }
            return existing;
        };
        for (const result of report.results ?? []) {
            const step = planLookup.get(result.stepId);
            const title = step?.title ?? result.stepId;
            const command = typeof step?.command === 'string' ? step.command : undefined;
            const placeholder = this.isPlaceholderCommand(command);
            const status = result.ok ? 'complete' : 'error';
            const data = result.data;
            const primaryPath = typeof data?.path === 'string' ? data.path : undefined;
            const snippetSource = (result.output ?? '').toString().trim() || (result.error ?? '').toString().trim();
            let summary;
            if (snippetSource) {
                const firstLine = snippetSource.split(/\r?\n/).find((segment) => segment.trim().length > 0);
                if (firstLine) {
                    summary = this.truncate(firstLine.trim(), 120);
                }
            }
            steps.push({
                id: result.stepId,
                title,
                status,
                command,
                placeholder,
                summary,
                path: primaryPath
            });
            if (primaryPath) {
                const fileEntry = ensureFileEntry(primaryPath, placeholder, status);
                const diffCandidate = typeof data?.diff === 'string' ? data.diff.trim() : '';
                if (diffCandidate && diffCandidate !== '__pending__') {
                    fileEntry.diff = data?.diff;
                }
                if (typeof data.diffSummary === 'object') {
                    fileEntry.summary = data.diffSummary ?? null;
                }
                const confidenceCandidate = typeof data.confidence === 'number'
                    ? data.confidence
                    : typeof data.astEdits?.confidence === 'number'
                        ? (data.astEdits?.confidence ?? null)
                        : undefined;
                if (typeof confidenceCandidate === 'number') {
                    fileEntry.confidence = confidenceCandidate;
                }
                if (typeof data.backupPath === 'string' && data.backupPath) {
                    fileEntry.backupPath = data.backupPath ?? null;
                }
                if (typeof data.review === 'string' && (data.review ?? '').trim().length > 0) {
                    fileEntry.review = (data.review ?? '').trim();
                }
                const sample = typeof data.sample === 'string'
                    ? (data.sample ?? '').trim()
                    : undefined;
                if (sample) {
                    contextPathSet.add(primaryPath);
                }
            }
            const extraPaths = Array.isArray(data?.paths) ? data.paths : [];
            for (const entry of extraPaths) {
                if (typeof entry === 'string') {
                    ensureFileEntry(entry, placeholder, status);
                }
            }
        }
        const files = Array.from(filesMap.values()).map((file) => ({
            ...file,
            diff: file.diff ?? null,
            summary: file.summary ?? null,
            confidence: typeof file.confidence === 'number' ? file.confidence : null,
            backupPath: file.backupPath ?? null,
            review: file.review ?? null
        }));
        const diffPreview = files.find((file) => typeof file.diff === 'string' && file.diff.trim().length > 0)?.diff ?? undefined;
        const updatedPaths = files.map((file) => file.path);
        const contextPaths = Array.from(contextPathSet);
        const backupPath = files.find((file) => file.backupPath)?.backupPath ?? null;
        return {
            goal: report.goal,
            planGoal: typeof report.plan?.goal === 'string' ? report.plan.goal : undefined,
            success,
            confidence,
            iterations,
            feedback: report.evaluation?.feedback ?? undefined,
            updatedPaths,
            contextPaths,
            steps,
            files,
            diffPreview,
            backupPath
        };
    }
    formatAgentReport(report) {
        const summary = this.deriveAgentSummary(report);
        const lines = [];
        const confidenceLabel = summary.confidence !== null ? `${(summary.confidence * 100).toFixed(1)}%` : 'n/a';
        const statusLabel = summary.success ? '✅ Success' : '⚠️ Needs follow-up';
        lines.push('**Agent Report**');
        lines.push('');
        lines.push(`Goal: ${summary.goal}`);
        lines.push(`Status: ${statusLabel} (confidence ${confidenceLabel})`);
        lines.push(`Iterations: ${summary.iterations}`);
        if (summary.steps.length > 0) {
            lines.push('');
            lines.push('**Steps**');
            for (const step of summary.steps) {
                const statusIcon = step.status === 'complete' ? '✅' : '⚠️';
                let line = `- ${statusIcon} ${step.title}`;
                if (step.command) {
                    line += ` (command: ${step.command})`;
                }
                if (step.placeholder) {
                    line += ' [placeholder command – no direct code changes]';
                }
                if (step.summary) {
                    line += ` — ${step.summary}`;
                }
                lines.push(line);
            }
        }
        if (summary.updatedPaths.length > 0) {
            lines.push('');
            lines.push('**Files Updated**');
            for (const filePath of summary.updatedPaths) {
                lines.push(`- ${filePath}`);
            }
        }
        if (summary.feedback) {
            lines.push('');
            lines.push(`**Feedback:** ${summary.feedback}`);
        }
        if (summary.contextPaths.length > 0) {
            lines.push('');
            lines.push('**Context Files**');
            summary.contextPaths.forEach((path) => {
                lines.push(`- ${path}`);
            });
        }
        if (summary.diffPreview) {
            lines.push('');
            lines.push('**Code Diff Preview**');
            lines.push('```diff');
            lines.push(this.truncateDiff(summary.diffPreview));
            lines.push('```');
        }
        if (summary.backupPath) {
            lines.push('');
            lines.push(`Backup saved at: ${summary.backupPath}`);
        }
        lines.push('');
        lines.push('Full report saved to `.bandit/agent-report.json`.');
        return lines.join('\n');
    }
    buildAgentSummaryHeadline(report) {
        const confidence = Number.isFinite(report.evaluation?.confidence)
            ? `${(report.evaluation.confidence * 100).toFixed(1)}%`
            : 'n/a';
        const success = report.evaluation?.success ?? false;
        const statusLabel = success ? 'completed successfully' : 'needs follow-up';
        const prefix = success ? '✅' : '⚠️';
        return `${prefix} ${report.goal} — ${statusLabel} (confidence ${confidence}).`;
    }
    buildAgentSummaryPayload(report, summaryMarkdown, agentReply) {
        const info = this.deriveAgentSummary(report);
        return {
            type: 'agent-summary',
            goal: info.goal,
            planGoal: info.planGoal ?? null,
            success: info.success,
            confidence: info.confidence,
            iterations: info.iterations,
            feedback: info.feedback ?? null,
            updatedPaths: info.updatedPaths,
            contextPaths: info.contextPaths,
            steps: info.steps,
            files: info.files,
            diffPreview: info.diffPreview ?? null,
            backupPath: info.backupPath ?? null,
            summary: summaryMarkdown,
            response: agentReply,
            completedAt: report.finishedAt ?? null
        };
    }
    truncate(value, max = 120) {
        if (value.length <= max) {
            return value;
        }
        return `${value.slice(0, max - 1)}…`;
    }
    truncateDiff(diff, maxLines = 200) {
        const lines = diff.split('\n');
        if (lines.length <= maxLines) {
            return diff;
        }
        const head = lines.slice(0, maxLines);
        head.push('... diff truncated ...');
        return head.join('\n');
    }
    isPlaceholderCommand(command) {
        if (!command) {
            return false;
        }
        const normalized = command.trim().toLowerCase();
        if (normalized === '' || normalized === 'noop' || normalized === 'true' || normalized === 'exit 0') {
            return true;
        }
        return normalized.startsWith('echo ') || normalized.includes('echo "') || normalized.includes("echo '") || /sleep\s+\d+/u.test(normalized);
    }
    describeAgentReport(report) {
        const lines = [];
        lines.push(`Goal: ${report.goal}`);
        lines.push(`Iterations: ${report.iterations}`);
        const evaluation = report.evaluation ?? { success: false, feedback: '', confidence: 0 };
        lines.push(`Evaluation: success=${evaluation.success ? 'true' : 'false'}, confidence=${(evaluation.confidence * 100).toFixed(1)}%, feedback=${evaluation.feedback ?? ''}`);
        const planSteps = Array.isArray(report.plan?.steps) ? report.plan.steps : [];
        const lookup = new Map(planSteps.map((step) => [step.id, step]));
        if (Array.isArray(report.results) && report.results.length > 0) {
            lines.push('Results:');
            for (const result of report.results) {
                const step = lookup.get(result.stepId);
                const title = step?.title ?? result.stepId;
                const status = result.ok ? 'ok' : 'failed';
                const command = typeof step?.command === 'string' ? step.command : undefined;
                const placeholder = this.isPlaceholderCommand(command);
                const snippetSource = (result.output ?? '').toString().trim() || (result.error ?? '').toString().trim();
                const snippet = snippetSource ? this.truncate(snippetSource.replace(/\s+/g, ' '), 200) : '';
                const meta = [];
                if (command) {
                    meta.push(`command=${command}`);
                }
                if (placeholder) {
                    meta.push('placeholder=true');
                }
                const metaText = meta.length > 0 ? ` [${meta.join('; ')}]` : '';
                lines.push(`- ${title}: ${status}${metaText}${snippet ? ` (${snippet})` : ''}`);
            }
        }
        const fileReads = (report.results ?? []).map((result) => {
            const data = result.data;
            const sample = typeof data?.sample === 'string' ? data.sample.trim() : undefined;
            const path = typeof data?.path === 'string' ? data.path : undefined;
            if (!sample || !path) {
                return undefined;
            }
            return { path, sample };
        }).filter((entry) => Boolean(entry));
        if (fileReads.length > 0) {
            lines.push('');
            lines.push('File context excerpts:');
            for (const entry of fileReads) {
                lines.push(`- ${entry.path}`);
                lines.push('```');
                lines.push(this.truncate(entry.sample, 360));
                lines.push('```');
            }
        }
        const diffResult = report.results.find((result) => typeof result.data?.diff === 'string');
        if (diffResult) {
            const diffText = diffResult.data.diff ?? '';
            if (diffText.trim().length > 0) {
                lines.push('Diff preview:');
                lines.push(this.truncateDiff(diffText, 80));
            }
        }
        const scriptResult = report.results.find((result) => Array.isArray(result.data?.runs));
        if (scriptResult) {
            const runs = (scriptResult.data.runs ?? [])
                .map((run) => {
                const script = typeof run.script === 'string' ? run.script : 'unknown';
                const ok = run.ok === false ? 'failed' : 'ok';
                return `${script}:${ok}`;
            });
            if (runs.length > 0) {
                lines.push(`Script checks: ${runs.join(', ')}`);
            }
        }
        return lines.join('\n');
    }
    buildAgentCompletionRequest(goal, report, configuration) {
        const providerKind = this.getProviderKind(configuration);
        const model = providerKind === 'ollama'
            ? this.resolveAgentModel(configuration)
            : (configuration.get('model', 'bandit-core-1') ?? 'bandit-core-1');
        const temperature = configuration.get('temperature', 0.2);
        const topP = configuration.get('topP', 1);
        const messages = [
            {
                role: 'system',
                content: 'You are Bandit Stealth, an expert coding assistant operating inside VS Code. Provide a concise, accurate response to the user goal using only information contained in the agent run summary. If steps are marked as placeholders or no concrete changes were made, state that clearly. Never claim that code was modified unless the summary explicitly indicates a real change.'
            },
            {
                role: 'user',
                content: `User goal: ${goal}\n\nAgent report:\n${this.describeAgentReport(report)}\n\nRespond directly to the user goal.`
            }
        ];
        const request = {
            model,
            messages,
            stream: true,
            temperature
        };
        if (typeof topP === 'number' && !Number.isNaN(topP)) {
            request.options = { top_p: topP };
        }
        return request;
    }
    async generateAgentReply(goal, report) {
        const configuration = vscode.workspace.getConfiguration('banditStealth');
        const providerKind = this.getProviderKind(configuration);
        const apiKey = await this.context.secrets.get(API_KEY_SECRET_KEY);
        if (providerKind === 'bandit' && !apiKey) {
            return undefined;
        }
        const ollamaAuth = await Promise.resolve(this.context.secrets.get(OLLAMA_AUTH_SECRET_KEY)).catch(() => undefined);
        const provider = await (0, stealth_core_runtime_1.createProvider)(this.buildProviderSettings(configuration, apiKey ?? '', ollamaAuth));
        const request = this.buildAgentCompletionRequest(goal, report, configuration);
        let response = '';
        try {
            for await (const chunk of provider.chat(request)) {
                const content = chunk?.message?.content ?? '';
                if (content) {
                    response += content;
                }
                if (chunk?.done) {
                    break;
                }
            }
        }
        catch (error) {
            throw error instanceof Error ? error : new Error(String(error));
        }
        const trimmed = response.trim();
        return trimmed.length > 0 ? trimmed : undefined;
    }
    async appendAssistantMessage(content, options) {
        let payload;
        if (options && Object.prototype.hasOwnProperty.call(options, 'payload')) {
            const value = options.payload;
            if (typeof value === 'string') {
                payload = value;
            }
            else if (value !== undefined) {
                try {
                    payload = JSON.stringify(value);
                }
                catch {
                    payload = content;
                }
            }
        }
        const assistantEntry = createConversationEntry('assistant', content, { payload: payload ?? content });
        if (this.historyVisible) {
            this.historyVisible = false;
        }
        await this.updateConversation([...this.conversation, assistantEntry]);
        await this.syncState();
    }
    async evaluateIntentForPrompt(entry, prompt, configuration, providerKind) {
        if (providerKind !== 'bandit') {
            await this.attachIntentToMessage(entry.id, undefined);
            await this.setIntentInsight(undefined);
            return;
        }
        try {
            await this.setStatusMessage('Detecting intent…');
            const insight = await this.interpretIntent(prompt, configuration, providerKind);
            if (insight) {
                const enriched = { ...insight, summary: this.summarizeIntent(insight) };
                await this.attachIntentToMessage(entry.id, enriched);
                await this.recordIntentMemory(enriched);
                await this.setIntentInsight(enriched);
                await this.setStatusMessage(`Intent detected: ${enriched.summary}`);
            }
            else {
                await this.attachIntentToMessage(entry.id, undefined);
                await this.setIntentInsight(undefined);
                await this.setStatusMessage('No specific intent detected');
            }
        }
        catch (error) {
            console.warn('Intent detection failed', error);
            await this.attachIntentToMessage(entry.id, undefined);
            await this.setIntentInsight(undefined);
            await this.setStatusMessage('Intent unavailable');
        }
    }
    async performCompletion(apiKey, configuration) {
        // Intercept slash commands before they reach the agent so `/rewind`
        // and similar meta-commands don't get sent to the model as a user
        // prompt (which would confuse small models into echoing them back).
        const lastUserMessage = [...this.conversation].reverse().find(e => e.role === 'user')?.content ?? '';
        const trimmed = lastUserMessage.trim();
        if (trimmed.startsWith('/rewind')) {
            await this.handleRewindCommand(trimmed);
            return;
        }
        // Delegate to tool use loop when the feature is enabled.
        if (configuration.get('enableToolUse', true)) {
            await this.performToolUseCompletion(apiKey, configuration, lastUserMessage);
            return;
        }
        this.cancelActiveStream();
        const providerKind = this.getProviderKind(configuration);
        const providerLabel = this.describeProvider(providerKind);
        await this.setBusy(true, `Waiting for ${providerLabel}…`);
        const assistantEntry = createConversationEntry('assistant', '', { payload: '' });
        let assistantAdded = false;
        try {
            const ollamaAuth = await Promise.resolve(this.context.secrets.get(OLLAMA_AUTH_SECRET_KEY)).catch(() => undefined);
            const provider = await (0, stealth_core_runtime_1.createProvider)(this.buildProviderSettings(configuration, apiKey, ollamaAuth));
            const lastUserMessage = [...this.conversation].reverse().find(e => e.role === 'user')?.content ?? '';
            const contextResult = await this.buildContextBlock(lastUserMessage, configuration).catch(() => undefined);
            const request = this.buildChatRequest(configuration, contextResult?.formatted);
            await this.updateConversation([...this.conversation, assistantEntry], { persist: false });
            assistantAdded = true;
            await this.syncState();
            const iterator = provider.chat(request)[Symbol.asyncIterator]();
            this.activeStream = iterator;
            let streamStarted = false;
            let completedNaturally = false;
            try {
                for (;;) {
                    const { value, done } = await iterator.next();
                    if (done) {
                        completedNaturally = true;
                        break;
                    }
                    const chunk = value;
                    if (!chunk) {
                        continue;
                    }
                    if (!streamStarted && !chunk.done) {
                        streamStarted = true;
                        void this.setStatusMessage(`Streaming ${providerLabel} response…`);
                    }
                    const content = chunk.message?.content ?? '';
                    if (content) {
                        assistantEntry.content += content;
                        assistantEntry.payload = assistantEntry.content;
                        assistantEntry.timestamp = Date.now();
                        void this.syncState();
                    }
                    if (chunk.done) {
                        completedNaturally = true;
                        break;
                    }
                }
            }
            catch (error) {
                if (error instanceof Error && error.name === 'AbortError') {
                    completedNaturally = true;
                }
                else {
                    throw error;
                }
            }
            finally {
                this.activeStream = undefined;
                if (!completedNaturally && typeof iterator.return === 'function') {
                    try {
                        await iterator.return();
                    }
                    catch {
                        // ignore iterator cleanup errors
                    }
                }
            }
            assistantEntry.content = assistantEntry.content.trim();
            assistantEntry.payload = assistantEntry.content;
            if (!assistantEntry.content) {
                this.conversation = this.conversation.filter((entry) => entry.id !== assistantEntry.id);
            }
            await this.updateConversation(this.conversation);
            await this.syncState();
        }
        catch (error) {
            if (assistantAdded && !assistantEntry.content.trim()) {
                this.conversation = this.conversation.filter((entry) => entry.id !== assistantEntry.id);
            }
            const message = error instanceof Error ? error.message : 'Unknown issue.';
            const friendlyProvider = this.describeProvider(this.getProviderKind(configuration));
            this.postMessage({ type: 'error', message: `${friendlyProvider} error: ${message}` });
            void vscode.window.showErrorMessage(`${friendlyProvider} error: ${message}`);
            if (assistantAdded) {
                await this.updateConversation(this.conversation);
                await this.syncState();
            }
        }
        finally {
            this.cancelActiveStream();
            await this.setBusy(false);
        }
    }
    /**
     * Handle `/rewind` slash command in the composer. No args lists the
     * most recent checkpoints; `/rewind <id>` or `/rewind last` applies
     * one. Result is posted as a synthetic assistant entry so it lives
     * in the conversation history alongside the diff cards that created
     * those checkpoints.
     */
    async handleRewindCommand(raw) {
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath ?? process.cwd();
        const store = new host_kit_1.CheckpointStore({ workspaceRoot });
        const arg = raw.slice('/rewind'.length).trim();
        const systemEntry = createConversationEntry('assistant', '', { payload: '' });
        this.conversation.push(systemEntry);
        const render = async (content) => {
            systemEntry.content = content;
            systemEntry.payload = content;
            systemEntry.timestamp = Date.now();
            await this.updateConversation(this.conversation);
            await this.syncState();
        };
        try {
            if (!arg) {
                const list = await store.list(10);
                if (list.length === 0) {
                    await render('_No checkpoints yet — rewind is available after the agent makes an edit._');
                    return;
                }
                const rows = list.map((e, i) => {
                    const tag = i === 0 ? '**most recent**' : '';
                    return `- \`${e.id}\` · ${e.tool} \`${e.relPath}\` · **+${e.plus} −${e.minus}** ${tag}`;
                });
                await render([
                    '**Recent checkpoints** — `/rewind <id>` or `/rewind last` to restore:',
                    '',
                    ...rows
                ].join('\n'));
                return;
            }
            let targetId = arg;
            if (arg === 'last' || arg === '--last') {
                const list = await store.list(1);
                if (list.length === 0) {
                    await render('_No checkpoints to rewind to._');
                    return;
                }
                targetId = list[0].id;
            }
            const entry = await store.rewind(targetId);
            if (!entry) {
                await render(`_Checkpoint \`${targetId}\` not found. Run \`/rewind\` to list available ids._`);
                return;
            }
            const action = entry.isNewFile ? 'deleted (was new file)' : 'restored to pre-edit state';
            await render([
                `**↶ rewound** \`${entry.id}\` — ${entry.relPath} ${action}.`,
                '',
                `_Turn \`${entry.turnId}\` · iteration ${entry.iteration} · ${entry.tool}_`
            ].join('\n'));
        }
        catch (err) {
            const msg = err instanceof Error ? err.message : String(err);
            await render(`_Rewind failed: ${msg}_`);
        }
    }
    /**
     * Ask-mode completion backed by the text-based tool use loop.
     * Active when `banditStealth.enableToolUse` is true.
     *
     * The loop injects XML tool definitions into the system prompt, executes
     * <tool_call> blocks emitted by the model, and returns the final answer
     * once no more tool calls appear.
     */
    async performToolUseCompletion(apiKey, configuration, userGoal) {
        this.cancelActiveStream();
        const providerKind = this.getProviderKind(configuration);
        const providerLabel = this.describeProvider(providerKind);
        await this.setBusy(true, `Tool agent starting…`);
        const assistantEntry = createConversationEntry('assistant', '', { payload: '' });
        let assistantAdded = false;
        // Hoisted so the catch block can clear the thinking / tool-call-gen
        // markers when an error (e.g. Ollama 404) interrupts mid-loop. The
        // real implementations are assigned once the try-block sets up the
        // interval handlers below.
        let stopThinking = () => { };
        let stopToolCallGen = () => { };
        try {
            const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
            if (!workspaceRoot) {
                throw new Error('Tool use requires an open workspace folder.');
            }
            const ollamaAuth = await Promise.resolve(this.context.secrets.get(OLLAMA_AUTH_SECRET_KEY)).catch(() => undefined);
            const providerSettings = this.buildProviderSettings(configuration, apiKey, ollamaAuth);
            const model = providerKind === 'ollama'
                ? this.resolveAgentModel(configuration)
                : configuration.get('model', 'bandit-core-1') ?? 'bandit-core-1';
            const temperature = configuration.get('temperature', 0.2);
            const toolCtx = new nodeToolContext_1.NodeToolExecutionContext(workspaceRoot, (0, agent_core_1.createDefaultLanguageAdapters)());
            // Resolve active skills (built-in + workspace custom) and build the tool registry.
            const skillRegistry = (0, agent_core_1.createDefaultSkillRegistry)();
            await (0, agent_core_1.registerWorkspaceSkills)(skillRegistry, (pattern, cwd) => toolCtx.listFiles(pattern, cwd), (absPath) => toolCtx.readFile(absPath), workspaceRoot).catch(() => 0);
            // Open a per-turn transcript log so we always have forensics when the
            // agent claims something it didn't actually do. Writes to
            // .bandit/turns/turn-<timestamp>.jsonl in the workspace.
            const turnLog = await (0, host_kit_1.openTurnLog)(workspaceRoot).catch(() => null);
            await turnLog?.append({ type: 'user-prompt', prompt: (0, host_kit_1.previewText)(userGoal) });
            // Derive a short turn id from the log filename so checkpoints
            // and turn logs line up on disk for forensic replay.
            const turnId = turnLog
                ? (path.basename(turnLog.filePath).replace(/\.jsonl$/, ''))
                : `turn-${Date.now()}`;
            const checkpointStore = new host_kit_1.CheckpointStore({ workspaceRoot });
            const activeSkills = skillRegistry.resolveActiveSkills(userGoal);
            const { registry, toolToSkill } = skillRegistry.buildToolRegistryWithMap(activeSkills);
            const skillNameById = new Map(activeSkills.map((s) => [s.id, s.name]));
            let lastAnnouncedSkillId = null;
            // Host-kit additions: project memory (BANDIT.md / CLAUDE.md), hooks, extra tools.
            const memoryBundle = await (0, host_kit_1.loadMemory)(workspaceRoot).catch(() => ({ content: '', sources: [] }));
            const hookSettings = await (0, host_kit_1.loadHookSettings)(workspaceRoot).catch(() => ({ hooks: {} }));
            const todoStore = new host_kit_1.TodoStore();
            registry.register((0, host_kit_1.buildTodoWriteTool)(todoStore));
            registry.register((0, host_kit_1.buildWebFetchTool)());
            const toolStartedAt = new Map();
            // Tracks pre-write / post-write content per path so we can emit a
            // "+X -Y" diff summary once the write completes successfully.
            const pendingWriteBefore = new Map();
            const pendingWriteAfter = new Map();
            // Map from tool name → most-recently-emitted timeline-row id for
            // that tool. Set in tool_execute, looked up in tool_result so we
            // can flip the row's status from running → done/error and
            // back-fill its duration. Parallel calls to the same tool land
            // and complete in order, so a single-slot-per-name is sufficient.
            const pendingTimelineIds = new Map();
            // Latest run_command invocation — captured at tool_execute so the
            // IN/OUT card can pair command + output when tool_result fires.
            let pendingRunCommand = null;
            // Flush all pending diff cards — called on iteration boundaries
            // and at turn end. Parallel edits to the same file produce ONE
            // cumulative card (before = iteration-start disk state, after =
            // current disk state). Parallel edits to different files each
            // get their own card. Run synchronously to avoid racing with the
            // next iteration's content truncation.
            const flushPendingEditDiffs = () => {
                if (pendingWriteBefore.size === 0)
                    return;
                for (const [absPath, before] of pendingWriteBefore.entries()) {
                    const pendingAfter = pendingWriteAfter.get(absPath);
                    // For write_file we already know the full after content; for
                    // apply_edit we left a placeholder and read fresh from disk.
                    const after = (pendingAfter && pendingAfter.length > 0) ? pendingAfter : readFileSafe(absPath);
                    if (before === after)
                        continue;
                    const rel = path.relative(workspaceRoot, absPath) || absPath;
                    const { plus, minus } = lineDiffCounts(before, after);
                    const isNew = before === '';
                    const header = isNew
                        ? `\n\n**✦ created** \`${rel}\` · **+${after.split('\n').length} lines**\n`
                        : `\n\n**✎ edited** \`${rel}\` · **+${plus} −${minus}**\n`;
                    const preview = buildCompactDiffBlock(before, after, 60, { relPath: rel, plus, minus });
                    assistantEntry.content += header + preview;
                    assistantEntry.payload = assistantEntry.content;
                    // Fire-and-forget checkpoint — best effort.
                    const tool = (pendingAfter && pendingAfter.length > 0) ? 'write_file' : 'apply_edit';
                    void checkpointStore.create({
                        turnId,
                        tool,
                        absolutePath: absPath,
                        before,
                        after,
                        iteration: currentIteration + 1
                    }).catch(() => undefined);
                }
                pendingWriteBefore.clear();
                pendingWriteAfter.clear();
                void this.syncState();
            };
            let subagentBuffer = null;
            // Cycling verb set for the "thinking" indicator. The CLI shows this as
            // a live terminal line; we render the same affordance inline in the
            // assistant message so the extension feels equally alive. A trailing
            // "— _⟳ pondering…_" marker at the end of assistantEntry.content gets
            // swapped every 2.5s, and is stripped whenever a tool call fires or
            // real streamed output arrives.
            const THINKING_VERBS = ['pondering', 'inspecting', 'wiring', 'untangling', 'distilling', 'scheming', 'plotting', 'calibrating', 'rummaging', 'stitching'];
            // Unified status marker. Matches ANY `_⟳ ... _` line anywhere in the
            // content — no $ anchor — so the strip works regardless of where
            // the marker sits relative to streamed content. One marker only:
            // the two previous mechanisms (thinking verb + generating tool
            // call) stacked into separate lines because their $-anchored
            // regexes couldn't find the "old" marker when newer content had
            // been appended between ticks. Now both tickers share one state
            // line at the tail of the content — stripped universally before
            // every re-append.
            // Delimiter is backticks (code span), not emphasis. We went _..._
            // → *...* → and both failed: markdown-it's underscore rule blocked
            // closing `s_`, and the asterisk variant STILL didn't italicize
            // because markdown-it's flanking logic treats the `⟳` symbol as
            // punctuation and refuses `*⟳ ... 23s*` as emphasis (observed
            // 2026-04-23 — users saw literal `*⟳` in the UI).
            // Backticks have NO flanking rules. `` `⟳ text` `` always renders
            // as `<code>⟳ text</code>`. The webview regex upgrades that to
            // the animated pill; the CLI renders it as plain inline code.
            const STATUS_MARKER_RE = /\n*`⟳ [^\n`]+`\s*(?=\n|$)/g;
            let thinkingInterval = null;
            let toolCallGenInterval = null;
            let toolCallGenBytes = 0;
            let toolCallGenStartedAt = 0;
            let currentThinkingVerb = null;
            let toolCallGenActive = false;
            const buildStatusText = () => {
                // Compose a single status line from whichever indicators are
                // active. Priority: tool-call-gen (more specific, timings
                // matter for "am I hung?") overlays the thinking verb.
                if (toolCallGenActive) {
                    const elapsedSec = Math.max(0, Math.floor((Date.now() - toolCallGenStartedAt) / 1000));
                    let signal = `${elapsedSec}s`;
                    if (elapsedSec >= 20 && toolCallGenBytes >= 2048) {
                        const kb = (toolCallGenBytes / 1024).toFixed(1);
                        signal = `${elapsedSec}s · ${kb}kb`;
                    }
                    return `generating tool call · ${signal}`;
                }
                if (currentThinkingVerb) {
                    return `${currentThinkingVerb}…`;
                }
                return '';
            };
            const renderStatus = () => {
                const stripped = assistantEntry.content.replace(STATUS_MARKER_RE, '');
                const text = buildStatusText();
                if (!text) {
                    if (stripped !== assistantEntry.content) {
                        assistantEntry.content = stripped;
                        assistantEntry.payload = assistantEntry.content;
                        void this.syncState();
                    }
                    return;
                }
                const marker = `\n\n\`⟳ ${text}\``;
                assistantEntry.content = stripped + marker;
                assistantEntry.payload = assistantEntry.content;
                void this.syncState();
            };
            const startThinking = () => {
                if (thinkingInterval)
                    return;
                const tick = () => {
                    currentThinkingVerb = THINKING_VERBS[Math.floor(Math.random() * THINKING_VERBS.length)];
                    void this.setStatusMessage(`${providerLabel} ${currentThinkingVerb}…`);
                    renderStatus();
                };
                tick();
                thinkingInterval = setInterval(tick, 2500);
            };
            stopThinking = () => {
                if (thinkingInterval) {
                    clearInterval(thinkingInterval);
                    thinkingInterval = null;
                }
                currentThinkingVerb = null;
                renderStatus();
            };
            // Secondary indicator for the "generating tool call" phase — the
            // model has started streaming tokens but the chunks are being
            // ignored (they're tool_call JSON that will execute once complete).
            // Without this marker the user sees a silent void for 10-60 seconds
            // while a long content payload streams. We show ELAPSED SECONDS as
            // the primary signal; bytes as secondary signal once generation
            // is clearly long-running.
            const startToolCallGen = () => {
                if (toolCallGenInterval)
                    return;
                toolCallGenBytes = 0;
                toolCallGenStartedAt = Date.now();
                toolCallGenActive = true;
                renderStatus();
                // 1s cadence — matches the displayed second-precision so the
                // marker updates once per visible tick, no redundant renders.
                toolCallGenInterval = setInterval(renderStatus, 1000);
            };
            stopToolCallGen = () => {
                if (toolCallGenInterval) {
                    clearInterval(toolCallGenInterval);
                    toolCallGenInterval = null;
                }
                toolCallGenActive = false;
                renderStatus();
            };
            // Ring buffer for repeat-tool-call detection. A repeat is the same
            // tool name with the same primary param (path/cmd/pattern/query)
            // appearing within the last N calls. We annotate repeats with a
            // distinct marker so plan churn and redundant probes stand out
            // visually rather than stacking identical lines.
            const recentToolCallDisplays = [];
            const REPEAT_WINDOW = 6;
            // Pull images from the most recent user entry in the conversation
            // so the tool-use loop can forward them to the provider on the
            // FIRST iteration. Without this, images attached to the user's
            // prompt never reached the model — the tool-use adapter was
            // stripping `content` + `role` only and dropping `images`. Only
            // send on the first chat() call of the turn; subsequent
            // iterations are tool-result follow-ups with no new image.
            const allowInlineImages = this.canUseInlineImages(configuration, model);
            const lastUserEntryForImages = [...this.conversation]
                .reverse()
                .find((entry) => entry.role === 'user');
            const turnImages = allowInlineImages && lastUserEntryForImages?.images
                ? lastUserEntryForImages.images
                    .map((image) => this.extractImagePayload(image))
                    .filter((image) => image.length > 0)
                : [];
            let imagesAlreadySent = turnImages.length === 0;
            // Resolve user's thinking-mode preference. "auto" → no override;
            // "on" / "off" → force that state via request.think. Read once
            // per turn so mid-session toggles of the setting take effect on
            // the NEXT prompt without rebuilding providers.
            const thinkingModePref = vscode.workspace
                .getConfiguration('banditStealth')
                .get('thinkingMode', 'auto');
            const thinkOverride = thinkingModePref === 'on' ? true :
                thinkingModePref === 'off' ? false :
                    undefined;
            // Adapt provider.chat() → ChatFn (ToolLoopMessage[] → AsyncIterable<string>)
            const chat = async function* (messages, tools) {
                const request = {
                    model,
                    messages: messages.map(m => ({ role: m.role, content: m.content })),
                    stream: true,
                    temperature
                };
                if (thinkOverride !== undefined) {
                    request.think = thinkOverride;
                }
                if (!imagesAlreadySent && turnImages.length > 0) {
                    request.images = turnImages;
                    imagesAlreadySent = true;
                }
                if (tools && tools.length > 0) {
                    // ToolUseLoop is in nativeTools mode — forward the schemas to
                    // Ollama so the model's chat template serializes them in its
                    // compact native format instead of our XML block.
                    request.tools = tools;
                }
                const provider = await (0, stealth_core_runtime_1.createProvider)(providerSettings);
                for await (const chunk of provider.chat(request)) {
                    // Stream chain-of-thought reasoning as a `bandit-reasoning`
                    // fence so the webview renders it in a collapsed disclosure
                    // block. Emitted before content so the reasoning lands above
                    // the answer in transcript order. If reasoning arrives in
                    // multiple chunks, we append segments into the open block.
                    const reasoning = chunk.message?.thinking;
                    if (reasoning) {
                        yield `\n\`\`\`bandit-reasoning\n${reasoning}\n\`\`\`\n`;
                    }
                    const text = chunk.message?.content ?? '';
                    if (text) {
                        yield text;
                    }
                    if (chunk.done) {
                        break;
                    }
                }
            };
            // Shared gate applied to every tool call (main loop + Task subagents).
            // Order: hooks first (scripted guardrails), then permission policy
            // (user-facing "allow this write?" modal). Either can abort the call.
            const permissionStore = this.permissionStore;
            // Turn-local auto-grant so parallel edits to the SAME file only
            // prompt once. Without this, a model that emits two apply_edit
            // calls in one iteration (common when it's patching two regions
            // of the same file) shows the user two back-to-back permission
            // cards for identical `tool + path` — which reads as a duplicate
            // prompt bug. Scope is this turn only; cleared when the loop ends.
            const turnApprovedKeys = new Set();
            // Inflight permission promises keyed by turnKey. If two tool calls
            // fire in the same iteration for the same file, the second one
            // awaits the first's card instead of spawning its own.
            const inflightPermissions = new Map();
            const buildTurnKey = (toolName, primaryParam) => primaryParam ? `${toolName}:${primaryParam}` : toolName;
            const beforeToolExecute = async ({ name, params }) => {
                const primary = params.path ?? params.pattern ?? params.cmd ?? params.url ?? params.query ?? '';
                // 1. Shell hooks — project-authored guardrails.
                const hookResults = await (0, host_kit_1.runHooks)('PreToolUse', hookSettings, { toolName: name, primary }, workspaceRoot);
                const blocker = hookResults.find(r => r.exitCode !== 0);
                if (blocker) {
                    const reason = (blocker.stderr.trim() || blocker.stdout.trim()) || `PreToolUse hook exited ${blocker.exitCode}`;
                    return { allow: false, reason };
                }
                // 2. Permission policy — merged workspace config + session grants.
                const merged = (0, host_kit_1.mergePolicies)({
                    allow: hookSettings.permissions?.allow ?? [],
                    deny: hookSettings.permissions?.deny ?? [],
                    ask: hookSettings.permissions?.ask ?? []
                }, permissionStore.toPolicy());
                const decision = (0, host_kit_1.evaluatePermission)(name, primary, merged);
                if (decision === 'deny') {
                    return { allow: false, reason: `denied by permission policy (${name}${primary ? `:${primary}` : ''})` };
                }
                if (decision === 'ask') {
                    // Turn-local auto-grant: if the user already approved this
                    // exact (tool, primary) within the current turn, skip the card
                    // so parallel multi-region edits to one file don't stack
                    // duplicate prompts.
                    const turnKey = buildTurnKey(name, primary);
                    if (turnApprovedKeys.has(turnKey)) {
                        toolStartedAt.set(name, Date.now());
                        return { allow: true };
                    }
                    // Edit-automatically toggle: bypass the card for write_file and
                    // apply_edit when the user has opted in. run_command is never
                    // bypassed — shell commands always require an explicit choice.
                    // Fetched fresh every call so flipping the toggle mid-run takes
                    // effect on the next tool use without restarting the loop.
                    const autoApproveEdits = vscode.workspace
                        .getConfiguration('banditStealth')
                        .get('agent.autoApproveEdits', false) ?? false;
                    if (autoApproveEdits && (name === 'write_file' || name === 'apply_edit')) {
                        toolStartedAt.set(name, Date.now());
                        return { allow: true };
                    }
                    const description = describeToolForPrompt(name, primary, params);
                    // For write_file, include a short unified-diff preview in the card
                    // so the user sees exactly what's changing before approving.
                    let bodyPreview;
                    let warning;
                    let diffStats;
                    if (name === 'write_file' && params.path) {
                        const absPath = path.isAbsolute(params.path) ? params.path : path.resolve(workspaceRoot, params.path);
                        const before = readFileSafe(absPath);
                        const after = params.content ?? '';
                        const fileExists = before !== '';
                        if (before !== after) {
                            bodyPreview = buildCompactDiffBlock(before, after, 8);
                            const lines = bodyPreview.split('\n');
                            let added = 0;
                            let removed = 0;
                            for (const l of lines) {
                                if (l.startsWith('+') && !l.startsWith('+++'))
                                    added++;
                                else if (l.startsWith('-') && !l.startsWith('---'))
                                    removed++;
                            }
                            diffStats = { added, removed };
                        }
                        // If write_file is about to CREATE a new file AND the user's
                        // prompt implied editing an existing one (update/fix/change/
                        // refactor + no explicit "create" keyword), surface a warning
                        // on the card. Caught the pburg-bowl regression where the
                        // model invented `src/scoring/scoring.ts` instead of reading
                        // the search result that pointed at `src/utils/scoring.ts`.
                        if (!fileExists) {
                            const promptText = userGoal.toLowerCase();
                            const editIntent = /\b(update|edit|modify|change|fix|refactor|rewrite|rename|replace)\b/.test(promptText);
                            const createIntent = /\b(create|new|add|generate|scaffold|bootstrap)\b/.test(promptText);
                            if (editIntent && !createIntent) {
                                warning = `This would CREATE a new file at \`${params.path}\`. Your prompt suggested editing an existing file — if that wasn't your intent, click "Deny with notes…" and point the agent at the correct path (e.g. try search_code for the right location).`;
                            }
                        }
                    }
                    // Share an inflight card with any sibling call that hit this
                    // gate at the same time for the same (tool, primary). First
                    // caller creates the promise, the rest await it.
                    let permissionPromise = inflightPermissions.get(turnKey);
                    if (!permissionPromise) {
                        permissionPromise = this.requestPermissionInChat({
                            tool: name,
                            primary,
                            description,
                            bodyPreview,
                            warning,
                            diffStats,
                            assistantEntry
                        });
                        inflightPermissions.set(turnKey, permissionPromise);
                        void permissionPromise.finally(() => inflightPermissions.delete(turnKey));
                    }
                    const picked = await permissionPromise;
                    if (picked.choice === 'once') {
                        // Remember for the remainder of this turn only — covers the
                        // common case where the model emits two apply_edits to the
                        // same file in one iteration.
                        turnApprovedKeys.add(turnKey);
                    }
                    else if (picked.choice === 'session') {
                        permissionStore.grant(name, primary);
                        turnApprovedKeys.add(turnKey);
                    }
                    else if (picked.choice === 'save') {
                        permissionStore.grant(name, primary);
                        turnApprovedKeys.add(turnKey);
                        const entry = primary ? `${name}:${primary}` : name;
                        void (0, host_kit_1.persistAllowEntry)(workspaceRoot, entry).catch(() => undefined);
                    }
                    else {
                        // 'deny' — abort. When the user supplied follow-up notes,
                        // surface them in the denial reason so the model can read the
                        // correction on its next turn and adjust rather than just
                        // seeing "blocked."
                        const target = primary ? `${name} ${primary}` : name;
                        const reason = picked.notes
                            ? `User denied \`${target}\` and asked you to revise your approach: "${picked.notes}". Do not retry this tool call with the same arguments — adjust your plan based on the user's guidance.`
                            : `User denied \`${target}\`. Do not retry this tool call with the same arguments.`;
                        return { allow: false, reason };
                    }
                }
                toolStartedAt.set(name, Date.now());
                return { allow: true };
            };
            // Register the Task tool so the model can delegate scoped work to a subagent.
            registry.register((0, host_kit_1.buildTaskTool)({
                chat,
                parentRegistry: registry,
                ctx: toolCtx,
                beforeToolExecute,
                onEvent: (type, payload) => {
                    if (type === 'task:start') {
                        const p = payload;
                        subagentBuffer = { goal: p?.goal ?? '', tools: [] };
                    }
                    else if (type === 'subagent:tool_loop:tool_execute') {
                        const p = payload;
                        if (subagentBuffer) {
                            const primaryRaw = p?.params?.path ?? p?.params?.pattern ?? p?.params?.cmd ?? p?.params?.url ?? p?.params?.query ?? '';
                            const primary = compactToolDisplayParam(primaryRaw, workspaceRoot);
                            subagentBuffer.tools.push({ name: p?.name ?? '', primary });
                        }
                    }
                    else if (type === 'subagent:tool_loop:tool_result') {
                        const p = payload;
                        if (subagentBuffer && p?.isError) {
                            const last = subagentBuffer.tools[subagentBuffer.tools.length - 1];
                            if (last && last.name === p.name)
                                last.isError = true;
                        }
                    }
                    else if (type === 'task:done') {
                        const p = payload;
                        if (subagentBuffer) {
                            subagentBuffer.iterations = p?.iterations ?? 0;
                            subagentBuffer.hitLimit = !!p?.hitLimit;
                        }
                    }
                    else if (type === 'task:error') {
                        if (subagentBuffer) {
                            subagentBuffer.hitLimit = false;
                            subagentBuffer.iterations = 0;
                        }
                    }
                }
            }));
            const contextResult = await this.buildContextBlock(userGoal, configuration).catch(() => undefined);
            const baseSystemPrompt = this.buildSystemPrompt(providerKind, configuration, contextResult?.formatted, model, userGoal);
            // Append active skill descriptions + project memory + operational hints.
            const skillInstructions = activeSkills
                .filter((s) => s.instructions)
                .map((s) => `### ${s.name}\n${s.instructions}`)
                .join('\n\n');
            const memoryBlock = memoryBundle.content
                ? `\n\n## Project Memory\n\n${memoryBundle.content}`
                : '';
            // Operational hints: nudges the model to use todo_write for multi-step
            // work so the user sees a visible plan in the chat. Also teaches the
            // skill manifest schema so "make a skill" requests don't produce
            // shell scripts or invented JSON shapes.
            const operationalHints = [
                '',
                '## Working Style',
                '- For multi-step tasks, call `todo_write` first with a JSON array of steps so the user sees a plan. Update items as you finish each step.',
                '- Before writing a file you have not read, read it first.',
                '- **Editing existing files: prefer `apply_edit` over `write_file`.** `apply_edit` does a targeted find/replace and cannot accidentally rewrite the whole file — crucial when the user asks for a small change ("add a comment", "fix this line"). Use `write_file` only to CREATE a new file or when replacing the majority of an existing one.',
                '- `apply_edit` requires `find` to match verbatim (whitespace included). Copy the text from a recent `read_file` result; do not reconstruct it from memory.',
                '- When running `git_*` tools against a repo outside the current workspace, pass `repo_path` (e.g. `git_status(repo_path="/Users/me/projects/other-repo")`).',
                '- After editing code, suggest a command the user can run to verify (tests, build, lint).',
                '',
                '## Authoring skills (when the user asks "make a skill" / "create a skill")',
                'A skill is a context package, not a tool plugin. You already have `run_command`, `read_file`, `write_file`, `git_*` — a skill\'s job is to tell you WHEN to reach for them and WHICH flags/patterns to use. Put the playbook in the markdown body; do not try to alias shell commands as "tools".',
                '',
                'Skills live at `.bandit/skills/<name>.md` as markdown with YAML frontmatter (`.bandit/skills/<name>/SKILL.md` also works when you need to bundle scripts). The legacy `.bandit/skills/*.json` schema still loads, but is deprecated — the nested-escaping rules made model-authored JSON skills unreliable.',
                '',
                'Use THIS shape when the user asks for a skill:',
                '',
                '```markdown',
                '---',
                'id: github',
                'name: GitHub CLI',
                'description: Use when the user mentions GitHub — PRs, issues, commits',
                'activation: auto',
                'triggers: [gh, github, pr, "pull request"]',
                '---',
                '',
                '# GitHub CLI',
                '',
                'When the user asks about GitHub work, use `run_command` with `gh`:',
                '',
                '**Pull requests**',
                '- `gh pr create --title "<t>" --body "<b>"` — open a PR',
                '- `gh pr list` / `gh pr view <n>` / `gh pr checkout <n>`',
                '',
                '**Issues** — `gh issue list`, `gh issue create --title "<t>" --body "<b>"`.',
                '',
                'Suggest `gh auth status` and stop if auth errors appear.',
                '```',
                '',
                'Rules:',
                '- `id` is required, short, kebab-case.',
                '- `activation`: `always` | `auto` (trigger-gated) | `on-demand`.',
                '- `triggers` are simple substrings (not regex). Word boundaries are applied automatically. Use `triggerPatterns: [...]` only if you need a real regex.',
                '- The markdown body IS the skill instructions — write it as a playbook the agent can follow verbatim.',
                '- DO NOT emit a `tools[]` array. The agent already has tools; you are giving it guidance.'
            ].join('\n');
            const systemPrompt = skillInstructions
                ? `${baseSystemPrompt}${memoryBlock}${operationalHints}\n\n## Skill Instructions\n\n${skillInstructions}`
                : `${baseSystemPrompt}${memoryBlock}${operationalHints}`;
            await this.updateConversation([...this.conversation, assistantEntry], { persist: false });
            assistantAdded = true;
            await this.syncState();
            const streamedCharsByIteration = new Map();
            const iterationsWithToolCalls = new Set();
            let currentIteration = 0;
            let currentIterationStartLength = 0;
            let ignoreIterationChunks = false;
            const modelCaps = (0, stealth_core_runtime_1.getModelCapabilities)(model);
            // Raised defaults 2026-04-22: Gemma-class models don't parallelize
            // tool calls (supportsToolCalling=false, so they serialize one
            // apply_edit per iteration) and were consistently hitting the
            // previous 8-iteration cap mid-task on real "document N methods"
            // requests. Large frontier models still finish in 3-5 iterations
            // by parallelizing; the extra headroom is dead weight for them
            // and a genuine unblock for the 12B/26B class.
            const defaultMaxIterations = modelCaps.tier === 'large' ? 20 : modelCaps.tier === 'medium' ? 20 : 12;
            const maxIterations = configuration.get('toolUse.maxIterations', defaultMaxIterations);
            const loop = (0, agent_core_1.createToolUseLoop)(registry, toolCtx, {
                maxIterations,
                beforeToolExecute,
                emitEvent: async (type, payload) => {
                    if (type === 'tool_loop:llm_start') {
                        currentIteration = this.getToolLoopIteration(payload, currentIteration);
                        currentIterationStartLength = assistantEntry.content.length;
                        ignoreIterationChunks = false;
                        streamedCharsByIteration.set(currentIteration, 0);
                        startThinking();
                        return;
                    }
                    if (type === 'tool_loop:llm_chunk') {
                        const iteration = this.getToolLoopIteration(payload, currentIteration);
                        if (iteration !== currentIteration) {
                            // New iteration begins — flush any pending diff cards from
                            // the iteration that just completed. This is the right
                            // time because all tool_results from the prior iteration
                            // have already fired (events are sequential, emitEvent
                            // is awaited), and the disk state reflects every edit.
                            flushPendingEditDiffs();
                            currentIteration = iteration;
                            currentIterationStartLength = assistantEntry.content.length;
                            ignoreIterationChunks = false;
                            streamedCharsByIteration.set(currentIteration, 0);
                        }
                        if (ignoreIterationChunks) {
                            // Still consuming tool_call chunks silently. Bump the
                            // bytes counter so the generating-tool-call indicator
                            // reflects progress on its next tick.
                            const chunkLen = typeof payload?.chunk === 'string'
                                ? payload.chunk.length
                                : 0;
                            toolCallGenBytes += chunkLen;
                            return;
                        }
                        const chunkText = typeof payload?.chunk === 'string'
                            ? payload.chunk
                            : '';
                        if (!chunkText) {
                            return;
                        }
                        // Real tokens are arriving — the thinking verb marker must go
                        // before we append, otherwise "_⟳ pondering…_" ends up mid-text.
                        stopThinking();
                        // On a non-initial iteration (model has already called at
                        // least one tool), suppress LLM prose by default. Small
                        // local models (gemma3:12b, bandit-core:12b) stream
                        // "Okay, I've read the file. Now I'll..." preambles + ```json
                        // plan scratchpads between tool calls — all of which leaks
                        // into the chat history when the native tool-call path is
                        // used (no `<tool_call>` envelope in the stream to trigger
                        // the legacy truncator). We kick into tool-call-gen mode
                        // immediately and let `tool_loop:tool_calls` clear the
                        // accumulated noise. Iteration 0 is left unmuted so a pure
                        // Q&A turn (no tools) still streams visibly.
                        const suppressStreamPreamble = currentIteration > 0 || iterationsWithToolCalls.size > 0;
                        if (suppressStreamPreamble) {
                            ignoreIterationChunks = true;
                            toolCallGenBytes += chunkText.length;
                            if (toolCallGenBytes > 0) {
                                startToolCallGen();
                            }
                            return;
                        }
                        assistantEntry.content += chunkText;
                        assistantEntry.payload = assistantEntry.content;
                        assistantEntry.timestamp = Date.now();
                        const iterationText = assistantEntry.content.slice(currentIterationStartLength).toLowerCase();
                        if (iterationText.includes('<tool_call')) {
                            assistantEntry.content = assistantEntry.content.slice(0, currentIterationStartLength);
                            assistantEntry.payload = assistantEntry.content;
                            assistantEntry.timestamp = Date.now();
                            ignoreIterationChunks = true;
                            iterationsWithToolCalls.add(currentIteration);
                            streamedCharsByIteration.set(currentIteration, 0);
                            // Start the "generating tool call" indicator so the user
                            // sees progress while the tool_call JSON payload streams
                            // in invisibly. On big write_file calls this period can be
                            // 30-60 seconds; before this the webview went silent.
                            startToolCallGen();
                            void this.syncState();
                            return;
                        }
                        const streamedChars = streamedCharsByIteration.get(currentIteration) ?? 0;
                        streamedCharsByIteration.set(currentIteration, streamedChars + chunkText.length);
                        void this.syncState();
                        return;
                    }
                    if (type === 'tool_loop:tool_calls') {
                        const iteration = this.getToolLoopIteration(payload, currentIteration);
                        const p = payload;
                        void turnLog?.append({ type: 'tool-calls', iteration, tools: p?.tools ?? [] });
                        iterationsWithToolCalls.add(iteration);
                        ignoreIterationChunks = true;
                        streamedCharsByIteration.set(iteration, 0);
                        if (assistantEntry.content.length !== currentIterationStartLength) {
                            assistantEntry.content = assistantEntry.content.slice(0, currentIterationStartLength);
                            assistantEntry.payload = assistantEntry.content;
                            assistantEntry.timestamp = Date.now();
                            void this.syncState();
                        }
                        return;
                    }
                    if (type === 'tool_loop:llm_response') {
                        const p = payload;
                        void turnLog?.append({ type: 'llm-response', iteration: p?.iteration, responsePreview: (0, host_kit_1.previewText)(p?.response ?? '') });
                    }
                    if (type === 'tool_loop:parse_retry') {
                        const p = payload;
                        void turnLog?.append({ type: 'parse-retry', iteration: p?.iteration, attempt: p?.attempt });
                    }
                    if (type === 'tool_loop:stream_abort') {
                        const p = payload;
                        void turnLog?.append({ type: 'stream-abort', iteration: p?.iteration, reason: p?.reason, length: p?.length, fingerprintPreview: p?.fingerprintPreview });
                    }
                    if (type === 'tool_loop:prose_loop_nudge') {
                        const p = payload;
                        void turnLog?.append({ type: 'prose-loop-nudge', iteration: p?.iteration, reason: p?.reason });
                    }
                    if (type === 'tool_loop:fake_tool_result_detected') {
                        const p = payload;
                        void turnLog?.append({ type: 'fake-tool-result', iteration: p?.iteration, preview: p?.preview });
                    }
                    if (type === 'tool_loop:false_completion_nudge') {
                        const p = payload;
                        void turnLog?.append({ type: 'false-completion-nudge', iteration: p?.iteration });
                    }
                    if (type === 'tool_loop:code_fence_nudge') {
                        const p = payload;
                        void turnLog?.append({ type: 'code-fence-nudge', iteration: p?.iteration, fenceLines: p?.fenceLines });
                    }
                    if (type === 'tool_loop:todo_churn_nudge') {
                        const p = payload;
                        void turnLog?.append({ type: 'todo-churn-nudge', iteration: p?.iteration, consecutive: p?.consecutive });
                    }
                    if (type === 'tool_loop:empty_retry') {
                        const p = payload;
                        void turnLog?.append({ type: 'empty-retry', iteration: p?.iteration, attempt: p?.attempt });
                    }
                    if (type === 'tool_loop:compacted') {
                        const p = payload;
                        void turnLog?.append({ type: 'compacted', iteration: p?.iteration, messagesCompacted: p?.messagesCompacted, beforeTokens: p?.beforeTokens, afterTokens: p?.afterTokens });
                    }
                    if (type === 'tool_loop:json_todo_auto_promoted') {
                        const p = payload;
                        void turnLog?.append({ type: 'json-todo-auto-promoted', iteration: p?.iteration, itemCount: p?.itemCount });
                    }
                    if (type === 'tool_loop:tool_error') {
                        const p = payload;
                        void turnLog?.append({ type: 'tool-error', name: p?.name, error: p?.error });
                    }
                    if (type === 'tool_loop:tool_blocked') {
                        const p = payload;
                        void turnLog?.append({ type: 'tool-blocked', name: p?.name, reason: p?.reason });
                    }
                    if (type === 'tool_loop:tool_not_found') {
                        const p = payload;
                        void turnLog?.append({ type: 'tool-not-found', name: p?.name });
                    }
                    if (type === 'tool_loop:tool_execute') {
                        stopThinking();
                        stopToolCallGen();
                        const p = payload;
                        const name = p?.name ?? '';
                        void turnLog?.append({ type: 'tool-execute', name, params: p?.params ? Object.fromEntries(Object.entries(p.params).map(([k, v]) => [k, (0, host_kit_1.previewText)(v)])) : {} });
                        const skillId = name ? toolToSkill.get(name) : undefined;
                        const skillName = skillId ? skillNameById.get(skillId) : undefined;
                        // Announce the skill once per contiguous run of its tools so users
                        // see which skill the agent is invoking without repeating every call.
                        if (skillId && skillId !== lastAnnouncedSkillId && skillName) {
                            const skillMarker = `\n\n_▸ using skill: ${skillName}_\n`;
                            if (!assistantEntry.content.endsWith(skillMarker)) {
                                assistantEntry.content += skillMarker;
                                assistantEntry.payload = assistantEntry.content;
                            }
                            lastAnnouncedSkillId = skillId;
                        }
                        // Capture pre-write state for diff summaries. We read here (before
                        // the tool runs) so we can compare against params.content later.
                        // IMPORTANT: only capture `before` on the FIRST edit to this file
                        // within an iteration. Later parallel edits to the same file
                        // overwriting this would clobber the original pre-iteration
                        // state and make the final diff show only the last edit's delta.
                        if (name === 'write_file' && p?.params?.path) {
                            const absPath = path.isAbsolute(p.params.path) ? p.params.path : path.resolve(workspaceRoot, p.params.path);
                            if (!pendingWriteBefore.has(absPath)) {
                                pendingWriteBefore.set(absPath, readFileSafe(absPath));
                            }
                            pendingWriteAfter.set(absPath, p.params.content ?? '');
                        }
                        // apply_edit: capture before-state too so we can render a diff
                        // card on success. Without this, the user sees the italic
                        // `→ apply_edit …` line and then nothing — no visual
                        // confirmation that the edit landed or what changed.
                        if (name === 'apply_edit' && p?.params?.path) {
                            const absPath = path.isAbsolute(p.params.path) ? p.params.path : path.resolve(workspaceRoot, p.params.path);
                            // Only set on FIRST edit to this file this iteration.
                            // Multiple parallel apply_edits to the same file should
                            // share one diff card showing the cumulative change.
                            if (!pendingWriteBefore.has(absPath)) {
                                pendingWriteBefore.set(absPath, readFileSafe(absPath));
                            }
                            // `after` is computed from the actual file post-edit (in
                            // tool_result); the placeholder keeps the key ordering
                            // consistent with write_file's flow.
                            pendingWriteAfter.set(absPath, '');
                        }
                        // run_command: stash params so the tool_result handler can
                        // pair IN (command) with OUT (captured stdout/stderr).
                        if (name === 'run_command') {
                            pendingRunCommand = {
                                cmd: String(p?.params?.cmd ?? ''),
                                args: String(p?.params?.args ?? '')
                            };
                        }
                        // Surface the tool call inline in the chat so users see what the
                        // agent is doing. Paths get compacted to a workspace-relative
                        // form so the transcript stays readable — absolute paths like
                        // `/Users/mark/Documents/GitHub/pburg-bowl/api/...` swamp the
                        // side panel with noise.
                        const rawPrimary = p?.params?.path || p?.params?.pattern || p?.params?.cmd || p?.params?.query || '';
                        const primaryParam = compactToolDisplayParam(rawPrimary, workspaceRoot);
                        const display = primaryParam ? `→ ${name} ${primaryParam}` : `→ ${name}`;
                        // Repeat detection — if this tool+primary was invoked in the
                        // recent window, render a distinct marker so the user sees the
                        // model is redoing work (rather than N identical lines stacking
                        // up and looking like normal progress). Models commonly
                        // re-read a file they just read, or ls the same dir twice; the
                        // marker makes that visible without hiding the call.
                        const isRepeat = recentToolCallDisplays.slice(-REPEAT_WINDOW).includes(display);
                        // Emit as a bandit-tl (timeline) fence rather than raw italic
                        // markdown. The webview renderer turns consecutive bandit-tl
                        // rows into a vertical rail with status dots — Claude-Code-
                        // style — instead of a flat wall of italic lines. The `id`
                        // lets tool_result rewrite this row's status when the call
                        // finishes (string-replace in assistantEntry.content).
                        const tlId = `${name}-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 6)}`;
                        const tlPayload = JSON.stringify({
                            id: tlId,
                            glyph: isRepeat ? '↺' : '→',
                            name,
                            primary: primaryParam || null,
                            status: isRepeat ? 'repeat' : 'running',
                            skill: skillName ?? null
                        });
                        // Remember the id so tool_result can find and mutate this
                        // specific fence. Pending entries are keyed by tool name; if
                        // multiple parallel calls to the same tool fire, the Map
                        // stores the latest (and tool_result events come back in
                        // submission order, so they pair up correctly).
                        pendingTimelineIds.set(name, tlId);
                        const marker = `\n\n\`\`\`bandit-tl\n${tlPayload}\n\`\`\`\n`;
                        recentToolCallDisplays.push(display);
                        if (recentToolCallDisplays.length > REPEAT_WINDOW * 2) {
                            recentToolCallDisplays.splice(0, recentToolCallDisplays.length - REPEAT_WINDOW);
                        }
                        if (!assistantEntry.content.endsWith(marker)) {
                            // Strip any trailing partial-tag starter left from the
                            // previous iteration's LLM stream (`…<` or `…<tool_c`).
                            // The iteration-boundary truncation clears whole
                            // `<tool_call>` blocks but can miss the bare `<` that
                            // lands between a tool marker and the next iteration's
                            // first streamed chunk, leaving `foo.cs<` stuck in
                            // history. Clean it here so every marker starts flush.
                            assistantEntry.content = assistantEntry.content.replace(/<\/?[a-zA-Z][a-zA-Z0-9_-]*(?:\s[^>]*)?$|<$/, '');
                            assistantEntry.content += marker;
                            assistantEntry.payload = assistantEntry.content;
                            void this.updateConversation([...this.conversations.messages], { persist: false });
                            void this.syncState();
                        }
                        void this.setStatusMessage(skillName ? `Running ${skillName}: ${name}…` : `Running tool: ${name}…`);
                    }
                    if (type === 'tool_loop:tool_result') {
                        const p = payload;
                        const name = p?.name ?? '';
                        const started = toolStartedAt.get(name);
                        const duration = started ? Date.now() - started : 0;
                        void turnLog?.append({ type: 'tool-result', name, isError: !!p?.isError, durationMs: duration, outputLength: p?.outputLength });
                        void (0, host_kit_1.runHooks)('PostToolUse', hookSettings, { toolName: name, durationMs: duration }, workspaceRoot);
                        // Flip this tool's timeline row from running → done/error and
                        // back-fill its duration. We find the exact fence by its id
                        // (set in tool_execute above) and rewrite the JSON payload in
                        // place inside assistantEntry.content. If the id is gone
                        // (e.g. truncated by the iteration-boundary cleanup) we just
                        // no-op — the row stays "running" visually, which is a minor
                        // glitch but better than crashing the turn.
                        const tlId = pendingTimelineIds.get(name);
                        if (tlId) {
                            pendingTimelineIds.delete(name);
                            const fenceRe = new RegExp('```bandit-tl\\n(\\{"id":"' + tlId.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '"[^\\n]*\\})\\n```', 'g');
                            assistantEntry.content = assistantEntry.content.replace(fenceRe, (_full, jsonStr) => {
                                try {
                                    const row = JSON.parse(jsonStr);
                                    row.status = p?.isError ? 'error' : 'done';
                                    row.durationMs = duration;
                                    return '```bandit-tl\n' + JSON.stringify(row) + '\n```';
                                }
                                catch {
                                    return _full;
                                }
                            });
                            assistantEntry.payload = assistantEntry.content;
                            void this.syncState();
                        }
                        // task (subagent) completion: render a collapsible card
                        // that surfaces the goal, the tools the subagent ran, and
                        // the final synopsis. Parent assistantEntry.content stays
                        // clean — the card is the whole subagent trace.
                        if (name === 'task' && subagentBuffer) {
                            const synopsis = payload?.outputSnippet ?? '';
                            const fence = JSON.stringify({
                                goal: subagentBuffer.goal,
                                result: synopsis,
                                iterations: subagentBuffer.iterations ?? 0,
                                hitLimit: subagentBuffer.hitLimit ?? false,
                                tools: subagentBuffer.tools,
                                isError: !!p?.isError
                            });
                            assistantEntry.content += `\n\n\`\`\`bandit-subagent\n${fence}\n\`\`\`\n`;
                            assistantEntry.payload = assistantEntry.content;
                            subagentBuffer = null;
                            void this.syncState();
                        }
                        // run_command: render a Claude-Code-style IN/OUT card. The
                        // agent-core event carries up to 280 chars of outputSnippet;
                        // anything longer gets a "… (N more chars)" marker. The
                        // renderer in App.tsx picks up the `bandit-run` fence.
                        if (name === 'run_command' && pendingRunCommand) {
                            const fullCmd = [pendingRunCommand.cmd, pendingRunCommand.args].filter(Boolean).join(' ').trim();
                            const snippet = p?.outputSnippet ?? '';
                            const truncated = (p?.outputLength ?? 0) > snippet.length;
                            const payloadJson = JSON.stringify({
                                cmd: fullCmd,
                                out: snippet,
                                isError: !!p?.isError,
                                truncated,
                                totalLen: p?.outputLength ?? snippet.length
                            });
                            assistantEntry.content += `\n\n\`\`\`bandit-run\n${payloadJson}\n\`\`\`\n`;
                            assistantEntry.payload = assistantEntry.content;
                            pendingRunCommand = null;
                            void this.syncState();
                        }
                        // Diff card rendering is deferred to iteration boundaries
                        // (see flushPendingEditDiffs) so that parallel edits to
                        // the same file get combined into one cumulative card
                        // and parallel edits to different files each get their
                        // own card. Rendering per-tool_result would mis-correlate
                        // when the model emits 10 apply_edits in one iteration
                        // (real telemetry: S3Api Apr 22, iteration 2 had 10).
                        // todo_write success → render the current checklist as a block.
                        // The model calls todo_write repeatedly (once per plan revision /
                        // status change), so we REPLACE the previous Plan block in
                        // place instead of appending a new one. Without this the user
                        // sees a stack of Plan lists and no sense of items getting
                        // checked off — the rendered output looks identical across
                        // calls even though the store state is advancing correctly.
                        if (name === 'todo_write' && !p?.isError) {
                            const items = todoStore.snapshot();
                            if (items.length > 0) {
                                // Accept every status alias the store might have persisted
                                // before the normalizer landed (old "complete" payloads
                                // still in conversation state), plus the canonical forms.
                                const isDone = (s) => s === 'done' || s === 'complete' || s === 'completed' || s === 'finished';
                                const isActive = (s) => s === 'in_progress' || s === 'in-progress' || s === 'inprogress'
                                    || s === 'active' || s === 'working' || s === 'running';
                                const lines = items.map(t => {
                                    const status = String(t.status ?? '').toLowerCase();
                                    const box = isDone(status) ? '✓' : isActive(status) ? '◐' : '○';
                                    return `${box} ${t.content}`;
                                });
                                const block = `\n\n**Plan**\n${lines.map(l => '- ' + l).join('\n')}\n`;
                                // Remove ALL prior Plan blocks from the content, then
                                // append a fresh one at the current end. This way the
                                // plan always renders near the most recent activity
                                // instead of getting stranded near the top of a long
                                // turn's transcript (user saw 10 iterations worth of
                                // tool activity scroll past the Plan, never seeing
                                // items flip to ✓ without scrolling back up).
                                const PLAN_BLOCK_REGEX = /\n\n\*\*Plan\*\*\n(?:- [^\n]*\n)+/g;
                                assistantEntry.content = assistantEntry.content.replace(PLAN_BLOCK_REGEX, '');
                                assistantEntry.content += block;
                                assistantEntry.payload = assistantEntry.content;
                                void this.syncState();
                            }
                        }
                    }
                }
            });
            // Compaction budget: reserve ~25% of num_ctx for the model's
            // response + system prompt headroom, give the remaining ~75% to
            // the rolling tool-result history. Ollama's runtime options are
            // the single source of truth here — if the cluster rebuilds the
            // 31B Modelfile with a larger num_ctx, this auto-adapts.
            const runtimeOpts = (0, stealth_core_runtime_1.resolveOllamaRuntimeOptions)(model);
            const messageTokenBudget = Math.floor(runtimeOpts.num_ctx * 0.75);
            // Seed the tool-use loop with prior conversation turns so
            // follow-up prompts ("you didn't update the health controller")
            // carry context from the previous turn. Without this, the
            // extension called loop.run(userGoal, ...) every turn, which
            // starts fresh with only the system prompt + current user
            // message — the model had no memory of what it just did. The
            // CLI already does this via runWithMessages; parity now.
            const seedMessages = this.conversation
                .filter((entry) => entry.role === 'user' || entry.role === 'assistant')
                .filter((entry) => entry.id !== assistantEntry.id)
                .filter((entry) => typeof entry.content === 'string' && entry.content.trim().length > 0)
                .map((entry) => ({
                role: entry.role,
                content: typeof entry.content === 'string' ? entry.content : ''
            }));
            // Ensure the current user turn is the last message the loop sees.
            if (seedMessages.length === 0 || seedMessages[seedMessages.length - 1].content !== userGoal) {
                seedMessages.push({ role: 'user', content: userGoal });
            }
            // Native tool calling when the model advertises it — Qwen2.5-Coder,
            // Llama 3.1+, Devstral, DeepSeek-Coder-V2+, Nemotron. Skips the
            // XML tool block in the system prompt (~1000-1800 tokens) and
            // routes schemas through Ollama's `tools` field where the model's
            // chat template serializes them natively. Enabled on both direct
            // Ollama and the bandit cloud path — the cloud provider's
            // serializeBanditPayload forwards `tools` as an unknown top-level
            // key which the gateway's BuildOllamaRequestPayloadAsync relays
            // to upstream Ollama via AdditionalProperties.
            const nativeTools = modelCaps.supportsToolCalling
                && (providerKind === 'ollama' || providerKind === 'bandit');
            const result = await loop.runWithMessages(seedMessages, chat, systemPrompt, { messageTokenBudget, nativeTools });
            stopThinking();
            stopToolCallGen();
            // Final iteration's edits weren't flushed by an iteration
            // boundary (there wasn't a next iteration). Flush them now so
            // the user sees diff cards for the last edit batch too.
            flushPendingEditDiffs();
            await turnLog?.append({
                type: 'final-response',
                iterations: result.iterations,
                hitLimit: result.hitLimit,
                finalPreview: (0, host_kit_1.previewText)(result.finalResponse),
                logPath: turnLog.filePath
            });
            await (0, host_kit_1.runHooks)('Stop', hookSettings, {}, workspaceRoot).catch(() => undefined);
            const finalResponse = result.finalResponse.trim();
            const finalIteration = result.iterations;
            const finalIterationStreamedChars = streamedCharsByIteration.get(finalIteration) ?? 0;
            const shouldAnimateFinalResponse = finalResponse.length > 0
                && finalIterationStreamedChars === 0
                && !iterationsWithToolCalls.has(finalIteration);
            // Preserve the tool-activity transcript we accumulated during the
            // turn (skill markers, `→ tool` lines, diff cards, Plan block).
            // When the transcript is non-empty we always append the final
            // prose — never animate, because animation reseeds the content
            // and any event that fires during the animation loop (status
            // message, thinking tick, etc.) can race with the reseed and
            // visibly wipe diff cards. Simpler + race-free: just concat.
            // Strip any thinking / tool-call-gen markers left at the tail
            // before deciding how to finalize. They tick at turn-end time
            // and would otherwise land mid-transcript as "_⟳ scheming…_"
            // stranded above the real answer.
            const TAIL_MARKERS_RE = /(?:\n*`⟳\s+(?:[a-z]+…|generating tool call(?:[^`]*))`\s*)+$/;
            const activityTranscript = assistantEntry.content.replace(TAIL_MARKERS_RE, '').trimEnd();
            const hadToolActivity = iterationsWithToolCalls.size > 0;
            if (hadToolActivity) {
                // Tool-using turn: content holds the accumulated activity
                // transcript (skill markers, tool-execute lines, diff cards,
                // Plan block, etc.). The model's final prose was emitted in
                // the final iteration but was suppressed from streaming
                // (suppressStreamPreamble). Append it now so the user sees
                // the conclusion below the work record.
                assistantEntry.content = finalResponse
                    ? `${activityTranscript}\n\n${finalResponse}`
                    : activityTranscript;
                assistantEntry.payload = assistantEntry.content;
                assistantEntry.timestamp = Date.now();
            }
            else if (activityTranscript) {
                // No tool activity but content is non-empty — iteration 0's
                // prose streamed in directly (pure Q&A like "who are you?",
                // /help explanations). The final response is already in
                // content verbatim; appending it again would duplicate the
                // entire answer. Keep content as-is.
                assistantEntry.content = activityTranscript;
                assistantEntry.payload = assistantEntry.content;
                assistantEntry.timestamp = Date.now();
            }
            else if (shouldAnimateFinalResponse) {
                // Truly empty content (no streaming happened) + a final
                // response to show. Animate for the pure-Q&A feel.
                await this.animateAssistantResponse(assistantEntry, finalResponse);
            }
            else {
                assistantEntry.content = finalResponse;
                assistantEntry.payload = assistantEntry.content;
                assistantEntry.timestamp = Date.now();
            }
            if (!assistantEntry.content) {
                this.conversation = this.conversation.filter(e => e.id !== assistantEntry.id);
            }
            if (result.iterations > 0) {
                const plural = result.iterations !== 1 ? 's' : '';
                void this.setStatusMessage(`Completed with ${result.iterations} tool call${plural}.`);
            }
            await this.updateConversation(this.conversation);
            await this.syncState();
        }
        catch (error) {
            // Stop any live thinking markers first — otherwise the assistant
            // entry keeps a trailing "_⟳ pondering…_" or "_⟳ generating tool
            // call · 1.2kb_" line that was supposed to be cleared on success.
            // Without this the user sees the spinner verbs stranded in chat
            // even after the error toast fires, which is the exact failure
            // the pburg-bowl session report surfaced (Ollama 404 on missing
            // coding-model → thinking verbs loop forever in the UI).
            stopThinking();
            stopToolCallGen();
            if (assistantAdded && !assistantEntry.content.trim()) {
                this.conversation = this.conversation.filter(e => e.id !== assistantEntry.id);
            }
            const message = error instanceof Error ? error.message : 'Unknown issue.';
            const friendlyProvider = this.describeProvider(this.getProviderKind(configuration));
            // Surface Ollama-specific failures with actionable guidance so the
            // user doesn't have to decode "Ollama request failed: 404 …" —
            // the most common cause is a missing model name from an
            // explicit setting, not a network issue.
            let displayMessage = `${friendlyProvider} tool agent error: ${message}`;
            const lower = message.toLowerCase();
            if (lower.includes('ollama request failed: 404') || (lower.includes('model') && lower.includes('not found'))) {
                const match = message.match(/model[^"]*"([^"]+)"|model ['`]?([A-Za-z0-9:._-]+)['`]?/i);
                const modelName = match ? (match[1] ?? match[2] ?? 'your configured model') : 'your configured model';
                displayMessage = `Ollama doesn't have "${modelName}" installed. Run: ollama pull ${modelName} — or set banditStealth.ollamaAutoRouteModels to false so Ollama uses your ollamaModel directly.`;
            }
            this.postMessage({ type: 'error', message: displayMessage });
            void vscode.window.showErrorMessage(displayMessage);
            if (assistantAdded) {
                await this.updateConversation(this.conversation);
                await this.syncState();
            }
        }
        finally {
            this.cancelActiveStream();
            await this.setBusy(false);
        }
    }
    getToolLoopIteration(payload, fallback) {
        if (payload && typeof payload === 'object') {
            const rawIteration = payload.iteration;
            if (typeof rawIteration === 'number' && Number.isFinite(rawIteration) && rawIteration >= 0) {
                return Math.floor(rawIteration);
            }
        }
        return fallback;
    }
    async animateAssistantResponse(entry, text, preamble) {
        const source = text.trim();
        const prefix = preamble ? `${preamble.trimEnd()}\n\n` : '';
        if (!source) {
            entry.content = preamble ? preamble.trimEnd() : '';
            entry.payload = entry.content;
            entry.timestamp = Date.now();
            return;
        }
        const tokens = source.split(/(\s+)/).filter((token) => token.length > 0);
        const maxChunks = 60;
        const chunkSize = Math.max(1, Math.ceil(tokens.length / maxChunks));
        // Seed the entry with the preserved activity transcript so the
        // diff cards / plan remain visible while the final prose animates
        // in beneath them.
        entry.content = prefix;
        entry.payload = prefix;
        entry.timestamp = Date.now();
        await this.syncState();
        for (let index = 0; index < tokens.length; index += chunkSize) {
            const chunk = tokens.slice(index, index + chunkSize).join('');
            entry.content += chunk;
            entry.payload = entry.content;
            entry.timestamp = Date.now();
            await this.syncState();
            await new Promise((resolve) => setTimeout(resolve, 10));
        }
    }
    buildChatRequest(configuration, contextBlock) {
        const providerKind = this.getProviderKind(configuration);
        const lastUserEntry = [...this.conversation]
            .reverse()
            .find((entry) => entry.role === 'user');
        const hasImages = Boolean(lastUserEntry?.images?.length);
        const model = providerKind === 'ollama'
            ? this.resolveChatModel(configuration, hasImages)
            : (configuration.get('model', 'bandit-core-1') ?? 'bandit-core-1');
        const temperature = configuration.get('temperature', 0.2);
        const topP = configuration.get('topP', 1);
        const allowInlineImages = this.canUseInlineImages(configuration, model);
        const messages = [];
        const systemPrompt = this.buildSystemPrompt(providerKind, configuration, contextBlock, model, lastUserEntry?.content);
        if (systemPrompt) {
            messages.push({
                role: 'system',
                content: systemPrompt
            });
        }
        for (const entry of this.conversation) {
            messages.push({
                role: entry.role,
                content: this.buildMessageContent(entry, allowInlineImages)
            });
        }
        const request = {
            model,
            messages,
            stream: true,
            temperature
        };
        if (typeof topP === 'number' && !Number.isNaN(topP)) {
            request.options = { top_p: topP };
        }
        if (allowInlineImages && lastUserEntry) {
            const payloadImages = lastUserEntry?.images
                ?.map((image) => this.extractImagePayload(image))
                .filter((image) => image.length > 0);
            if (payloadImages && payloadImages.length > 0) {
                request.images = payloadImages;
            }
        }
        return request;
    }
    buildMessageContent(entry, allowInlineImages) {
        const payload = typeof entry.payload === 'string' && entry.payload.length > 0
            ? entry.payload
            : entry.content;
        const text = typeof payload === 'string' ? payload : payload != null ? String(payload) : '';
        if (!allowInlineImages) {
            return text;
        }
        const images = Array.isArray(entry.images) ? entry.images : [];
        if (images.length === 0) {
            return text;
        }
        const parts = [];
        if (text.trim().length > 0) {
            parts.push({ type: 'text', text });
        }
        for (const rawImage of images) {
            const normalized = this.extractImagePayload(rawImage);
            if (!normalized) {
                continue;
            }
            parts.push({ type: 'image_url', image_url: { url: normalized } });
        }
        if (parts.length === 0) {
            return text;
        }
        if (parts.length === 1 && parts[0]?.type === 'text') {
            return parts[0].text;
        }
        return parts;
    }
    isInlineImageEnabled(configuration) {
        const provider = this.getProviderKind(configuration);
        if (provider === 'bandit') {
            const model = configuration.get('model', 'bandit-core-1') ?? 'bandit-core-1';
            return model.trim().toLowerCase().startsWith('bandit-core');
        }
        if (provider === 'ollama') {
            const visionModel = this.resolveChatModel(configuration, true);
            return this.canUseInlineImages(configuration, visionModel);
        }
        return false;
    }
    calculateContextUsage(configuration, overrideMessages) {
        if (!this.isInlineImageEnabled(configuration)) {
            return undefined;
        }
        const limit = 128000;
        const messages = overrideMessages ?? this.conversation;
        const hasImages = messages.some((entry) => Array.isArray(entry.images) && entry.images.length > 0);
        const providerKind = this.getProviderKind(configuration);
        const model = providerKind === 'ollama'
            ? this.resolveChatModel(configuration, hasImages)
            : (configuration.get('model', 'bandit-core-1') ?? 'bandit-core-1');
        const systemPrompt = this.buildSystemPrompt(providerKind, configuration, undefined, model);
        let used = 0;
        if (systemPrompt) {
            used += this.estimateTokenUsage(systemPrompt);
        }
        for (const entry of messages) {
            const messageContent = typeof entry.payload === 'string' && entry.payload.length > 0 ? entry.payload : entry.content;
            used += this.estimateTokenUsage(messageContent);
            if (Array.isArray(entry.images) && entry.images.length > 0) {
                used += entry.images.length * 2048;
            }
        }
        return { used, limit };
    }
    normalizeIntentMemory(entries) {
        if (!Array.isArray(entries)) {
            return [];
        }
        const normalized = new Map();
        for (const entry of entries) {
            if (!entry || typeof entry.summary !== 'string' || entry.summary.trim().length === 0) {
                continue;
            }
            const action = typeof entry.action === 'string' && entry.action.trim().length > 0 ? entry.action.trim() : 'unknown';
            const summary = entry.summary.trim();
            const key = `${action}:${summary}`;
            const confidence = typeof entry.confidence === 'number' && Number.isFinite(entry.confidence)
                ? Math.max(0, Math.min(1, entry.confidence))
                : undefined;
            const record = {
                action,
                target: typeof entry.target === 'string' && entry.target.trim().length > 0 ? entry.target.trim() : undefined,
                summary,
                confidence,
                lastUsed: typeof entry.lastUsed === 'number' && Number.isFinite(entry.lastUsed) ? entry.lastUsed : Date.now()
            };
            const existing = normalized.get(key);
            if (!existing || existing.lastUsed < record.lastUsed) {
                normalized.set(key, record);
            }
        }
        return Array.from(normalized.values())
            .sort((a, b) => b.lastUsed - a.lastUsed)
            .slice(0, 20);
    }
    buildIntentSuggestions() {
        return this.intentMemory.slice(0, 4).map((entry) => ({
            label: entry.target && entry.target !== entry.summary ? `${entry.summary} (${entry.target})` : entry.summary,
            summary: entry.summary,
            action: entry.action,
            confidence: entry.confidence
        }));
    }
    findLatestIntent(entries) {
        for (let index = entries.length - 1; index >= 0; index -= 1) {
            const candidate = entries[index]?.intent;
            if (candidate) {
                return candidate;
            }
        }
        return undefined;
    }
    summarizeIntent(insight) {
        if (insight.summary && insight.summary.trim().length > 0) {
            return insight.summary.trim();
        }
        const parts = [insight.action, insight.intent, insight.target]
            .map((value) => (typeof value === 'string' ? value.trim() : ''))
            .filter((value) => value.length > 0);
        if (parts.length === 0) {
            return insight.action || 'General assistance';
        }
        return parts.join(' • ');
    }
    async setIntentInsight(insight) {
        this.currentIntent = insight ? { ...insight, summary: this.summarizeIntent(insight) } : undefined;
        await this.syncState();
    }
    async clearLatestIntentFromConversation() {
        const conversation = this.getCurrentConversation();
        if (!conversation) {
            return;
        }
        let updated = false;
        for (let index = conversation.messages.length - 1; index >= 0; index -= 1) {
            const entry = conversation.messages[index];
            if (entry?.intent) {
                const updatedEntry = { ...entry };
                delete updatedEntry.intent;
                conversation.messages[index] = updatedEntry;
                updated = true;
            }
        }
        if (updated) {
            this.conversation = conversation.messages;
            await this.persistConversationHistory();
        }
    }
    async attachIntentToMessage(messageId, insight) {
        const conversation = this.ensureActiveConversation();
        const index = conversation.messages.findIndex((entry) => entry.id === messageId);
        if (index === -1) {
            return;
        }
        const current = conversation.messages[index];
        const next = insight
            ? { ...current, intent: { ...insight, summary: this.summarizeIntent(insight) } }
            : { ...current };
        if (!insight) {
            delete next.intent;
        }
        conversation.messages[index] = next;
        this.conversation = conversation.messages;
        await this.persistConversationHistory();
    }
    async recordIntentMemory(insight) {
        const summary = this.summarizeIntent(insight);
        if (!summary) {
            return;
        }
        const entry = {
            action: insight.action || 'general',
            target: insight.target,
            summary,
            confidence: insight.confidence,
            lastUsed: Date.now()
        };
        const existingIndex = this.intentMemory.findIndex((item) => item.action === entry.action && item.summary === entry.summary);
        if (existingIndex >= 0) {
            this.intentMemory[existingIndex] = { ...this.intentMemory[existingIndex], ...entry };
        }
        else {
            this.intentMemory.unshift(entry);
        }
        this.intentMemory = this.normalizeIntentMemory(this.intentMemory);
        await this.context.workspaceState.update(INTENT_MEMORY_STORAGE_KEY, this.intentMemory);
    }
    async interpretIntent(prompt, configuration, providerKind) {
        if (providerKind !== 'bandit') {
            return undefined;
        }
        const apiKey = await this.context.secrets.get(API_KEY_SECRET_KEY);
        if (!apiKey) {
            return undefined;
        }
        const intentUrl = this.resolveIntentUrl(configuration);
        const editor = vscode.window.activeTextEditor;
        const selection = editor?.selection && !editor.selection.isEmpty ? editor.document.getText(editor.selection) : undefined;
        const filePath = editor ? vscode.workspace.asRelativePath(editor.document.uri, false) : undefined;
        const languageId = editor?.document.languageId;
        const payload = {
            text: prompt,
            mode: 'agent',
            provider: providerKind,
            context: {
                filePath,
                languageId,
                selection,
                workspace: vscode.workspace.name
            }
        };
        const trimmedApiKey = apiKey.trim();
        if (!trimmedApiKey) {
            return undefined;
        }
        const headers = {
            'Content-Type': 'application/json',
            Authorization: `Bearer ${trimmedApiKey}`
        };
        let rawData;
        let primaryError;
        try {
            const response = await fetch(intentUrl, {
                method: 'POST',
                headers,
                body: JSON.stringify(payload)
            });
            if (!response.ok) {
                const detail = await response.text().catch(() => '');
                throw new Error(`Intent request failed: ${response.status} ${response.statusText}${detail ? ` – ${detail}` : ''}`);
            }
            rawData = (await response.json());
        }
        catch (error) {
            primaryError = error;
            console.warn('Bandit intent endpoint unavailable, attempting completions fallback.', error);
        }
        if (!rawData) {
            try {
                rawData = await this.requestIntentViaCompletions(prompt, {
                    mode: 'agent',
                    filePath,
                    languageId,
                    selection,
                    workspace: vscode.workspace.name ?? undefined
                }, configuration, trimmedApiKey);
            }
            catch (fallbackError) {
                const finalError = fallbackError instanceof Error ? fallbackError : new Error(String(fallbackError));
                if (primaryError instanceof Error) {
                    throw new Error(`${primaryError.message}; completions fallback failed: ${finalError.message}`);
                }
                throw finalError;
            }
        }
        if (!rawData) {
            return undefined;
        }
        const normalized = this.normalizeIntentInsight({
            ...rawData,
            action: typeof rawData.action === 'string' && rawData.action.trim().length > 0
                ? rawData.action
                : 'general_assist',
            summary: typeof rawData.summary === 'string' ? rawData.summary : undefined,
            intent: typeof rawData.intent === 'string' ? rawData.intent : undefined,
            target: typeof rawData.target === 'string' ? rawData.target : undefined,
            confidence: typeof rawData.confidence === 'number' ? rawData.confidence : undefined,
            rationale: typeof rawData.rationale === 'string' ? rawData.rationale : undefined,
            raw: rawData
        });
        if (!normalized) {
            return undefined;
        }
        const summary = this.summarizeIntent(normalized);
        return { ...normalized, summary };
    }
    resolveIntentUrl(configuration) {
        const raw = configuration.get('intentUrl');
        const fallback = configuration.get('apiUrl', 'https://api.burtson.ai/completions');
        return this.deriveEndpoint(raw, fallback, 'intent');
    }
    resolveSemanticUrl(configuration) {
        const raw = configuration.get('semanticUrl');
        const fallback = configuration.get('apiUrl', 'https://api.burtson.ai/completions');
        return this.deriveEndpoint(raw, fallback, 'semantic/query');
    }
    resolveFeedbackUrl(configuration) {
        const raw = configuration.get('feedbackUrl');
        const fallback = configuration.get('apiUrl', 'https://api.burtson.ai/completions');
        return this.deriveEndpoint(raw, fallback, 'feedback');
    }
    deriveEndpoint(raw, fallbackBase, path) {
        const candidate = raw?.trim();
        const base = candidate && candidate.length > 0 ? candidate : fallbackBase;
        try {
            const url = new URL(base);
            const sanitized = url.pathname.replace(/\/+$/, '');
            if (sanitized.toLowerCase().endsWith(`/${path}`)) {
                url.pathname = sanitized;
            }
            else if (sanitized.toLowerCase().endsWith('/completions')) {
                url.pathname = sanitized.replace(/\/completions$/i, `/${path}`);
            }
            else if (sanitized.toLowerCase().endsWith('/chat/completions')) {
                url.pathname = sanitized.replace(/\/chat\/completions$/i, `/${path}`);
            }
            else {
                url.pathname = `${sanitized}/${path}`.replace(/\/+/g, '/');
            }
            url.search = '';
            url.hash = '';
            return url.toString();
        }
        catch {
            const normalized = fallbackBase.replace(/\/+$/, '');
            return `${normalized}/${path}`;
        }
    }
    async fetchSemanticKnowledge(prompt, configuration, apiKey) {
        try {
            const semanticUrl = this.resolveSemanticUrl(configuration);
            const response = await fetch(semanticUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    Authorization: `Bearer ${apiKey}`
                },
                body: JSON.stringify({
                    text: prompt,
                    topK: 1,
                    ns: 'bandit-core'
                })
            });
            if (!response.ok) {
                return '';
            }
            const results = (await response.json());
            const top = Array.isArray(results) ? results[0] : undefined;
            const snippet = top?.payload?.text ?? '';
            if (!snippet || typeof snippet !== 'string') {
                return '';
            }
            return `Bandit context:\n${snippet.trim()}`;
        }
        catch (error) {
            console.warn('Semantic knowledge lookup failed:', error);
            return '';
        }
    }
    async requestIntentViaCompletions(prompt, context, configuration, apiKey) {
        if (this.getProviderKind(configuration) !== 'bandit') {
            return undefined;
        }
        const selectionSnippet = context.selection ? this.truncateForFeedback(context.selection, 600) : undefined;
        const contextParts = [
            `Mode: ${context.mode}`,
            context.workspace ? `Workspace: ${context.workspace}` : undefined,
            context.filePath ? `File path: ${context.filePath}` : undefined,
            context.languageId ? `Language: ${context.languageId}` : undefined,
            selectionSnippet ? `Selected text:\n${selectionSnippet}` : undefined
        ].filter((value) => Boolean(value));
        const messages = [
            {
                role: 'system',
                content: [
                    'You are an intent classification module for the Bandit Stealth VS Code extension.',
                    'Analyze the user prompt and output a JSON object describing the intent.',
                    'Output schema:',
                    '{',
                    '  "action": string,         // required action label such as "explain_code", "update_file", or "general_assist"',
                    '  "target": string|null,    // optional target file, component, or concept',
                    '  "intent": string|null,    // optional natural language paraphrase of the user goal',
                    '  "summary": string|null,   // optional short summary for UI display',
                    '  "confidence": number,     // confidence between 0 and 1',
                    '  "rationale": string|null  // optional reasoning for the classification',
                    '}',
                    'Always include the "action" key and clamp confidence to the 0–1 range.',
                    'Respond with JSON only. Do not include prose or code fences.'
                ].join('\n')
            },
            {
                role: 'user',
                content: [
                    `User prompt:\n${prompt}`,
                    contextParts.length > 0 ? `Context:\n${contextParts.join('\n')}` : undefined,
                    'Return the JSON object now.'
                ].filter((value) => Boolean(value)).join('\n\n')
            }
        ];
        const responseText = await this.runBanditCompletion(messages, configuration, apiKey, { temperature: 0 });
        const parsed = this.extractJsonObject(responseText);
        if (!parsed) {
            console.warn('Intent fallback response not parseable as JSON.', responseText);
            return undefined;
        }
        return parsed;
    }
    async submitFeedbackViaCompletions(payload, configuration, apiKey) {
        if (this.getProviderKind(configuration) !== 'bandit') {
            return;
        }
        const messages = [
            {
                role: 'system',
                content: [
                    'You triage feedback for the Bandit Stealth VS Code assistant.',
                    'Summarize the provided feedback into JSON for later review.',
                    'Output schema:',
                    '{',
                    '  "summary": string,',
                    '  "category": string,',
                    '  "priority": string,',
                    '  "actionItems": string[]',
                    '}',
                    'Respond with JSON only. Do not include explanations or code fences.'
                ].join('\n')
            },
            {
                role: 'user',
                content: [
                    'Feedback payload:',
                    JSON.stringify(payload, null, 2),
                    'Summarize and categorize this feedback.'
                ].join('\n\n')
            }
        ];
        const responseText = await this.runBanditCompletion(messages, configuration, apiKey, { temperature: 0.15 });
        const parsed = this.extractJsonObject(responseText);
        if (parsed) {
            console.info('Feedback captured via completions fallback:', parsed);
        }
        else {
            console.info('Feedback captured via completions fallback (raw):', responseText.trim());
        }
    }
    async runBanditCompletion(messages, configuration, apiKey, options) {
        if (this.getProviderKind(configuration) !== 'bandit') {
            throw new Error('Bandit completion fallback unavailable for the current provider.');
        }
        const modelSetting = configuration.get('model', 'bandit-core-1');
        const model = modelSetting && modelSetting.trim().length > 0 ? modelSetting.trim() : 'bandit-core-1';
        const ollamaAuth = await Promise.resolve(this.context.secrets.get(OLLAMA_AUTH_SECRET_KEY)).catch(() => undefined);
        const provider = await (0, stealth_core_runtime_1.createProvider)(this.buildProviderSettings(configuration, apiKey, ollamaAuth));
        const request = {
            model,
            messages,
            stream: false,
            temperature: options?.temperature ?? 0
        };
        const topPSetting = typeof options?.topP === 'number' ? options.topP : configuration.get('topP', 1);
        if (typeof topPSetting === 'number' && !Number.isNaN(topPSetting)) {
            request.options = { top_p: topPSetting };
        }
        return this.collectCompletionResult(provider, request);
    }
    async collectCompletionResult(provider, request) {
        let buffer = '';
        for await (const chunk of provider.chat(request)) {
            if (!chunk) {
                continue;
            }
            const content = typeof chunk.message?.content === 'string' ? chunk.message.content : '';
            if (content) {
                buffer += content;
            }
            if (chunk.done) {
                break;
            }
        }
        return buffer.trim();
    }
    extractJsonObject(text) {
        const normalized = typeof text === 'string' ? text.trim() : '';
        if (!normalized) {
            return undefined;
        }
        const candidates = [];
        const fencedJson = normalized.match(/```json\s*([\s\S]*?)```/i);
        if (fencedJson?.[1]) {
            candidates.push(fencedJson[1]);
        }
        const genericFence = normalized.match(/```\s*([\s\S]*?)```/); // fall back to any fenced block
        if (genericFence?.[1]) {
            candidates.push(genericFence[1]);
        }
        const firstBrace = normalized.indexOf('{');
        const lastBrace = normalized.lastIndexOf('}');
        if (firstBrace !== -1 && lastBrace > firstBrace) {
            candidates.push(normalized.slice(firstBrace, lastBrace + 1));
        }
        candidates.push(normalized);
        for (const candidate of Array.from(new Set(candidates))) {
            try {
                const parsed = JSON.parse(candidate);
                if (parsed && typeof parsed === 'object') {
                    return parsed;
                }
            }
            catch {
                // ignore parse errors and continue trying other candidates
            }
        }
        return undefined;
    }
    findNearestUserMessage(messages, referenceId) {
        const index = messages.findIndex((entry) => entry.id === referenceId);
        for (let cursor = index - 1; cursor >= 0; cursor -= 1) {
            const candidate = messages[cursor];
            if (candidate?.role === 'user') {
                return candidate;
            }
        }
        return undefined;
    }
    async handleFeedbackSubmission(messageId, rating) {
        const conversation = this.ensureActiveConversation();
        const index = conversation.messages.findIndex((entry) => entry.id === messageId);
        if (index === -1) {
            return;
        }
        const target = conversation.messages[index];
        if (target.role !== 'assistant') {
            return;
        }
        const updated = {
            ...target,
            feedback: {
                rating,
                submitted: false,
                submittedAt: Date.now()
            }
        };
        conversation.messages[index] = updated;
        this.conversation = conversation.messages;
        await this.persistConversationHistory();
        await this.syncState();
        try {
            await this.sendChatFeedback(updated, rating, conversation);
            conversation.messages[index] = {
                ...updated,
                feedback: {
                    ...(updated.feedback ?? {}),
                    submitted: true,
                    submittedAt: Date.now()
                }
            };
            this.conversation = conversation.messages;
            await this.persistConversationHistory();
            await this.syncState();
            // silent acknowledgement — the thumbs-up/down button state flips visually.
        }
        catch (error) {
            const message = error instanceof Error ? error.message : String(error);
            this.postMessage({ type: 'notification', message: `Unable to send feedback: ${message}` });
        }
    }
    async sendChatFeedback(entry, rating, conversation) {
        const configuration = vscode.workspace.getConfiguration('banditStealth');
        const nearestUser = this.findNearestUserMessage(conversation.messages, entry.id);
        const summary = this.truncateForFeedback(entry.content, 1600);
        const prompt = nearestUser ? this.truncateForFeedback(nearestUser.content, 800) : undefined;
        const descriptionParts = [
            `Rating: ${rating}`,
            `Assistant message:\n${summary}`
        ];
        if (prompt) {
            descriptionParts.push(`User prompt:\n${prompt}`);
        }
        if (entry.intent?.summary) {
            descriptionParts.push(`Intent: ${entry.intent.summary}`);
        }
        const payload = {
            title: rating === 'up' ? 'Chat feedback — positive' : 'Chat feedback — needs improvement',
            description: descriptionParts.join('\n\n'),
            category: rating === 'up' ? 'feature' : 'improvement',
            priority: rating === 'down' ? 'high' : 'medium',
            sessionInfo: { conversationId: this.currentConversationId }
        };
        await this.sendFeedbackRequest(payload, configuration);
    }
    async sendFeedbackRequest(payload, configuration) {
        const feedbackUrl = this.resolveFeedbackUrl(configuration);
        const providerKind = this.getProviderKind(configuration);
        const apiKey = await this.context.secrets.get(API_KEY_SECRET_KEY);
        const trimmedApiKey = apiKey?.trim() ?? '';
        if (providerKind === 'bandit' && trimmedApiKey.length === 0) {
            throw new Error('Bandit API key required.');
        }
        const headers = {
            'Content-Type': 'application/json'
        };
        if (trimmedApiKey.length > 0) {
            headers.Authorization = `Bearer ${trimmedApiKey}`;
        }
        try {
            const response = await fetch(feedbackUrl, {
                method: 'POST',
                headers,
                body: JSON.stringify(payload)
            });
            if (!response.ok) {
                const detail = await response.text().catch(() => '');
                throw new Error(`Feedback request failed: ${response.status} ${response.statusText}${detail ? ` – ${detail}` : ''}`);
            }
        }
        catch (error) {
            if (providerKind === 'bandit' && trimmedApiKey.length > 0) {
                console.warn('Bandit feedback endpoint unavailable, attempting completions fallback.', error);
                await this.submitFeedbackViaCompletions(payload, configuration, trimmedApiKey);
                return;
            }
            throw error instanceof Error ? error : new Error(String(error));
        }
    }
    truncateForFeedback(text, maxLength = 1800) {
        const normalized = typeof text === 'string' ? text.trim() : '';
        if (!normalized) {
            return '';
        }
        if (normalized.length <= maxLength) {
            return normalized;
        }
        return `${normalized.slice(0, maxLength - 1)}…`;
    }
    extractPathFromOutput(output) {
        if (!output) {
            return undefined;
        }
        const match = output.match(/Wrote\s+(.+)/i);
        return match ? match[1].trim() : undefined;
    }
    extractDiffPreviews(report) {
        if (!Array.isArray(report.results)) {
            return [];
        }
        const previews = [];
        for (const result of report.results) {
            const data = result.data;
            const diff = typeof data?.diff === 'string' ? data.diff : undefined;
            const path = typeof data?.path === 'string' ? data.path : this.extractPathFromOutput(result.output);
            if (!diff || !path) {
                continue;
            }
            const backupPath = typeof data?.backupPath === 'string' ? data.backupPath : undefined;
            const backupContent = typeof data?.backupContent === 'string' ? data.backupContent : undefined;
            previews.push({ path, diff, backupPath, backupContent });
            const extras = Array.isArray(data?.additionalWrites)
                ? data.additionalWrites
                : [];
            for (const extra of extras) {
                if (!extra || typeof extra.path !== 'string' || typeof extra.diff !== 'string') {
                    continue;
                }
                previews.push({ path: extra.path, diff: extra.diff, backupPath: undefined, backupContent: undefined });
            }
        }
        return previews;
    }
    async clearDiffPreviewSessions() {
        const sessions = Array.from(this.diffPreviewSessions.values());
        this.diffPreviewSessions.clear();
        await Promise.all(sessions.map((session) => this.disposeDiffPreviewSession(session)));
        this.postMessage({ type: 'diffPreviewClear' });
    }
    async disposeDiffPreviewSession(session) {
        const tabsToClose = [];
        const inlineUri = session.inlineUri?.toString();
        const diffOriginal = session.diffInput?.original.toString();
        const diffModified = session.diffInput?.modified.toString();
        if (inlineUri || (diffOriginal && diffModified)) {
            for (const group of vscode.window.tabGroups.all) {
                for (const tab of group.tabs) {
                    const input = tab.input;
                    if (inlineUri && input instanceof vscode.TabInputText && input.uri.toString() === inlineUri) {
                        tabsToClose.push(tab);
                        continue;
                    }
                    if (diffOriginal &&
                        diffModified &&
                        input instanceof vscode.TabInputTextDiff &&
                        input.original.toString() === diffOriginal &&
                        input.modified.toString() === diffModified) {
                        tabsToClose.push(tab);
                    }
                }
            }
        }
        for (const tab of tabsToClose) {
            try {
                await vscode.window.tabGroups.close(tab);
            }
            catch {
                // ignore failures closing editors
            }
        }
        if (session.inlineUri) {
            this.diffContentProvider.release(session.inlineUri);
        }
    }
    async presentDiffFeedback(report) {
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0]?.uri;
        if (!workspaceFolder) {
            return;
        }
        const previews = this.extractDiffPreviews(report);
        if (previews.length === 0) {
            return;
        }
        this.pendingDiffPreviews = previews;
        await this.clearDiffPreviewSessions();
        for (const preview of previews) {
            this.diffPreviewSessions.set(preview.path, {
                preview,
                workspaceFolder
            });
            this.postMessage({
                type: 'diffPreviewCard',
                preview: {
                    path: preview.path,
                    hasBackup: Boolean(preview.backupPath)
                }
            });
        }
    }
    async handleDiffPreviewAction(message) {
        const session = this.diffPreviewSessions.get(message.path);
        if (!session) {
            this.postMessage({
                type: 'diffPreviewResult',
                path: message.path,
                status: 'error',
                message: 'Change preview is no longer available.'
            });
            return;
        }
        const { preview, workspaceFolder } = session;
        try {
            switch (message.action) {
                case 'apply':
                    await this.submitDiffFeedback(preview, 'apply');
                    await this.cleanupBackup(preview, workspaceFolder);
                    this.postMessage({ type: 'diffPreviewResult', path: message.path, status: 'apply' });
                    this.diffPreviewSessions.delete(message.path);
                    await this.disposeDiffPreviewSession(session);
                    break;
                case 'explain':
                    this.pendingPrompt = `Explain the proposed updates made to ${preview.path}.`;
                    await this.submitDiffFeedback(preview, 'explain');
                    await this.syncState();
                    await this.cleanupBackup(preview, workspaceFolder);
                    this.postMessage({ type: 'diffPreviewResult', path: message.path, status: 'explain' });
                    this.diffPreviewSessions.delete(message.path);
                    await this.disposeDiffPreviewSession(session);
                    break;
                case 'discard':
                    if (preview.backupPath) {
                        await this.restoreFromBackup(preview, workspaceFolder);
                    }
                    await this.submitDiffFeedback(preview, 'discard');
                    this.postMessage({ type: 'diffPreviewResult', path: message.path, status: 'discard' });
                    this.diffPreviewSessions.delete(message.path);
                    await this.disposeDiffPreviewSession(session);
                    break;
                default:
                    this.postMessage({
                        type: 'diffPreviewResult',
                        path: message.path,
                        status: 'error',
                        message: 'Unsupported action.'
                    });
                    return;
            }
        }
        catch (error) {
            this.postMessage({
                type: 'diffPreviewResult',
                path: message.path,
                status: 'error',
                message: error instanceof Error ? error.message : String(error)
            });
        }
    }
    async handleUndoAgentChange() {
        let snapshot = null;
        try {
            snapshot = await this.undoManager.undoLastChange();
        }
        catch (error) {
            const detail = error instanceof Error ? error.message : String(error);
            void vscode.window.showErrorMessage(`Undo failed: ${detail}`);
            this.postMessage({ type: 'notification', message: `Undo failed: ${detail}` });
            return;
        }
        finally {
            this.undoSnapshotsAvailable = this.undoManager.hasSnapshots();
        }
        if (!snapshot) {
            // silent — the undo button disables itself when nothing's restorable.
            await this.syncState();
            return;
        }
        const label = snapshot.path || path.basename(snapshot.absolutePath);
        const message = snapshot.existedBefore
            ? `Reverted changes in ${label}`
            : `Removed ${label}`;
        // silent success — the file in the editor already reflects the undo.
        void vscode.window.showInformationMessage(message);
        await this.syncState();
    }
    async openDiffPreview(preview, workspaceFolder) {
        const inlineUri = this.diffContentProvider.registerDiff(preview.path, preview.diff);
        const inlineDocument = await vscode.workspace.openTextDocument(inlineUri);
        await vscode.languages.setTextDocumentLanguage(inlineDocument, 'markdown');
        await vscode.window.showTextDocument(inlineDocument, {
            preview: true,
            viewColumn: vscode.ViewColumn.Beside
        });
        if (!preview.backupPath) {
            return { inlineUri };
        }
        const originalUri = this.resolveWorkspacePath(workspaceFolder, preview.backupPath);
        const currentUri = this.resolveWorkspacePath(workspaceFolder, preview.path);
        try {
            await vscode.workspace.fs.stat(originalUri);
        }
        catch {
            throw new Error('Original backup not found.');
        }
        await vscode.commands.executeCommand('vscode.diff', originalUri, currentUri, `${preview.path} — Bandit changes`);
        return {
            inlineUri,
            diffInput: {
                original: originalUri,
                modified: currentUri
            }
        };
    }
    async submitDiffFeedback(preview, decision) {
        const configuration = vscode.workspace.getConfiguration('banditStealth');
        const description = [
            `File: ${preview.path}`,
            `Decision: ${decision}`,
            'Diff snippet:',
            this.truncateDiff(preview.diff, 120)
        ].join('\n\n');
        const payload = {
            title: `Diff review — ${decision}`,
            description,
            category: decision === 'apply' ? 'feature' : decision === 'discard' ? 'bug' : 'improvement',
            priority: decision === 'discard' ? 'critical' : decision === 'explain' ? 'medium' : 'medium',
            annoyanceLevel: decision === 'discard' ? 10 : decision === 'explain' ? 4 : 3,
            sessionInfo: { conversationId: this.currentConversationId }
        };
        await this.sendFeedbackRequest(payload, configuration);
    }
    async restoreFromBackup(preview, workspaceFolder) {
        if (!preview.backupPath && typeof preview.backupContent !== 'string') {
            void vscode.window.showWarningMessage(`No backup available for ${preview.path}.`);
            return;
        }
        const targetUri = this.resolveWorkspacePath(workspaceFolder, preview.path);
        const backupUri = preview.backupPath ? this.resolveWorkspacePath(workspaceFolder, preview.backupPath) : undefined;
        try {
            const contentBuffer = backupUri
                ? await vscode.workspace.fs.readFile(backupUri)
                : utf8Encoder.encode(preview.backupContent ?? '');
            const restoredViaEditor = await this.replaceDocumentContents(targetUri, contentBuffer);
            if (!restoredViaEditor) {
                await vscode.workspace.fs.writeFile(targetUri, contentBuffer);
            }
            const current = await vscode.workspace.fs.readFile(targetUri);
            if (!Buffer.from(current).equals(Buffer.from(contentBuffer))) {
                throw new Error('Unable to restore original file contents.');
            }
            if (backupUri) {
                await this.deleteBackupFile(backupUri);
            }
            void vscode.window.showInformationMessage(`Restored ${preview.path} from backup.`);
        }
        catch (error) {
            const message = error instanceof Error ? error.message : String(error);
            void vscode.window.showErrorMessage(`Failed to restore ${preview.path}: ${message}`);
            throw error;
        }
    }
    async replaceDocumentContents(targetUri, content) {
        try {
            const document = await vscode.workspace.openTextDocument(targetUri);
            const edit = new vscode.WorkspaceEdit();
            const fullRange = document.lineCount > 0
                ? new vscode.Range(new vscode.Position(0, 0), document.lineAt(document.lineCount - 1).range.end)
                : new vscode.Range(new vscode.Position(0, 0), new vscode.Position(0, 0));
            edit.replace(targetUri, fullRange, utf8Decoder.decode(content));
            const applied = await vscode.workspace.applyEdit(edit);
            if (applied) {
                const saved = await document.save();
                if (!saved) {
                    await vscode.workspace.fs.writeFile(targetUri, content);
                }
                return true;
            }
        }
        catch {
            // fall through to filesystem write
        }
        try {
            await vscode.workspace.fs.writeFile(targetUri, content);
            await this.revertVisibleEditors(targetUri);
        }
        catch {
            return false;
        }
        return true;
    }
    async deleteBackupFile(uri) {
        try {
            await vscode.workspace.fs.delete(uri, { recursive: false, useTrash: false });
        }
        catch {
            // ignore cleanup failures
        }
    }
    async cleanupBackup(preview, workspaceFolder) {
        if (!preview.backupPath) {
            return;
        }
        const backupUri = this.resolveWorkspacePath(workspaceFolder, preview.backupPath);
        await this.deleteBackupFile(backupUri);
    }
    resolveWorkspacePath(workspaceFolder, relativePath) {
        if (path.isAbsolute(relativePath)) {
            return vscode.Uri.file(relativePath);
        }
        const resolved = path.resolve(workspaceFolder.fsPath, relativePath);
        return vscode.Uri.file(resolved);
    }
    async revertVisibleEditors(targetUri) {
        const targetKey = targetUri.toString();
        const matchingEditors = vscode.window.visibleTextEditors.filter((editor) => editor.document.uri.toString() === targetKey);
        if (!matchingEditors.length) {
            return;
        }
        const previous = vscode.window.activeTextEditor;
        for (const editor of matchingEditors) {
            await vscode.window.showTextDocument(editor.document, { preview: false, preserveFocus: false });
            await vscode.commands.executeCommand('workbench.action.files.revert');
        }
        if (previous && !matchingEditors.includes(previous)) {
            await vscode.window.showTextDocument(previous.document, { preview: false, preserveFocus: true });
        }
    }
    estimateTokenUsage(text) {
        if (!text) {
            return 0;
        }
        const trimmed = text.trim();
        if (!trimmed) {
            return 0;
        }
        return Math.max(1, Math.ceil(trimmed.length / 4));
    }
    extractImagePayload(image) {
        if (typeof image !== 'string') {
            return '';
        }
        const trimmed = image.trim();
        if (!trimmed) {
            return '';
        }
        if (/^data:/i.test(trimmed) || /^https?:/i.test(trimmed)) {
            return trimmed;
        }
        return `data:image/png;base64,${trimmed}`;
    }
    buildSystemPrompt(providerKind, configuration, contextBlock, modelIdOverride, userGoal) {
        const basePrompt = configuration.get('systemPrompt', '').trim();
        let prompt;
        const goalText = userGoal ?? '';
        if (providerKind === 'ollama') {
            const configuredModelId = configuration.get('ollamaModel', 'gemma3:12b') ?? 'gemma3:12b';
            const modelId = (modelIdOverride && modelIdOverride.trim().length > 0 ? modelIdOverride : configuredModelId).trim();
            const caps = (0, stealth_core_runtime_1.getModelCapabilities)(modelId);
            const modelLower = modelId.toLowerCase();
            let ollamaIdentityPrompt;
            if (caps.tier === 'small') {
                // Small / 4B models: keep it short — every token costs more at low context windows.
                ollamaIdentityPrompt = [
                    'You are Bandit Stealth, a concise coding assistant inside VS Code built by Burtson Labs LLC.',
                    'When asked who you are, always say "I am Bandit Stealth" — never mention Gemma, Llama, or any underlying model.',
                    'Give direct, focused answers. Prefer small targeted edits over rewrites.'
                ].join('\n');
            }
            else if (modelLower.startsWith('llama') || modelLower.startsWith('qwen') || modelLower.startsWith('deepseek')) {
                // Llama / Qwen / DeepSeek — instruction format works best with explicit task framing.
                ollamaIdentityPrompt = [
                    'You are Bandit Stealth, an expert coding assistant embedded in VS Code, built by Burtson Labs LLC.',
                    'When asked who you are, always identify yourself as Bandit Stealth — never reveal the underlying model name.',
                    'Never answer as Qwen, Llama, or DeepSeek. Always speak in first-person as Bandit Stealth.',
                    'When answering:',
                    '- Reference file paths and line numbers when relevant.',
                    '- Prefer targeted, minimal edits over full rewrites.',
                    '- If a question is ambiguous, ask one clarifying question before proceeding.',
                    '- Format code in fenced blocks with the correct language tag.'
                ].join('\n');
            }
            else {
                // gemma3 / gemma4 / bandit-core fine-tunes — tool-aware but
                // tight. The earlier version of this prompt aggressively
                // advertised skill creation (`.bandit/skills/<name>.md`), which
                // medium-size models latched onto literally — e.g. answering
                // "add comments to api controllers" by writing a skill file
                // instead of editing the controllers. Skill-creation guidance
                // is now injected on-demand (see userGoal heuristic below) so
                // the default prompt stays focused on the actual task:
                // read/search/edit/run code. Language-agnostic on purpose —
                // users have reported refusals on C# + Python when the prompt
                // implied a TypeScript-only context.
                const wantsSkillGuide = /\b(skills?)\b/i.test(goalText);
                const lines = [
                    'You are Bandit Stealth, an expert coding agent developed by Burtson Labs LLC.',
                    'You run inside VS Code. You help users across any language, framework, or runtime present in the workspace — read, search, debug, edit, and run code as needed.',
                    'When asked who you are, say you are Bandit Stealth — do not identify as Gemma or any base model.',
                    '',
                    'You have tools. Use them to accomplish the task — never refuse because of supposed language or environment limitations; the workspace dictates the stack.',
                    'Call tools by outputting: <tool_call>{"name": "tool_name", "params": {"key": "value"}}</tool_call>',
                    'Call one tool at a time. Wait for results. Read files before modifying them.',
                    'NEVER emit `<tool_result>` in your response — those envelopes are SYSTEM output injected BETWEEN your turns. You only emit `<tool_call>`. If you invent a `<tool_result>` the tool did not actually run; your apparent "success" is a hallucination.',
                    'NEVER paste your todo list as a ```json fenced block. Call the `todo_write` tool directly: <tool_call>{"name":"todo_write","params":{"items":"[{\\"content\\":\\"...\\",\\"status\\":\\"pending\\"}]"}}</tool_call>. Pasted JSON does not update your plan — only the tool call does. If you keep pasting JSON instead of calling the tool, the model will iterate on the same task forever because its plan state never advances.',
                    '',
                    'Guidelines:',
                    '- Cite file paths and line numbers when referencing code.',
                    '- Prefer small, targeted edits over large rewrites.',
                    '- When uncertain, ask a clarifying question rather than guessing.',
                    '- Format code in fenced blocks with the correct language identifier.'
                ];
                if (wantsSkillGuide) {
                    lines.push('', 'Skill authoring: when asked to create or update a skill, write markdown with YAML frontmatter to .bandit/skills/<name>.md. Skills are loaded automatically. Do not use the legacy JSON format.');
                }
                ollamaIdentityPrompt = lines.join('\n');
            }
            // Always inject brand/identity guardrails for Ollama even when a custom systemPrompt exists.
            prompt = basePrompt.length === 0 ? ollamaIdentityPrompt : `${basePrompt}\n${ollamaIdentityPrompt}`;
        }
        else {
            // Bandit hosted API — identity prompt overrides default. Never reveal underlying model.
            const brandContext = [
                'You are Bandit Stealth, an expert AI coding agent developed by Burtson Labs LLC.',
                'Only if the user explicitly asks who you are, identify yourself as "Bandit Stealth."',
                'Do not self-introduce unless asked, and never mention any underlying base model name.',
                'You run inside VS Code and help users understand, write, debug, and refactor code.',
                '',
                'You have tools available. Use them — do not just describe what you would do.',
                'To call a tool: <tool_call>{"name": "tool_name", "params": {"key": "value"}}</tool_call>',
                'NEVER emit `<tool_result>` in your response — those envelopes are SYSTEM output injected BETWEEN your turns. You only emit `<tool_call>`. Inventing a `<tool_result>` means the tool did not actually run; your apparent "success" is a hallucination.',
                'Read files before modifying them. When writing files, include complete content.',
                '',
                'When asked to create a "skill" for Bandit, write a MARKDOWN file to .bandit/skills/<name>.md using write_file. DO NOT create VS Code tasks, launch configs, or JSON skill files (the old JSON schema is deprecated). Skills are context packages — the markdown body tells the agent when to use existing tools (run_command, git_*, etc).',
                'Shape: `---\\nid: <name>\\nname: <Name>\\ndescription: When to use this skill\\nactivation: auto\\ntriggers: [<keyword>, <keyword>]\\n---\\n\\n# <Name>\\n\\n<playbook prose: which commands to run, when, in what order>`',
                'After writing the file, confirm it was created and explain how to trigger it.',
                '',
                'Cite file paths when referencing code. Format code in fenced blocks with language tags.'
            ].join('\n');
            prompt = basePrompt.length === 0 ? brandContext : `${basePrompt}\n${brandContext}`;
        }
        if (contextBlock && contextBlock.trim().length > 0) {
            prompt = prompt ? `${prompt}\n\n${contextBlock}` : contextBlock;
        }
        return prompt;
    }
    /**
     * Builds a codebase context block for the current user message.
     * Uses GatewaySearchAdapter (Tier 1) if configured, falls back to local
     * OllamaEmbeddingClient (Tier 2). Returns empty string when no context found.
     */
    async buildContextBlock(userMessage, configuration) {
        if (!userMessage.trim())
            return undefined;
        const gatewayUrl = configuration.get('gatewayUrl', '');
        const workspaceId = configuration.get('workspaceId', '');
        const embeddingProvider = configuration.get('embeddings.provider', 'ollama');
        let gateway;
        if (gatewayUrl && workspaceId) {
            const apiKey = await Promise.resolve(this.context.secrets.get(API_KEY_SECRET_KEY)).catch(() => undefined);
            if (apiKey) {
                gateway = new stealth_core_runtime_1.GatewaySearchAdapter({ gatewayUrl, apiKey, workspaceId });
            }
        }
        let localEmbeddings;
        if (embeddingProvider === 'ollama') {
            const ollamaUrl = configuration.get('ollamaBaseUrl', '') ||
                configuration.get('ollamaUrl', 'http://localhost:11434') ||
                'http://localhost:11434';
            const embedModel = configuration.get('embeddings.ollamaModel', 'nomic-embed-text');
            // Reuse cached client if settings unchanged; recreate if they changed.
            const currentUrl = this.localEmbeddingClient?.['baseUrl'];
            if (!this.localEmbeddingClient || currentUrl !== ollamaUrl) {
                this.localEmbeddingClient = new stealth_core_runtime_1.OllamaEmbeddingClient({ baseUrl: ollamaUrl, model: embedModel });
            }
            localEmbeddings = this.localEmbeddingClient;
        }
        if (!gateway && !localEmbeddings)
            return undefined;
        // Index the current open file into local embeddings (Tier 2) before searching.
        const editor = vscode.window.activeTextEditor;
        const currentFilePath = editor?.document.uri.fsPath;
        const currentFileContent = editor?.document.getText();
        if (localEmbeddings && currentFilePath && currentFileContent) {
            await localEmbeddings.upsertFile(currentFilePath, currentFileContent).catch(() => undefined);
        }
        const recentUserEntry = [...this.conversation]
            .reverse()
            .find((entry) => entry.role === 'user');
        const hasRecentImages = Boolean(recentUserEntry?.images?.length);
        const modelId = this.getProviderKind(configuration) === 'ollama'
            ? this.resolveChatModel(configuration, hasRecentImages)
            : configuration.get('model', 'bandit-core-1');
        // Inject git-modified files as pinned context so the model always sees
        // what the user is actively changing, even before embeddings index them.
        const gitPinnedFiles = await this.getGitModifiedFiles();
        const builder = new stealth_core_runtime_1.ContextBuilder(gateway, localEmbeddings);
        const result = await builder.build(userMessage, {
            modelId,
            currentFilePath,
            currentFileContent,
            pinnedFiles: gitPinnedFiles,
            workspaceId: workspaceId || undefined
        });
        // Publish context budget for status bar display.
        const caps = (0, stealth_core_runtime_1.getModelCapabilities)(modelId);
        const budget = { tokenEstimate: result.tokenEstimate, contextWindow: caps.contextWindow, source: result.source };
        this.lastContextBudget = budget;
        this._onDidChangeStatus.fire({ busy: this.isBusy, text: this.statusText, contextBudget: budget });
        return result;
    }
    /**
     * Returns up to 5 git-modified (added/modified) files as pinned context entries.
     * Runs `git diff --name-only HEAD` synchronously in the workspace root.
     * Silently returns an empty array when git is unavailable or the workspace has no repo.
     */
    async getGitModifiedFiles() {
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
        if (!workspaceRoot)
            return [];
        const git = (0, child_process_1.spawnSync)('git', ['diff', '--name-only', '--diff-filter=AM', 'HEAD'], {
            cwd: workspaceRoot,
            encoding: 'utf8'
        });
        if (git.status !== 0 || !git.stdout)
            return [];
        const relativePaths = git.stdout
            .trim()
            .split('\n')
            .map(p => p.trim())
            .filter(Boolean)
            .slice(0, 5);
        const pinned = [];
        for (const relPath of relativePaths) {
            try {
                const absUri = vscode.Uri.file(path.join(workspaceRoot, relPath));
                const bytes = await vscode.workspace.fs.readFile(absUri);
                pinned.push({ path: relPath, content: Buffer.from(bytes).toString('utf8') });
            }
            catch {
                // Skip files that can't be read (deleted, binary, permission denied, etc.)
            }
        }
        return pinned;
    }
    getProviderKind(configuration) {
        const rawProvider = configuration.get('provider', 'ollama');
        const normalized = typeof rawProvider === 'string' ? rawProvider.trim().toLowerCase() : 'ollama';
        if (normalized === 'ollama') {
            return 'ollama';
        }
        return 'bandit';
    }
    normalizeConfiguredModel(modelValue, fallback) {
        const normalized = typeof modelValue === 'string' ? modelValue.trim() : '';
        if (normalized.length > 0) {
            return normalized;
        }
        return fallback;
    }
    isOllamaAutoRoutingEnabled(configuration) {
        return configuration.get('ollamaAutoRouteModels', true) !== false;
    }
    resolveOllamaBaseModel(configuration) {
        return this.normalizeConfiguredModel(configuration.get('ollamaModel', 'gemma3:12b'), 'gemma3:12b');
    }
    resolveOllamaCodingModel(configuration) {
        const explicitCodingModel = this.normalizeConfiguredModel(configuration.get('ollamaCodingModel', ''), '');
        if (explicitCodingModel) {
            return explicitCodingModel;
        }
        const explicitAgentModel = this.normalizeConfiguredModel(configuration.get('agentOllamaModel', ''), '');
        if (explicitAgentModel) {
            return explicitAgentModel;
        }
        return this.resolveOllamaBaseModel(configuration);
    }
    resolveOllamaVisionModel(configuration) {
        const explicitVisionModel = this.normalizeConfiguredModel(configuration.get('ollamaVisionModel', ''), '');
        if (explicitVisionModel) {
            return explicitVisionModel;
        }
        return this.resolveOllamaBaseModel(configuration);
    }
    resolveChatModel(configuration, hasImages) {
        if (this.getProviderKind(configuration) !== 'ollama') {
            return this.normalizeConfiguredModel(configuration.get('model', 'bandit-core-1'), 'bandit-core-1');
        }
        if (!this.isOllamaAutoRoutingEnabled(configuration)) {
            return this.resolveOllamaBaseModel(configuration);
        }
        return hasImages
            ? this.resolveOllamaVisionModel(configuration)
            : this.resolveOllamaCodingModel(configuration);
    }
    resolveAgentModel(configuration) {
        if (this.getProviderKind(configuration) !== 'ollama') {
            return this.normalizeConfiguredModel(configuration.get('model', 'bandit-core-1'), 'bandit-core-1');
        }
        const explicitAgentModel = this.normalizeConfiguredModel(configuration.get('agentOllamaModel', ''), '');
        if (explicitAgentModel) {
            return explicitAgentModel;
        }
        if (!this.isOllamaAutoRoutingEnabled(configuration)) {
            return this.resolveOllamaBaseModel(configuration);
        }
        return this.resolveOllamaCodingModel(configuration);
    }
    modelSupportsVision(modelId) {
        const normalizedModelId = modelId.trim().toLowerCase();
        if (!normalizedModelId) {
            return false;
        }
        if ((0, stealth_core_runtime_1.getModelCapabilities)(normalizedModelId).supportsVision) {
            return true;
        }
        return normalizedModelId.includes('vision')
            || normalizedModelId.includes('llava')
            || normalizedModelId.includes('-vl')
            || normalizedModelId.includes('vl:')
            || normalizedModelId.startsWith('gemma3:')
            || normalizedModelId.startsWith('gemma4:')
            || normalizedModelId.startsWith('gemma4');
    }
    canUseInlineImages(configuration, modelId) {
        const provider = this.getProviderKind(configuration);
        if (provider === 'bandit') {
            const model = this.normalizeConfiguredModel(modelId ?? configuration.get('model', 'bandit-core-1'), 'bandit-core-1');
            return model.toLowerCase().startsWith('bandit-core');
        }
        if (provider === 'ollama') {
            const candidateModel = this.normalizeConfiguredModel(modelId, this.resolveOllamaVisionModel(configuration));
            return this.modelSupportsVision(candidateModel);
        }
        return false;
    }
    describeProvider(kind) {
        switch (kind) {
            case 'ollama':
                return 'Ollama';
            default:
                return 'Bandit AI';
        }
    }
    arePlanArtifactsEnabled() {
        const configuration = vscode.workspace.getConfiguration('banditStealth');
        return configuration.get('debug.emitPlanJson', true);
    }
    buildProviderSettings(configuration, apiKey, ollamaAuthToken) {
        const DEFAULT_OLLAMA_URL = 'http://localhost:11434';
        const rawHeaders = configuration.get('ollamaHeaders', {}) || {};
        const cleanHeaders = {};
        for (const [key, value] of Object.entries(rawHeaders)) {
            if (!key || typeof key !== 'string')
                continue;
            if (key.toLowerCase() === 'content-type')
                continue; // always forced by provider
            if (typeof value === 'string' && value.length > 0)
                cleanHeaders[key] = value;
        }
        // Auto-inject the secrets-stored Authorization header when present —
        // but ONLY if the user hasn't already declared an explicit
        // Authorization header in settings. Explicit config wins so custom
        // schemes (Basic, PrivateToken, etc.) aren't overridden.
        const hasExplicitAuth = Object.keys(cleanHeaders).some(k => k.toLowerCase() === 'authorization');
        if (ollamaAuthToken && !hasExplicitAuth) {
            cleanHeaders['Authorization'] = `Bearer ${ollamaAuthToken}`;
        }
        return {
            kind: this.getProviderKind(configuration),
            apiKey,
            apiUrl: configuration.get('apiUrl', 'https://api.burtson.ai/completions'),
            // ollamaBaseUrl is the new primary; ollamaUrl is the legacy alias
            ollamaUrl: configuration.get('ollamaBaseUrl', '') ||
                configuration.get('ollamaUrl', DEFAULT_OLLAMA_URL) ||
                DEFAULT_OLLAMA_URL,
            ollamaNodeUrl: configuration.get('ollamaNodeUrl', '') || undefined,
            ollamaModel: this.resolveOllamaBaseModel(configuration),
            ollamaHeaders: Object.keys(cleanHeaders).length > 0 ? cleanHeaders : undefined
        };
    }
    async setBusy(value, message) {
        this.isBusy = value;
        if (typeof message === 'string') {
            this.statusText = message;
        }
        else if (!value) {
            this.statusText = 'Ready';
        }
        this._onDidChangeStatus.fire({ busy: this.isBusy, text: this.statusText, contextBudget: this.lastContextBudget });
        await this.syncState();
    }
    async refreshAccountProfile() {
        const configuration = vscode.workspace.getConfiguration('banditStealth');
        const providerKind = this.getProviderKind(configuration);
        if (providerKind !== 'bandit') {
            this.accountProfile = null;
            this.accountProfileError = null;
            this.accountProfileStatus = 'idle';
            await this.syncState();
            return;
        }
        const apiKey = await this.context.secrets.get(API_KEY_SECRET_KEY);
        if (!apiKey) {
            this.accountProfile = null;
            this.accountProfileError = null;
            this.accountProfileStatus = 'idle';
            await this.syncState();
            return;
        }
        this.accountProfileStatus = 'loading';
        this.accountProfileError = null;
        await this.syncState();
        try {
            const controller = new AbortController();
            const timeout = setTimeout(() => controller.abort(), 6000);
            const url = `https://auth.burtson.ai/api/keys/validate?key=${encodeURIComponent(apiKey)}`;
            const response = await fetch(url, {
                method: 'GET',
                headers: {
                    Accept: 'application/json'
                },
                signal: controller.signal
            });
            clearTimeout(timeout);
            if (!response.ok) {
                const text = await response.text().catch(() => '');
                throw new Error(text || `Validation failed (${response.status})`);
            }
            const payload = (await response.json());
            this.accountProfile = payload;
            this.accountProfileStatus = 'idle';
            this.accountProfileError = null;
        }
        catch (error) {
            const message = error instanceof Error ? error.message : String(error);
            this.accountProfile = null;
            this.accountProfileStatus = 'error';
            this.accountProfileError = message;
        }
        await this.syncState();
    }
    async setStatusMessage(message) {
        this.statusText = message;
        this._onDidChangeStatus.fire({ busy: this.isBusy, text: this.statusText, contextBudget: this.lastContextBudget });
        await this.syncState();
    }
    /**
     * Build the skill list the composer's `/` picker shows. Reuses the same
     * registry the tool-use loop instantiates per turn so the picker reflects
     * exactly what the agent would activate. Built-in skills are identified by
     * ids that match the curated set from `createDefaultSkillRegistry`; everything
     * else comes from `.bandit/skills/` in the workspace.
     */
    async sendSkillList() {
        const BUILTIN_SKILL_IDS = new Set([
            'core/filesystem',
            'core/git',
            'review/code-review',
            'testing/test-gen',
            'agent/plan',
            'search/semantic'
        ]);
        try {
            const registry = (0, agent_core_1.createDefaultSkillRegistry)();
            const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
            if (workspaceRoot) {
                const toolCtx = new nodeToolContext_1.NodeToolExecutionContext(workspaceRoot, (0, agent_core_1.createDefaultLanguageAdapters)());
                await (0, agent_core_1.registerWorkspaceSkills)(registry, (pattern, cwd) => toolCtx.listFiles(pattern, cwd), (absPath) => toolCtx.readFile(absPath), workspaceRoot).catch(() => 0);
            }
            const skills = registry.getAll().map((skill) => ({
                id: skill.id,
                name: skill.name,
                description: skill.description,
                source: BUILTIN_SKILL_IDS.has(skill.id) ? 'builtin' : 'workspace'
            }));
            // Sort: built-ins first (preserving default order), workspace second (alphabetical by id).
            const builtin = skills.filter((s) => s.source === 'builtin');
            const workspace = skills
                .filter((s) => s.source === 'workspace')
                .sort((a, b) => a.id.localeCompare(b.id));
            this.postMessage({ type: 'skillList', skills: [...builtin, ...workspace] });
        }
        catch (error) {
            console.warn('sendSkillList failed', error);
            this.postMessage({ type: 'skillList', skills: [] });
        }
    }
    /**
     * Replace the native permission modal with an in-chat card. The webview
     * renders the card and posts a permissionResponse when the user clicks;
     * the Promise we return resolves with their choice.
     *
     * The card is injected into the assistantEntry content as a fenced JSON
     * payload that the markdown renderer extracts into an interactive React
     * component. Once the user chooses, the payload is replaced in-place
     * with a resolved summary so the history stays clean.
     */
    requestPermissionInChat(req) {
        const id = `perm-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 6)}`;
        const payload = {
            type: 'bandit:permission',
            id,
            tool: req.tool,
            primary: req.primary,
            description: req.description,
            bodyPreview: req.bodyPreview ?? ''
        };
        if (req.warning)
            payload.warning = req.warning;
        if (req.diffStats)
            payload.diffStats = req.diffStats;
        // Serialize into the assistant entry as a fenced JSON block so it
        // survives the existing markdown-render pipeline. ChatMessage detects
        // this type and swaps to the interactive card component.
        //
        // Clean any live thinking / tool-call-gen markers off the tail first.
        // Without this, a pending "_⟳ pondering…_" marker lands BETWEEN the
        // prior content and the fenced permission block — subsequent marker
        // ticks strip only the last-anchored marker and then keep appending
        // new ones AFTER the permission fence, which has been observed to
        // visually swamp the card on slow renders. Stripping up-front keeps
        // the card at the tail where the user's eye is looking.
        const THINKING_MARKER_RE = /\n*`⟳ (?:[a-z]+)…`\s*$/;
        const TOOL_CALL_GEN_MARKER_RE = /\n*`⟳ generating tool call(?:[^`]*)`\s*$/;
        req.assistantEntry.content = req.assistantEntry.content
            .replace(THINKING_MARKER_RE, '')
            .replace(TOOL_CALL_GEN_MARKER_RE, '');
        const marker = `\n\n\`\`\`bandit-permission\n${JSON.stringify(payload)}\n\`\`\`\n`;
        req.assistantEntry.content += marker;
        req.assistantEntry.payload = req.assistantEntry.content;
        console.info(`[bandit] permission card injected: id=${id} tool=${req.tool} primary=${req.primary}`);
        void this.syncState();
        // Also post a direct message so the webview can flash focus, play a
        // sound, etc. if desired. The payload-in-content covers the render;
        // this is the notification channel.
        this.postMessage({
            type: 'permissionRequest',
            id,
            tool: req.tool,
            primary: req.primary,
            description: req.description,
            bodyPreview: req.bodyPreview
        });
        return new Promise((resolve) => {
            this.pendingPermissions.set(id, (choice, notes) => {
                this.pendingPermissions.delete(id);
                // Replace the live card with a resolved summary so the conversation
                // history reads cleanly on resume / reload.
                const resolvedMarker = this.buildResolvedPermissionMarker(req.tool, req.primary, choice, notes);
                req.assistantEntry.content = req.assistantEntry.content.replace(marker, resolvedMarker);
                req.assistantEntry.payload = req.assistantEntry.content;
                void this.syncState();
                resolve({ choice, notes });
            });
        });
    }
    buildResolvedPermissionMarker(tool, primary, choice, notes) {
        const label = choice === 'deny' ? '✗ denied' : choice === 'save' ? '✓ always allow (saved)' : choice === 'session' ? '✓ allowed for session' : '✓ allowed once';
        // Compact absolute paths to workspace-relative before embedding in the
        // marker — otherwise a long path like /Users/mark/Documents/GitHub/
        // S3Api/S3Api/Controllers/FileController.cs sits on one line inside
        // inline-code (no wrap) and forces the chat pane to grow a horizontal
        // scrollbar that eats the whole conversation layout.
        const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath ?? '';
        const compactPrimary = primary ? compactToolDisplayParam(primary, workspaceRoot) : '';
        const target = compactPrimary ? `\`${compactPrimary}\`` : '';
        // When the user denied with notes, surface them in the history marker
        // so a scrollback of the conversation explains WHY the tool was
        // blocked. Useful for replay, debugging, and later code review.
        const tail = choice === 'deny' && notes ? ` — "${notes.replace(/"/g, '\\"')}"` : '';
        // Build the inner text cleanly so markdown italic markers don't end
        // up adjacent to a trailing space (e.g. `_foo _`) — markdown-it
        // rejects that as an emphasis run and renders the underscores as
        // literal chars. Seen 2026-04-22 on the Gemma 4 trace when an
        // apply_edit was invoked with no `path` param, making `target`
        // empty and leaving `_✓ allowed once: apply_edit _` in the feed.
        const parts = [`${label}:`, tool];
        if (target)
            parts.push(target);
        const body = parts.join(' ') + tail;
        return `\n\n_${body}_\n`;
    }
    async flushState() {
        if (!this.view) {
            return;
        }
        const configuration = vscode.workspace.getConfiguration('banditStealth');
        const providerKind = this.getProviderKind(configuration);
        const storedApiKey = await this.context.secrets.get(API_KEY_SECRET_KEY);
        const hasStoredApiKey = Boolean(storedApiKey);
        const requiresApiKey = providerKind !== 'ollama';
        const hasApiKey = requiresApiKey ? hasStoredApiKey : true;
        const storedOllamaAuth = await Promise.resolve(this.context.secrets.get(OLLAMA_AUTH_SECRET_KEY)).catch(() => undefined);
        const hasOllamaAuthToken = Boolean(storedOllamaAuth);
        const currentConversation = this.getCurrentConversation();
        const currentConversationName = currentConversation?.name
            ?? (this.conversation.length > 0
                ? deriveConversationNameFromEntries(this.conversation, 'Recents')
                : 'Recents');
        this.currentIntent = this.findLatestIntent(this.conversation);
        const nonEmptyConversations = this.getSortedConversations(true).filter((conversation) => conversation.messages.length > 0);
        const activeConversationIncluded = nonEmptyConversations.some((conversation) => conversation.id === this.currentConversationId);
        const shouldForceWorkspaceView = !hasApiKey || nonEmptyConversations.length === 0;
        if (shouldForceWorkspaceView && this.historyVisible) {
            this.historyVisible = false;
        }
        const isDeveloperMode = this.context.extensionMode === vscode.ExtensionMode.Development;
        const skipValidationInDev = configuration.get('agent.skipValidationInDev', false) ?? false;
        const state = {
            messages: this.conversation,
            hasApiKey,
            hasStoredApiKey,
            requiresApiKey,
            isBusy: this.isBusy,
            presetPrompt: this.pendingPrompt,
            statusText: this.statusText,
            provider: providerKind,
            model: configuration.get('model', 'bandit-core-1') ?? 'bandit-core-1',
            ollamaModel: configuration.get('ollamaModel', 'gemma3:12b') ?? 'gemma3:12b',
            ollamaUrl: configuration.get('ollamaBaseUrl', '') ||
                configuration.get('ollamaUrl', 'http://localhost:11434') ||
                'http://localhost:11434',
            hasOllamaAuthToken,
            extensionVersion: this.context.extension?.packageJSON?.version ?? 'unknown',
            currentConversationId: activeConversationIncluded ? this.currentConversationId : undefined,
            currentConversationName,
            history: this.getRecentConversationSummaries(nonEmptyConversations),
            hasArchivedConversations: this.hasArchivedConversations(),
            showHistory: this.historyVisible,
            allowImageUploads: this.isInlineImageEnabled(configuration),
            showIntentChips: false,
            feedbackEnabled: configuration.get('feedback.enabled', true) ?? true,
            contextUsage: this.calculateContextUsage(configuration) ?? null,
            undoAvailable: this.undoSnapshotsAvailable,
            mode: 'agent',
            intentInsight: this.currentIntent ?? null,
            intentSuggestions: []
        };
        const planSnapshot = this.getPlanSnapshot(currentConversation);
        state.plan = planSnapshot.plan;
        state.planUpdates = planSnapshot.updates;
        state.planUnread = false;
        state.activePlanRunId = this.activePlanRunId ?? null;
        state.planHistory = this.serializePlanRuns(currentConversation?.planRuns ?? []);
        state.debugEmitPlanJson = configuration.get('debug.emitPlanJson', true) ?? true;
        state.enableToolUse = configuration.get('enableToolUse', true) ?? true;
        state.createBranchBeforeRun = configuration.get('agent.createBranchBeforeRun', false) ?? false;
        state.autoApproveEdits = configuration.get('agent.autoApproveEdits', false) ?? false;
        state.ollamaStatus = this.ollamaStatus;
        state.ollamaModelMissing = this.ollamaModelMissing;
        state.accountProfile = this.accountProfile ?? null;
        state.accountProfileStatus = this.accountProfileStatus;
        state.accountProfileError = this.accountProfileError;
        state.developerMode = isDeveloperMode;
        state.skipValidationInDev = skipValidationInDev;
        this.pendingPrompt = undefined;
        this.postMessage({ type: 'state', state });
        if (this.pendingOpenSettings) {
            this.postMessage({ type: 'openSettings' });
            this.pendingOpenSettings = false;
        }
    }
    async syncState() {
        if (this.syncScheduled) {
            return this.syncPromise ?? Promise.resolve();
        }
        this.syncScheduled = true;
        this.syncPromise = new Promise((resolve) => {
            setTimeout(() => {
                this.syncScheduled = false;
                void this.flushState()
                    .catch((error) => {
                    console.warn('State sync failed', error);
                })
                    .finally(() => {
                    resolve();
                });
            }, 60);
        });
        return this.syncPromise;
    }
    postMessage(message) {
        this.view?.webview.postMessage(message);
    }
    cancelActiveStream() {
        const iterator = this.activeStream;
        if (!iterator) {
            return;
        }
        this.activeStream = undefined;
        if (typeof iterator.return === 'function') {
            void iterator.return().catch(() => {
                // ignore cancellation errors
            });
        }
    }
    async openFileFromWorkspacePath(relativePath) {
        const normalized = typeof relativePath === 'string' ? relativePath.trim() : '';
        if (!normalized) {
            this.postMessage({ type: 'notification', message: 'Diff path unavailable.' });
            return;
        }
        const workspace = vscode.workspace.workspaceFolders?.[0];
        if (!workspace) {
            this.postMessage({ type: 'notification', message: 'Open a workspace to preview diffs.' });
            return;
        }
        const cleaned = normalized.replace(/^[\\/]+/, '');
        const target = vscode.Uri.joinPath(workspace.uri, cleaned);
        try {
            const document = await vscode.workspace.openTextDocument(target);
            await vscode.window.showTextDocument(document, { preview: true });
        }
        catch (error) {
            console.warn('Unable to open diff path', cleaned, error);
            this.postMessage({ type: 'notification', message: `Unable to open ${normalized}.` });
        }
    }
    handleAgentEnvironmentMessage(message) {
        this.agentActivityQueue = this.agentActivityQueue
            .then(async () => {
            await this.applyAgentEnvironmentMessage(message);
        })
            .catch((error) => {
            console.warn('Failed to update agent activity', error);
        });
    }
    async applyAgentEnvironmentMessage(message) {
        if (!message || typeof message !== 'object') {
            return;
        }
        const payload = message;
        const type = typeof payload.type === 'string' ? payload.type : '';
        if (!type.startsWith('agent:')) {
            return;
        }
        if (type === 'agent:plan') {
            const planPayload = payload;
            this.planStates.clear();
            const conversation = this.ensureActiveConversation();
            const planData = planPayload.plan && Array.isArray(planPayload.plan.steps) && planPayload.plan.steps.length > 0
                ? this.clonePlan(planPayload.plan)
                : null;
            let history = [];
            const artifactsEnabled = this.arePlanArtifactsEnabled();
            if (planData) {
                const runId = this.createPlanRunId();
                const run = {
                    id: runId,
                    goal: planData.goal,
                    plan: planData,
                    createdAt: Date.now(),
                    updatedAt: Date.now(),
                    updates: {},
                    artifactsPath: artifactsEnabled ? this.buildPlanArtifactsPath(conversation.id, runId) : undefined
                };
                if (!Array.isArray(conversation.planRuns)) {
                    conversation.planRuns = [];
                }
                conversation.planRuns.push(run);
                const maxRuns = 10;
                if (conversation.planRuns.length > maxRuns) {
                    conversation.planRuns = conversation.planRuns.slice(conversation.planRuns.length - maxRuns);
                }
                conversation.updatedAt = Date.now();
                this.activePlan = planData;
                this.activePlanRunId = runId;
                this.syncPlanStateFromConversation(conversation);
                environmentService_1.environmentService.setRunContext({
                    conversationId: conversation.id,
                    conversationName: conversation.name,
                    runId
                });
                void this.persistConversationHistory();
                history = this.serializePlanRuns(conversation.planRuns);
            }
            else {
                this.resetPlanState();
                environmentService_1.environmentService.setRunContext({
                    conversationId: conversation.id,
                    conversationName: conversation.name,
                    runId: undefined
                });
                history = this.serializePlanRuns(conversation.planRuns ?? []);
            }
            this.postMessage({
                type: 'agentPlan',
                plan: planData ?? planPayload.plan,
                history,
                activeRunId: this.activePlanRunId ?? null
            });
            this.postMessage({
                type: 'agentPlanHistory',
                history,
                activeRunId: this.activePlanRunId ?? null
            });
            return;
        }
        if (type === 'agent:planUpdate') {
            const updatePayload = payload;
            if (typeof updatePayload.stepId !== 'string') {
                return;
            }
            const stepUpdate = {
                summary: typeof updatePayload.meta?.summary === 'string' ? updatePayload.meta.summary : undefined,
                durationMs: typeof updatePayload.meta?.durationMs === 'number' ? updatePayload.meta.durationMs : undefined,
                tokens: typeof updatePayload.meta?.tokens === 'number' ? updatePayload.meta.tokens : undefined
            };
            if (typeof updatePayload.state === 'string') {
                stepUpdate.state = updatePayload.state;
            }
            const merged = this.updatePlanRunStep(updatePayload.stepId, stepUpdate, { emitHistory: false });
            const conversation = this.getCurrentConversation();
            const history = this.serializePlanRuns(conversation?.planRuns ?? []);
            this.postMessage({
                type: 'agentPlanUpdate',
                stepId: updatePayload.stepId,
                status: merged?.state ?? updatePayload.state,
                meta: {
                    summary: merged?.summary ?? updatePayload.meta?.summary,
                    durationMs: merged?.durationMs ?? updatePayload.meta?.durationMs,
                    tokens: merged?.tokens ?? updatePayload.meta?.tokens
                },
                history,
                activeRunId: this.activePlanRunId ?? null
            });
            this.postMessage({
                type: 'agentPlanHistory',
                history,
                activeRunId: this.activePlanRunId ?? null
            });
            return;
        }
        if (type === 'agent:telemetry') {
            const telemetry = payload;
            if (typeof telemetry.stepId === 'string' && telemetry.stepId.length > 0) {
                const update = {
                    durationMs: typeof telemetry.durationMs === 'number' ? telemetry.durationMs : undefined,
                    tokens: typeof telemetry.tokens === 'number' ? telemetry.tokens : undefined
                };
                this.updatePlanRunStep(telemetry.stepId, update);
            }
            this.postMessage({ type: 'agentTelemetry', telemetry });
            return;
        }
        if (type === 'agent:final') {
            const finalPayload = payload;
            const evaluation = finalPayload.report?.evaluation;
            if (!evaluation) {
                return;
            }
            const conversation = this.getCurrentConversation();
            const run = this.getActivePlanRun(conversation);
            if (run) {
                run.evaluation = {
                    success: evaluation.success,
                    confidence: evaluation.confidence,
                    feedback: evaluation.feedback
                };
                run.completedAt = Date.now();
                run.updatedAt = Date.now();
                void this.persistConversationHistory();
                const history = this.serializePlanRuns(conversation?.planRuns ?? []);
                this.postMessage({
                    type: 'agentPlanHistory',
                    history,
                    activeRunId: this.activePlanRunId ?? null
                });
            }
            const confidence = Number.isFinite(evaluation.confidence)
                ? ` (confidence ${(evaluation.confidence * 100).toFixed(1)}%)`
                : '';
            const detail = evaluation.feedback ? ` — ${evaluation.feedback}` : '';
            const awaitingGuidance = !evaluation.success && evaluation.feedback?.startsWith(feedbackService_1.AWAITING_GUIDANCE_PREFIX);
            const prefix = evaluation.success
                ? 'Agent run completed'
                : awaitingGuidance
                    ? 'Agent run paused'
                    : 'Agent run finished with issues';
            const messageText = `${prefix}${confidence}${detail}`.trim();
            if (messageText.length > 0) {
                // Silent — the chat feed already shows the agent's final status line.
            }
        }
    }
    async updateConversation(entries, options) {
        await this.conversations.updateMessages(entries, options);
        // After any message update, check whether we should kick off a name
        // upgrade. Fires once per conversation — the attempted-ids set
        // prevents repeated LLM calls on follow-up turns.
        if (options?.persist !== false) {
            void this.maybeUpgradeConversationName();
        }
    }
    async maybeUpgradeConversationName() {
        const conversation = this.getCurrentConversation();
        if (!conversation)
            return;
        if (this.conversationNameUpgradeAttempted.has(conversation.id))
            return;
        const hasUser = conversation.messages.some(m => m.role === 'user' && m.content.trim().length > 0);
        const hasAssistant = conversation.messages.some(m => m.role === 'assistant' && m.content.trim().length > 0);
        if (!hasUser || !hasAssistant)
            return;
        // If the current name differs from the derived default, the user
        // already renamed it manually — respect that and don't overwrite.
        const derivedDefault = deriveConversationNameFromEntries(conversation.messages, 'New Conversation');
        if (conversation.name && conversation.name !== derivedDefault)
            return;
        this.conversationNameUpgradeAttempted.add(conversation.id);
        try {
            const summary = await this.summarizeConversationName(conversation.messages);
            if (!summary)
                return;
            // The conversation may have moved on while we were summarizing —
            // re-fetch and only apply if the name is still the derived default.
            const fresh = this.getCurrentConversation();
            if (!fresh || fresh.id !== conversation.id)
                return;
            const currentDefault = deriveConversationNameFromEntries(fresh.messages, 'New Conversation');
            if (fresh.name && fresh.name !== currentDefault)
                return;
            fresh.name = sanitizeConversationName(summary);
            this.conversation = fresh.messages;
            await this.persistConversationHistory();
            await this.syncState();
        }
        catch {
            // Summarization is best-effort; keep the derived name on failure.
        }
    }
    /**
     * Short non-streaming LLM call to distill a user+assistant exchange
     * into a 3–6 word title. Uses the currently-configured provider so
     * the cost/latency profile matches wherever the main chat is running.
     * Bounded at ~1–2 seconds typical latency.
     */
    async summarizeConversationName(entries) {
        const firstUser = entries.find(e => e.role === 'user' && e.content.trim().length > 0);
        const firstAssistant = entries.find(e => e.role === 'assistant' && e.content.trim().length > 0);
        if (!firstUser || !firstAssistant)
            return null;
        const configuration = vscode.workspace.getConfiguration('banditStealth');
        const providerKind = this.getProviderKind(configuration);
        const apiKey = await this.context.secrets.get(API_KEY_SECRET_KEY);
        if (providerKind === 'bandit' && !apiKey)
            return null;
        const ollamaAuth = await Promise.resolve(this.context.secrets.get(OLLAMA_AUTH_SECRET_KEY)).catch(() => undefined);
        const provider = await (0, stealth_core_runtime_1.createProvider)(this.buildProviderSettings(configuration, apiKey ?? '', ollamaAuth));
        const model = providerKind === 'ollama'
            ? this.resolveOllamaBaseModel(configuration)
            : configuration.get('model', 'bandit-core-1') ?? 'bandit-core-1';
        // Keep the input tight — summaries from excerpts are fine, and we
        // want this to be fast. 600 chars from each message covers the gist
        // of typical turns without bloating the request.
        const userExcerpt = firstUser.content.slice(0, 600);
        const assistantExcerpt = firstAssistant.content.slice(0, 600);
        const request = {
            model,
            messages: [
                {
                    role: 'system',
                    content: 'You name chat threads. Reply with a concise 3-6 word title describing the conversation, suitable for a sidebar list. No quotes, no trailing punctuation, no emojis, no prefix like "Title:". Just the bare title.'
                },
                {
                    role: 'user',
                    content: `User asked:\n${userExcerpt}\n\nAssistant replied:\n${assistantExcerpt}\n\nTitle:`
                }
            ],
            stream: false,
            temperature: 0.3
        };
        let text = '';
        for await (const chunk of provider.chat(request)) {
            text += chunk.message?.content ?? '';
            if (chunk.done)
                break;
        }
        // Post-process aggressively: small models wrap the title in
        // `<think>…</think>` reasoning blocks, prefix with "Here's a good
        // title:", or return it as a markdown header. Walk the output,
        // peel off each layer, and return the last usable line.
        //  1. Strip <think>...</think> blocks (DeepSeek-R1, Qwen reasoning variants)
        //  2. Strip leading/trailing fenced code blocks
        //  3. Drop obvious preamble lines ("Here is a title:", etc.)
        //  4. Walk remaining non-empty lines; first viable one wins
        let cleaned = text
            .replace(/<think[^>]*>[\s\S]*?<\/think\s*>/gi, '')
            .replace(/^```[\s\S]*?```$/gm, '')
            .trim();
        const prefaceRe = /^(?:here(?:'?s|\s+is)|sure|okay|title|topic|subject|a\s+good\s+title)\b[^\n]*\n/i;
        while (prefaceRe.test(cleaned)) {
            cleaned = cleaned.replace(prefaceRe, '').trim();
        }
        const lines = cleaned.split(/\n+/).map(l => l.trim()).filter(Boolean);
        const title = lines.find(line => {
            // Skip lines that are still obvious meta (numbered prefix, markdown
            // heading markers, bullet prefixes) — normalize them instead.
            const normalized = line
                .replace(/^[#*>\-+\s]+/, '')
                .replace(/^\d+[.)]\s+/, '')
                .replace(/^["'`*_]+|["'`*_]+$/g, '')
                .replace(/^(?:title|topic|subject)\s*:\s*/i, '')
                .trim();
            return normalized.length > 0 && normalized.length <= 80;
        });
        if (!title)
            return null;
        const final = title
            .replace(/^[#*>\-+\s]+/, '')
            .replace(/^\d+[.)]\s+/, '')
            .replace(/^["'`*_]+|["'`*_]+$/g, '')
            .replace(/^(?:title|topic|subject)\s*:\s*/i, '')
            .trim();
        return final || null;
    }
    ensureActiveConversation() {
        return this.conversations.ensureActive();
    }
    getCurrentConversation() {
        return this.conversations.getCurrent();
    }
    getSortedConversations(includeArchived = true) {
        return this.conversations.getSorted(includeArchived);
    }
    normalizeConversationEntry(entry) {
        const role = entry?.role === 'assistant' ? 'assistant' : 'user';
        const content = typeof entry?.content === 'string' ? entry.content : '';
        const timestamp = typeof entry?.timestamp === 'number' ? entry.timestamp : Date.now();
        const fallbackId = `${timestamp.toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
        const images = Array.isArray(entry?.images) && entry.images.length > 0 ? [...entry.images] : undefined;
        const intent = this.normalizeIntentInsight(entry?.intent);
        const feedback = this.normalizeConversationFeedback(entry?.feedback);
        return {
            id: typeof entry?.id === 'string' && entry.id.length > 0 ? entry.id : fallbackId,
            role,
            content,
            timestamp,
            images,
            intent,
            feedback
        };
    }
    normalizeConversationRecord(record) {
        const normalizedMessages = Array.isArray(record?.messages)
            ? record.messages.map((entry) => this.normalizeConversationEntry(entry))
            : [];
        const baseName = record?.name ?? (normalizedMessages.length > 0
            ? deriveConversationNameFromEntries(normalizedMessages, 'New Conversation')
            : 'New Conversation');
        const timestamps = normalizedMessages.map((entry) => entry.timestamp);
        const fallbackCreated = timestamps.length > 0 ? Math.min(...timestamps) : Date.now();
        const fallbackUpdated = timestamps.length > 0 ? Math.max(...timestamps) : fallbackCreated;
        const createdAt = typeof record?.createdAt === 'number' ? record.createdAt : fallbackCreated;
        const updatedAt = typeof record?.updatedAt === 'number' ? record.updatedAt : fallbackUpdated;
        const sanitizedName = normalizedMessages.length > 0
            ? deriveConversationNameFromEntries(normalizedMessages, baseName)
            : sanitizeConversationName(baseName);
        const normalizedPlanRuns = Array.isArray(record?.planRuns)
            ? record.planRuns
                .map((run) => this.normalizePlanRun(run))
                .filter((run) => Boolean(run))
            : [];
        const limitedPlanRuns = normalizedPlanRuns.slice(-10);
        return {
            id: typeof record?.id === 'string' && record.id.length > 0 ? record.id : createConversationId(),
            name: sanitizedName,
            messages: normalizedMessages,
            archived: Boolean(record?.archived),
            createdAt,
            updatedAt,
            planRuns: limitedPlanRuns
        };
    }
    createConversationRecord(name, messages) {
        const now = Date.now();
        const normalizedMessages = Array.isArray(messages)
            ? messages.map((entry) => this.normalizeConversationEntry(entry))
            : [];
        const timestamps = normalizedMessages.map((entry) => entry.timestamp);
        const createdAt = timestamps.length > 0 ? Math.min(...timestamps) : now;
        const updatedAt = timestamps.length > 0 ? Math.max(...timestamps) : now;
        const record = {
            id: createConversationId(),
            name: normalizedMessages.length > 0
                ? deriveConversationNameFromEntries(normalizedMessages, name)
                : sanitizeConversationName(name),
            messages: normalizedMessages,
            archived: false,
            createdAt,
            updatedAt,
            planRuns: []
        };
        return record;
    }
    normalizePlanRun(raw) {
        if (!raw || typeof raw !== 'object') {
            return undefined;
        }
        const input = raw;
        const plan = input.plan;
        if (!plan || typeof plan !== 'object' || !Array.isArray(plan.steps) || plan.steps.length === 0) {
            return undefined;
        }
        const clonedPlan = this.clonePlan(plan);
        const updatesInput = typeof input.updates === 'object' && input.updates !== null
            ? input.updates
            : {};
        const updates = {};
        for (const [stepId, value] of Object.entries(updatesInput)) {
            if (typeof stepId !== 'string' || !stepId) {
                continue;
            }
            if (!value || typeof value !== 'object') {
                continue;
            }
            const detail = value;
            updates[stepId] = {
                state: typeof detail.state === 'string' ? detail.state : undefined,
                summary: typeof detail.summary === 'string' ? detail.summary : undefined,
                durationMs: typeof detail.durationMs === 'number' && Number.isFinite(detail.durationMs) ? detail.durationMs : undefined,
                tokens: typeof detail.tokens === 'number' && Number.isFinite(detail.tokens) ? detail.tokens : undefined,
                updatedAt: typeof detail.updatedAt === 'number' && Number.isFinite(detail.updatedAt) ? detail.updatedAt : undefined
            };
        }
        const createdAt = typeof input.createdAt === 'number' && Number.isFinite(input.createdAt) ? input.createdAt : Date.now();
        const updatedAt = typeof input.updatedAt === 'number' && Number.isFinite(input.updatedAt) ? input.updatedAt : createdAt;
        const completedAt = typeof input.completedAt === 'number' && Number.isFinite(input.completedAt) ? input.completedAt : undefined;
        const evaluation = input.evaluation && typeof input.evaluation === 'object'
            ? {
                success: typeof input.evaluation.success === 'boolean' ? input.evaluation.success : undefined,
                confidence: typeof input.evaluation.confidence === 'number' && Number.isFinite(input.evaluation.confidence)
                    ? input.evaluation.confidence
                    : undefined,
                feedback: typeof input.evaluation.feedback === 'string' ? input.evaluation.feedback : undefined
            }
            : undefined;
        const artifactsPath = typeof input.artifactsPath === 'string' && input.artifactsPath.length > 0
            ? input.artifactsPath
            : undefined;
        return {
            id: typeof input.id === 'string' && input.id.length > 0 ? input.id : this.createPlanRunId(),
            goal: typeof input.goal === 'string' && input.goal.length > 0 ? input.goal : clonedPlan.goal,
            plan: clonedPlan,
            createdAt,
            updatedAt,
            updates,
            completedAt,
            evaluation,
            artifactsPath
        };
    }
    clonePlan(plan) {
        const cloneTask = (task) => ({
            ...task,
            files: Array.isArray(task.files) ? [...task.files] : undefined,
            metadata: task.metadata ? { ...task.metadata } : undefined
        });
        return {
            goal: plan.goal,
            steps: Array.isArray(plan.steps) ? plan.steps.map((step) => ({ ...step })) : [],
            tasks: Array.isArray(plan.tasks) ? plan.tasks.map((task) => cloneTask(task)) : undefined,
            goals: Array.isArray(plan.goals)
                ? plan.goals.map((goal) => ({
                    ...goal,
                    tasks: Array.isArray(goal.tasks) ? goal.tasks.map((task) => cloneTask(task)) : []
                }))
                : undefined
        };
    }
    createPlanRunId() {
        const timestamp = new Date().toISOString().replace(/[:.]/g, '-');
        return `run-${timestamp}-${Math.random().toString(36).slice(2, 6)}`;
    }
    sanitizePathSegment(input, fallback) {
        const normalized = input.replace(/[^a-z0-9._-]/gi, '-').replace(/-+/g, '-').replace(/^-|-$/g, '');
        return normalized.length > 0 ? normalized.slice(0, 100) : fallback;
    }
    buildPlanArtifactsPath(conversationId, runId) {
        const conversationSegment = this.sanitizePathSegment(conversationId, 'conversation');
        const runSegment = this.sanitizePathSegment(runId, 'run');
        return ['plans', conversationSegment, runSegment].join('/');
    }
    normalizeIntentInsight(raw) {
        if (!raw || typeof raw !== 'object') {
            return undefined;
        }
        const input = raw;
        const action = typeof input.action === 'string' && input.action.trim().length > 0 ? input.action.trim() : undefined;
        if (!action) {
            return undefined;
        }
        const target = typeof input.target === 'string' && input.target.trim().length > 0 ? input.target.trim() : undefined;
        const intent = typeof input.intent === 'string' && input.intent.trim().length > 0 ? input.intent.trim() : undefined;
        const summary = typeof input.summary === 'string' && input.summary.trim().length > 0
            ? input.summary.trim()
            : undefined;
        const confidence = typeof input.confidence === 'number' && Number.isFinite(input.confidence)
            ? Math.max(0, Math.min(1, input.confidence))
            : undefined;
        const rationale = typeof input.rationale === 'string' && input.rationale.trim().length > 0
            ? input.rationale.trim()
            : undefined;
        const rawData = typeof input.raw === 'object' && input.raw !== null ? input.raw : undefined;
        return {
            action,
            target,
            intent,
            summary,
            confidence,
            rationale,
            raw: rawData
        };
    }
    normalizeConversationFeedback(raw) {
        if (!raw || typeof raw !== 'object') {
            return undefined;
        }
        const input = raw;
        const rating = input.rating === 'up' || input.rating === 'down' ? input.rating : undefined;
        if (!rating) {
            return undefined;
        }
        const submitted = input.submitted === true;
        const submittedAt = typeof input.submittedAt === 'number' && Number.isFinite(input.submittedAt)
            ? input.submittedAt
            : undefined;
        const note = typeof input.note === 'string' && input.note.trim().length > 0 ? input.note.trim() : undefined;
        return {
            rating,
            submitted,
            submittedAt,
            note
        };
    }
    async persistConversationHistory() {
        // Persistence is now handled by ConversationService internally.
        // This method is kept for compatibility with existing call sites.
    }
    syncPlanStateFromConversation(_conversation) {
        // Plan state is managed by ConversationService internally
    }
    resetPlanState() {
        // Plan state is managed by ConversationService internally
    }
    getActivePlanRun(_conversation) {
        return this.conversations.getPlanSnapshot().plan ? undefined : undefined;
    }
    updatePlanRunStep(stepId, update, options) {
        const result = this.conversations.updatePlanStep(stepId, update);
        if (result && options?.emitHistory !== false) {
            const conversation = this.getCurrentConversation();
            if (conversation) {
                this.postMessage({
                    type: 'agentPlanHistory',
                    history: this.conversations.serializePlanRuns(conversation.planRuns),
                    activeRunId: this.conversations.activePlanRunId ?? null
                });
            }
        }
        return result;
    }
    getPlanSnapshot(_conversation) {
        return this.conversations.getPlanSnapshot();
    }
    serializePlanRuns(runs) {
        return this.conversations.serializePlanRuns(runs);
    }
    getRecentConversationSummaries(_conversations) {
        return this.conversations.getSummaries();
    }
    hasArchivedConversations() {
        return this.conversations.hasArchived();
    }
    async clearCurrentConversation() {
        this.cancelActiveStream();
        this.isBusy = false;
        this.statusText = 'Ready';
        this.currentIntent = undefined;
        await this.clearDiffPreviewSessions();
        if (!this.currentConversationId) {
            await this.openHistoryView({ clearActive: true });
            return;
        }
        const current = this.ensureActiveConversation();
        current.archived = false;
        await this.updateConversation([]);
        await this.syncState();
    }
    async clearAllConversations() {
        this.cancelActiveStream();
        this.isBusy = false;
        this.statusText = 'Ready';
        this.currentIntent = undefined;
        await this.clearDiffPreviewSessions();
        await this.conversations.clearAll();
        await this.syncState();
        // silent — the chat feed visibly empties.
    }
    async confirmAndClearAll() {
        const choice = await vscode.window.showWarningMessage('Clear all Bandit Stealth conversations? This action cannot be undone.', { modal: true }, 'Clear conversations');
        if (choice === 'Clear conversations') {
            await this.clearAllConversations();
        }
    }
    async startNewConversation() {
        this.cancelActiveStream();
        this.isBusy = false;
        this.statusText = 'Ready';
        await this.conversations.startNew();
        await this.syncState();
    }
    async selectConversation(id) {
        if (this.conversations.currentId === id) {
            await this.syncState();
            return;
        }
        this.cancelActiveStream();
        this.isBusy = false;
        this.statusText = 'Ready';
        await this.conversations.select(id);
        await this.syncState();
    }
    async deleteConversation(id) {
        const wasCurrent = this.conversations.currentId === id;
        await this.conversations.remove(id);
        if (wasCurrent) {
            await this.openHistoryView({ clearActive: true });
            return;
        }
        this.statusText = 'Ready';
        await this.syncState();
    }
    async setConversationArchived(id, archived) {
        await this.conversations.setArchived(id, archived);
        if (archived && this.currentConversationId === id) {
            await this.openHistoryView({ skipPersist: true, clearActive: true });
            return;
        }
        if (!archived && this.currentConversationId === id) {
            this.historyVisible = false;
        }
        await this.syncState();
    }
    async openHistoryView(options) {
        this.cancelActiveStream();
        this.isBusy = false;
        this.statusText = 'Ready';
        this.historyVisible = true;
        await this.clearDiffPreviewSessions();
        if (options?.clearActive) {
            this.currentConversationId = undefined;
            this.conversation = [];
            this.resetPlanState();
        }
        if (!options?.skipPersist) {
            await this.persistConversationHistory();
        }
        await this.syncState();
    }
    getHtml(webview) {
        return this.getV2Html(webview);
    }
    getV2Html(webview) {
        const nonce = getNonce();
        const stylesFile = vscode.Uri.joinPath(this.context.extensionUri, 'media', 'v2', 'webview.css');
        const scriptFile = vscode.Uri.joinPath(this.context.extensionUri, 'media', 'v2', 'webview.js');
        const assetVersion = this.getWebviewAssetVersion([stylesFile.fsPath, scriptFile.fsPath]);
        const stylesUri = webview.asWebviewUri(stylesFile).with({ query: `v=${assetVersion}` });
        const scriptUri = webview.asWebviewUri(scriptFile).with({ query: `v=${assetVersion}` });
        const logoUri = webview.asWebviewUri(vscode.Uri.joinPath(this.context.extensionUri, 'media', 'logo.png'));
        const configJson = JSON.stringify({ logoSrc: logoUri.toString() }).replace(/</g, '\u003c');
        const csp = [
            "default-src 'none'",
            `img-src ${webview.cspSource} https: data:`,
            `font-src ${webview.cspSource}`,
            `style-src ${webview.cspSource}`,
            `script-src 'nonce-${nonce}' 'strict-dynamic'`
        ].join('; ');
        return /* html */ `
      <!DOCTYPE html>
      <html lang="en">
        <head>
          <meta charset="UTF-8" />
          <meta http-equiv="Content-Security-Policy" content="${csp}" />
          <meta name="viewport" content="width=device-width, initial-scale=1.0" />
          <title>Bandit Stealth</title>
          <link rel="stylesheet" href="${stylesUri}" />
        </head>
        <body>
          <div id="root"></div>
          <script id="bandit-stealth-config" type="application/json">${configJson}</script>
          <script type="module" nonce="${nonce}" src="${scriptUri}"></script>
        </body>
      </html>
    `;
    }
    getWebviewAssetVersion(assetPaths) {
        const packageVersion = typeof this.context.extension?.packageJSON?.version === 'string'
            ? this.context.extension.packageJSON.version
            : 'dev';
        let latestMtime = 0;
        for (const assetPath of assetPaths) {
            try {
                const mtime = Math.floor((0, fs_1.statSync)(assetPath).mtimeMs);
                if (mtime > latestMtime) {
                    latestMtime = mtime;
                }
            }
            catch {
                // Ignore missing stats and fall back to extension version only.
            }
        }
        return latestMtime > 0 ? `${packageVersion}.${latestMtime}` : packageVersion;
    }
    dispose() {
        this.cancelActiveStream();
        this.agentEnvironmentSubscription?.dispose();
        this._onDidChangeStatus.dispose();
    }
}
BanditStealthViewProvider.viewType = 'banditStealth.chat';
function activate(context) {
    const runtimeController = new agentRuntime_1.StealthAgentRuntime(context);
    const frameworkRuntime = runtimeController.getFrameworkRuntime();
    const adapter = (0, agent_adapters_vscode_1.createVscodeAdapter)(vscode);
    adapter.activate();
    const adapterPlanListener = (event) => {
        void environmentService_1.environmentService.postToWebview({ type: 'agent:plan', payload: event.payload });
    };
    adapter.on('plan:complete', adapterPlanListener);
    const diffListener = (event) => {
        void environmentService_1.environmentService.postToWebview({ type: 'agent:diff', payload: event.payload });
    };
    frameworkRuntime.on('diff:apply', diffListener);
    const promptPipeline = new promptPipeline_1.PromptPipeline(runtimeController);
    const diffContentProvider = new diffContentProvider_1.DiffContentProvider();
    const provider = new BanditStealthViewProvider(context, runtimeController, promptPipeline, diffContentProvider);
    // ── Status bar item ──────────────────────────────────────────────────────────
    const statusBarItem = vscode.window.createStatusBarItem(vscode.StatusBarAlignment.Right, 100);
    statusBarItem.command = 'banditStealth.switchModel';
    let lastContextBudget;
    function updateStatusBarText(busy, statusText, contextBudget) {
        if (contextBudget !== undefined) {
            lastContextBudget = contextBudget;
        }
        const configuration = vscode.workspace.getConfiguration('banditStealth');
        const providerKind = configuration.get('provider', 'bandit');
        const isOllama = providerKind === 'ollama';
        const model = isOllama
            ? configuration.get('ollamaModel', 'gemma3:12b') ?? 'gemma3:12b'
            : configuration.get('model', 'bandit-core-1') ?? 'bandit-core-1';
        const providerLabel = isOllama ? 'Ollama' : 'Bandit AI';
        const toolUse = configuration.get('enableToolUse', true) ? ' · tools' : '';
        // Format context budget suffix: e.g. " · $(database) 3.2k / 32k"
        let ctxSuffix = '';
        let ctxTooltipLine = '';
        if (lastContextBudget && lastContextBudget.source !== 'none') {
            const estK = (lastContextBudget.tokenEstimate / 1000).toFixed(1);
            const winK = Math.round(lastContextBudget.contextWindow / 1000);
            const srcIcon = lastContextBudget.source === 'gateway' ? '$(database)' : '$(files)';
            ctxSuffix = ` · ${srcIcon} ${estK}k / ${winK}k`;
            const srcLabel = lastContextBudget.source === 'gateway' ? 'Qdrant' : lastContextBudget.source === 'local' ? 'Local' : 'Pinned';
            ctxTooltipLine = `\nContext: ${srcLabel} · ${estK}k / ${winK}k tokens`;
        }
        if (busy) {
            const txt = statusText && statusText !== 'Ready' ? statusText : '…';
            statusBarItem.text = `$(sync~spin) Bandit · ${txt}`;
            statusBarItem.tooltip = `${providerLabel} — ${txt}`;
        }
        else {
            statusBarItem.text = `$(robot) Bandit · ${model}${toolUse}${ctxSuffix}`;
            statusBarItem.tooltip = `Bandit Stealth · ${providerLabel}\nModel: ${model}${toolUse}${ctxTooltipLine}\nClick to switch model`;
        }
    }
    updateStatusBarText();
    statusBarItem.show();
    // On activation, auto-detect Ollama availability and model capabilities.
    // Shows a helpful status message so users know the agent is ready.
    {
        const activationCfg = vscode.workspace.getConfiguration('banditStealth');
        if (activationCfg.get('provider', 'ollama') === 'ollama') {
            const baseModelId = activationCfg.get('ollamaModel', 'gemma3:12b') ?? '';
            // Auto-routing ACTUALLY uses ollamaCodingModel for coding/text prompts
            // when enabled. If we only validate baseModelId, we give users a
            // false "ready" signal — then their first prompt hits an uninstalled
            // coding model and hangs silently. Gather every model that could
            // be dispatched to and verify each is pulled.
            const autoRoute = activationCfg.get('ollamaAutoRouteModels', true) !== false;
            const codingModelId = (activationCfg.get('ollamaCodingModel', '') ?? '').trim();
            const agentModelId = (activationCfg.get('agentOllamaModel', '') ?? '').trim();
            const visionModelId = (activationCfg.get('ollamaVisionModel', '') ?? '').trim();
            const modelsToCheck = new Set();
            if (baseModelId)
                modelsToCheck.add(baseModelId);
            if (autoRoute && codingModelId)
                modelsToCheck.add(codingModelId);
            if (agentModelId)
                modelsToCheck.add(agentModelId);
            if (autoRoute && visionModelId)
                modelsToCheck.add(visionModelId);
            const activationBaseUrl = activationCfg.get('ollamaBaseUrl', '') ||
                activationCfg.get('ollamaUrl', 'http://localhost:11434') ||
                'http://localhost:11434';
            // Health check: is Ollama running? Update status bar + webview onboarding.
            void (async () => {
                try {
                    const response = await fetch(`${activationBaseUrl.replace(/\/+$/, '')}/api/tags`, {
                        signal: AbortSignal.timeout(3000)
                    });
                    if (response.ok) {
                        const data = await response.json();
                        const models = data?.models ?? [];
                        // Match on name-prefix up to the first colon so "gemma3:12b"
                        // matches "gemma3:12b-it-qat" — users frequently pull variants
                        // without realizing the tag differs from the config string.
                        const isInstalled = (candidate) => models.some(m => m.name === candidate || m.name.startsWith(candidate.split(':')[0] + ':') || m.name === candidate.split(':')[0]);
                        const missing = Array.from(modelsToCheck).filter(m => !isInstalled(m));
                        if (missing.length > 0 && models.length > 0) {
                            // Flag every missing model. The first missing one owns the
                            // prompt affordance (Pull Model button) since installing one
                            // at a time via the terminal is the path of least resistance.
                            const primary = missing[0];
                            provider.setOllamaStatus('no-model', primary);
                            const listed = missing.length === 1 ? `"${primary}"` : `${missing.length} models (${missing.map(m => `"${m}"`).join(', ')})`;
                            void vscode.window.showWarningMessage(`Ollama is running but ${listed} not installed. Without these, chats will silently hang. Run: ollama pull ${primary}${missing.length > 1 ? ` (and the others)` : ''}`, 'Pull Model', 'Disable auto-routing').then(choice => {
                                if (choice === 'Pull Model') {
                                    const terminal = vscode.window.createTerminal('Ollama');
                                    terminal.show();
                                    terminal.sendText(`ollama pull ${primary}`);
                                }
                                else if (choice === 'Disable auto-routing') {
                                    // Turning off auto-routing makes the extension use
                                    // banditStealth.ollamaModel directly — the safest
                                    // recovery when the coding/vision models are missing.
                                    void activationCfg.update('ollamaAutoRouteModels', false, vscode.ConfigurationTarget.Global);
                                }
                            });
                        }
                        else {
                            provider.setOllamaStatus('ready');
                        }
                        const caps = await (0, stealth_core_runtime_1.queryOllamaModelCapabilities)(baseModelId, activationBaseUrl);
                        if (caps)
                            (0, stealth_core_runtime_1.registerModelCapabilities)(baseModelId, caps);
                    }
                }
                catch {
                    provider.setOllamaStatus('offline');
                    statusBarItem.text = '$(warning) Bandit · Ollama offline';
                    statusBarItem.tooltip = 'Ollama is not running. Start it with: ollama serve';
                }
            })();
        }
    }
    // Update status bar when config changes (model, provider, tool use toggle).
    const configChangeListener = vscode.workspace.onDidChangeConfiguration((e) => {
        if (e.affectsConfiguration('banditStealth')) {
            updateStatusBarText();
        }
    });
    // Update status bar when provider busy state changes.
    const statusChangeListener = provider.onDidChangeStatus(({ busy, text, contextBudget }) => {
        updateStatusBarText(busy, text, contextBudget);
    });
    void (0, pythonEnvironment_1.ensurePython)().then((result) => {
        if (result.info) {
            console.info(`Bandit Stealth: detected Python ${result.info.version} via "${result.info.command}".`);
            return;
        }
        const openDocs = 'Open Python Downloads';
        const openSettings = 'Configure Python Path';
        void vscode.window.showWarningMessage('Bandit Stealth agent features require Python 3. Install Python 3 or configure the `banditStealth.pythonPath` setting.', openDocs, openSettings).then((choice) => {
            if (choice === openDocs) {
                void vscode.env.openExternal(vscode.Uri.parse('https://www.python.org/downloads/'));
            }
            else if (choice === openSettings) {
                void vscode.commands.executeCommand('workbench.action.openSettings', 'banditStealth.pythonPath');
            }
        });
    });
    context.subscriptions.push(provider, diffContentProvider, statusBarItem, configChangeListener, statusChangeListener, vscode.workspace.registerTextDocumentContentProvider(diffContentProvider_1.DiffContentProvider.scheme, diffContentProvider), vscode.window.registerWebviewViewProvider(BanditStealthViewProvider.viewType, provider), vscode.commands.registerCommand('banditStealth.askBandit', () => revealWithSelection(provider)), vscode.commands.registerCommand('banditStealth.openChat', () => provider.reveal()), vscode.commands.registerCommand('banditStealth.setApiKey', () => provider.showApiKeyOverlay()), vscode.commands.registerCommand('banditStealth.resetApiKey', () => provider.clearApiKey()), vscode.commands.registerCommand('banditStealth.setOllamaAuthToken', () => provider.setOllamaAuthToken()), vscode.commands.registerCommand('banditStealth.clearOllamaAuthToken', () => provider.clearOllamaAuthToken()), vscode.commands.registerCommand('banditStealth.toggleMode', () => provider.toggleMode()), 
    // ── Model switcher ───────────────────────────────────────────────────────
    vscode.commands.registerCommand('banditStealth.switchModel', async () => {
        const configuration = vscode.workspace.getConfiguration('banditStealth');
        const providerKind = configuration.get('provider', 'bandit');
        if (providerKind === 'ollama') {
            // Resolve the exact URL + headers the chat engine will use so the
            // picker can never disagree with the actual inference endpoint.
            const { url: ollamaUrl, headers: extraHeaders, isNodeOverride } = (0, stealth_core_runtime_1.resolveOllamaEndpoint)({
                get: (section, defaultValue) => configuration.get(section, defaultValue)
            });
            const currentModel = configuration.get('ollamaModel', 'gemma3:12b') ?? '';
            const isLocalUrl = /^https?:\/\/(localhost|127\.0\.0\.1|0\.0\.0\.0|\[::1\])(?::\d+)?/i.test(ollamaUrl);
            const hasCustomAuth = Object.keys(extraHeaders).length > 0 || isNodeOverride || !isLocalUrl;
            let models = [];
            let health = 'unreachable';
            let fetchError;
            try {
                const response = await fetch(`${ollamaUrl}/api/tags`, {
                    // 3-second timeout — don't hang the UI on unreachable remote endpoints.
                    signal: AbortSignal.timeout(3000),
                    headers: extraHeaders
                });
                if (response.ok) {
                    const data = await response.json();
                    models = Array.isArray(data?.models) ? data.models : [];
                    health = models.length > 0 ? 'healthy' : 'empty';
                }
                else {
                    fetchError = `HTTP ${response.status}`;
                }
            }
            catch (err) {
                fetchError = err instanceof Error ? err.message : String(err);
            }
            const commitModel = async (picked) => {
                const trimmed = picked.trim();
                if (!trimmed)
                    return;
                await configuration.update('ollamaModel', trimmed, vscode.ConfigurationTarget.Workspace);
                updateStatusBarText();
                void vscode.window.showInformationMessage(`Model switched to ${trimmed}`);
                // Auto-detect capabilities for models not in the built-in profile list.
                void (0, stealth_core_runtime_1.queryOllamaModelCapabilities)(trimmed, ollamaUrl).then(caps => {
                    if (caps)
                        (0, stealth_core_runtime_1.registerModelCapabilities)(trimmed, caps);
                });
            };
            if (health === 'healthy') {
                const items = models
                    .map(m => ({
                    label: m.name === currentModel ? `$(check) ${m.name}` : m.name,
                    description: m.name === currentModel ? 'current' : undefined,
                    model: m.name
                }))
                    .sort((a, b) => a.label.localeCompare(b.label));
                // Manual entry always available — even on localhost. Covers the
                // "set a name before pulling" flow, OLLAMA_MODELS-pointed setups
                // where /api/tags doesn't show everything, and "skip the list
                // wait" when a remote endpoint is slow.
                items.push({
                    label: '$(edit) Enter model name manually…',
                    description: 'Type a model ID (works even if not yet pulled)',
                    action: 'manual'
                });
                void hasCustomAuth; // retained for future per-endpoint gating hooks
                const selected = await vscode.window.showQuickPick(items, {
                    title: 'Switch Ollama Model',
                    placeHolder: `Current: ${currentModel} · ${ollamaUrl}`
                });
                if (!selected)
                    return;
                if (selected.action === 'manual') {
                    const input = await vscode.window.showInputBox({
                        title: 'Enter Ollama Model',
                        prompt: `Model ID on ${ollamaUrl}`,
                        value: currentModel
                    });
                    if (!input?.trim())
                        return;
                    await commitModel(input);
                }
                else if (selected.model) {
                    await commitModel(selected.model);
                }
            }
            else if (health === 'empty') {
                const pullHint = 'ollama pull bandit-core:31b';
                void vscode.window.showWarningMessage(`Ollama is reachable at ${ollamaUrl} but no models are installed. Pull one with: ${pullHint}`);
                if (hasCustomAuth) {
                    const input = await vscode.window.showInputBox({
                        title: 'Enter Ollama Model',
                        prompt: `Model ID on ${ollamaUrl}`,
                        value: currentModel
                    });
                    if (input?.trim())
                        await commitModel(input);
                }
            }
            else {
                // Unreachable: split copy by local vs remote. Remote failures almost
                // always mean "my GPU node / RunPod is off right now" — let the user
                // type a model manually so a down endpoint doesn't block them.
                if (isLocalUrl) {
                    void vscode.window.showErrorMessage(`Can't detect Ollama at ${ollamaUrl}. Check that it's running (curl ${ollamaUrl}/api/tags).`);
                }
                else {
                    void vscode.window.showWarningMessage(`Your remote Ollama at ${ollamaUrl} isn't responding${fetchError ? ` (${fetchError})` : ''} — type a model name manually to keep working.`);
                }
                if (hasCustomAuth || !isLocalUrl) {
                    const input = await vscode.window.showInputBox({
                        title: 'Enter Ollama Model',
                        prompt: `Model ID on ${ollamaUrl}`,
                        value: currentModel,
                        placeHolder: 'e.g. bandit-core:31b'
                    });
                    if (input?.trim())
                        await commitModel(input);
                }
            }
        }
        else {
            // Bandit AI — show available cloud models + a manual-entry escape
            // hatch for gateway-routed aliases (e.g. a cluster Ollama node
            // exposed as "qwen2.5-coder:32b" behind api.burtson.ai). The
            // built-in list covers the default trio; typing a custom name
            // works as long as the gateway knows how to route it.
            const currentModel = configuration.get('model', 'bandit-core-1') ?? 'bandit-core-1';
            // Only models that api.burtson.ai actually routes. bandit-core-flash
            // and bandit-core-pro were placeholders; removed to stop the picker
            // from offering 404s. Add more here as the gateway grows upstreams.
            const banditModels = [
                { label: 'bandit-core-1', description: 'Default — balanced speed/quality', model: 'bandit-core-1' },
                { label: 'bandit-logic', description: 'Agentic coding specialist (Qwen 3.6 27B, native tool calling, multimodal)', model: 'bandit-logic' }
            ];
            const items = banditModels.map(m => ({
                ...m,
                description: m.model === currentModel ? `$(check) current · ${m.description}` : m.description
            }));
            if (!items.some(it => it.model === currentModel)) {
                items.unshift({
                    label: currentModel,
                    description: '$(check) current · custom gateway alias',
                    model: currentModel
                });
            }
            items.push({
                label: '$(edit) Enter model name manually…',
                description: 'Route to a custom gateway alias (e.g. a cluster Ollama model)',
                action: 'manual'
            });
            const selected = await vscode.window.showQuickPick(items, {
                title: 'Switch Bandit AI Model',
                placeHolder: `Current: ${currentModel}`
            });
            if (!selected)
                return;
            let chosen = selected.model;
            if (selected.action === 'manual') {
                const input = await vscode.window.showInputBox({
                    title: 'Bandit AI Model — Custom Alias',
                    prompt: 'Model name as configured on api.burtson.ai (e.g. qwen2.5-coder:32b)',
                    value: currentModel,
                    validateInput: value => value.trim().length === 0 ? 'Enter a non-empty model name' : undefined
                });
                chosen = input?.trim();
            }
            if (!chosen)
                return;
            await configuration.update('model', chosen, vscode.ConfigurationTarget.Workspace);
            updateStatusBarText();
        }
    }), vscode.commands.registerCommand('banditStealth.agent.startGoal', async (inputGoal) => {
        let goal = typeof inputGoal === 'string' ? inputGoal.trim() : '';
        if (!goal) {
            goal = (await vscode.window.showInputBox({
                title: 'Agent Goal',
                prompt: 'Describe the goal to achieve'
            }))?.trim() ?? '';
        }
        if (!goal) {
            return;
        }
        const cfg = vscode.workspace.getConfiguration('banditStealth');
        const providerKind = cfg.get('provider', 'bandit') === 'ollama' ? 'ollama' : 'bandit';
        const activeModelId = providerKind === 'ollama'
            ? (() => {
                const baseModel = (cfg.get('ollamaModel', 'gemma3:12b') ?? 'gemma3:12b').trim();
                const agentModel = (cfg.get('agentOllamaModel', '') ?? '').trim();
                if (agentModel) {
                    return agentModel;
                }
                const autoRoute = cfg.get('ollamaAutoRouteModels', true) !== false;
                if (!autoRoute) {
                    return baseModel;
                }
                const codingModel = (cfg.get('ollamaCodingModel', '') ?? '').trim();
                return codingModel || baseModel;
            })()
            : cfg.get('model', 'bandit-core-1');
        const agentTier = (0, stealth_core_runtime_1.getModelCapabilities)(activeModelId).tier;
        // Opt-in: create an isolated git branch before the agent touches anything.
        if (cfg.get('agent.createBranchBeforeRun', false)) {
            const workspaceRoot = vscode.workspace.workspaceFolders?.[0]?.uri.fsPath;
            if (workspaceRoot) {
                const slug = goal
                    .toLowerCase()
                    .replace(/[^a-z0-9]+/g, '-')
                    .replace(/^-+|-+$/g, '')
                    .slice(0, 40);
                const branchName = `bandit/${slug || 'run'}`;
                const branchResult = (0, child_process_1.spawnSync)('git', ['checkout', '-b', branchName], {
                    cwd: workspaceRoot,
                    encoding: 'utf8'
                });
                if (branchResult.status === 0) {
                    void vscode.window.showInformationMessage(`Bandit: created branch ${branchName}`);
                }
                // Non-zero exit = branch already exists or git unavailable — silently continue.
            }
        }
        const contextResult = await provider.buildContextBlock(goal, cfg).catch(() => undefined);
        void runtimeController.startGoal(goal, { modelTier: agentTier, contextBlock: contextResult?.formatted });
    }), vscode.commands.registerCommand('banditStealth.agent.cancel', () => {
        runtimeController.cancel();
        void environmentService_1.environmentService.postToWebview({ type: 'agent:status', text: 'Goal cancelled', phase: 'error' });
    }), vscode.commands.registerCommand('banditStealth.agent.showReport', async () => {
        const workspaceFolder = vscode.workspace.workspaceFolders?.[0]?.uri;
        if (!workspaceFolder) {
            void vscode.window.showWarningMessage('Open a workspace to view agent reports.');
            return;
        }
        const reportUri = vscode.Uri.joinPath(workspaceFolder, '.bandit', 'agent-report.json');
        try {
            const document = await vscode.workspace.openTextDocument(reportUri);
            await vscode.window.showTextDocument(document, vscode.ViewColumn.Beside);
        }
        catch {
            void vscode.window.showWarningMessage('No report found. Run an agent goal first.');
        }
    }), vscode.commands.registerCommand('banditStealth.testConnection', async () => {
        const configuration = vscode.workspace.getConfiguration('banditStealth');
        const providerKind = configuration.get('provider', 'bandit');
        const ollamaUrl = configuration.get('ollamaBaseUrl', '') ||
            configuration.get('ollamaUrl', 'http://localhost:11434') ||
            'http://localhost:11434';
        const gatewayUrl = configuration.get('gatewayUrl', 'https://api.burtson.ai');
        if (providerKind === 'ollama') {
            try {
                const start = Date.now();
                const response = await fetch(`${ollamaUrl.replace(/\/+$/, '')}/api/tags`, { signal: AbortSignal.timeout(5000) });
                const latency = Date.now() - start;
                if (response.ok) {
                    const data = await response.json();
                    const modelCount = data?.models?.length ?? 0;
                    const model = configuration.get('ollamaModel', 'gemma3:12b');
                    void vscode.window.showInformationMessage(`Ollama connected · ${model} · ${modelCount} model(s) available · ${latency}ms`);
                }
                else {
                    void vscode.window.showWarningMessage(`Ollama responded with ${response.status} at ${ollamaUrl}`);
                }
            }
            catch (err) {
                void vscode.window.showErrorMessage(`Cannot reach Ollama at ${ollamaUrl} — is it running?`);
            }
        }
        else {
            // Bandit / Gateway provider
            const apiKey = await context.secrets.get(API_KEY_SECRET_KEY);
            if (!apiKey) {
                void vscode.window.showWarningMessage('No API key set. Use "Bandit: Set API Key" first.');
                return;
            }
            try {
                const start = Date.now();
                const response = await fetch(`${gatewayUrl.replace(/\/+$/, '')}/api/stealth/health`, {
                    headers: { Authorization: `Bearer ${apiKey}` },
                    signal: AbortSignal.timeout(5000)
                });
                const latency = Date.now() - start;
                if (response.ok) {
                    const model = configuration.get('model', 'bandit-core-1');
                    void vscode.window.showInformationMessage(`Gateway connected · ${model} · ${latency}ms`);
                }
                else {
                    void vscode.window.showWarningMessage(`Gateway responded with ${response.status}`);
                }
            }
            catch {
                void vscode.window.showErrorMessage(`Cannot reach Gateway at ${gatewayUrl}`);
            }
        }
    }), vscode.commands.registerCommand('banditStealth.linkWorkspace', async () => {
        const configuration = vscode.workspace.getConfiguration('banditStealth');
        const gatewayUrl = configuration.get('gatewayUrl', '');
        if (!gatewayUrl) {
            void vscode.window.showWarningMessage('Set "banditStealth.gatewayUrl" in settings first.');
            return;
        }
        const apiKey = await context.secrets.get(API_KEY_SECRET_KEY);
        if (!apiKey) {
            void vscode.window.showWarningMessage('No API key set. Use "Bandit: Set API Key" first.');
            return;
        }
        const adapter = new stealth_core_runtime_1.GatewaySearchAdapter({ gatewayUrl, apiKey, workspaceId: '' });
        const workspaces = await adapter.listWorkspaces();
        if (!workspaces.length) {
            void vscode.window.showWarningMessage('No workspaces found on Gateway. Create one in Bandit Stealth Web first.');
            return;
        }
        const items = workspaces.map(w => ({
            label: w.name,
            description: w.repoFullName ?? w.id,
            id: w.id
        }));
        const selected = await vscode.window.showQuickPick(items, {
            title: 'Link Workspace to Gateway',
            placeHolder: 'Select the workspace that matches this repo'
        });
        if (!selected)
            return;
        await configuration.update('workspaceId', selected.id, vscode.ConfigurationTarget.Workspace);
        void vscode.window.showInformationMessage(`Workspace linked: "${selected.label}" (${selected.id}). Qdrant context is now active for this repo.`);
    }), vscode.commands.registerCommand('banditStealth.indexRepo', async () => {
        const configuration = vscode.workspace.getConfiguration('banditStealth');
        const gatewayUrl = configuration.get('gatewayUrl', '');
        const workspaceId = configuration.get('workspaceId', '');
        if (!gatewayUrl || !workspaceId) {
            void vscode.window.showWarningMessage('Run "Bandit: Link Workspace to Gateway" first to configure gatewayUrl and workspaceId.');
            return;
        }
        const apiKey = await context.secrets.get(API_KEY_SECRET_KEY);
        if (!apiKey) {
            void vscode.window.showWarningMessage('No API key set. Use "Bandit: Set API Key" first.');
            return;
        }
        const adapter = new stealth_core_runtime_1.GatewaySearchAdapter({ gatewayUrl, apiKey, workspaceId });
        void vscode.window.withProgress({ location: vscode.ProgressLocation.Notification, title: 'Bandit: Starting repo index…', cancellable: false }, async () => {
            const ok = await adapter.triggerIndex(workspaceId);
            if (ok) {
                void vscode.window.showInformationMessage('Repo indexing started. Status will update in the status bar when complete.');
            }
            else {
                void vscode.window.showErrorMessage('Failed to trigger indexing. Check gateway logs.');
            }
        });
    }), new vscode.Disposable(() => {
        adapter.off('plan:complete', adapterPlanListener);
        adapter.dispose();
    }), new vscode.Disposable(() => {
        frameworkRuntime.off('diff:apply', diffListener);
    }));
}
function deactivate() {
    // no-op
}
async function revealWithSelection(provider) {
    const editor = vscode.window.activeTextEditor;
    const selection = editor?.selection && !editor.selection.isEmpty
        ? editor.document.getText(editor.selection).trim()
        : '';
    await provider.reveal(selection || undefined);
}
const EMOJI_REGEX = /\p{Extended_Pictographic}/gu;
const VARIATION_SELECTORS_REGEX = /[\uFE0F\uFE0E]/g;
const ZERO_WIDTH_JOINER_REGEX = /\u200D/g;
/** Synchronous best-effort read; returns '' if the file doesn't exist or errors. */
function readFileSafe(absolutePath) {
    try {
        return require('fs').readFileSync(absolutePath, 'utf-8');
    }
    catch {
        return '';
    }
}
/**
 * Compact a tool's `primary` display value for the inline `→ tool path`
 * activity marker. Absolute paths get rewritten to workspace-relative
 * form; anything still longer than 60 chars is trimmed with a leading
 * ellipsis so the filename stays visible. Non-path primaries (patterns,
 * shell commands, URLs) are just length-clamped.
 */
function compactToolDisplayParam(raw, workspaceRoot) {
    if (!raw)
        return '';
    let out = raw;
    if (path.isAbsolute(raw) && workspaceRoot) {
        const rel = path.relative(workspaceRoot, raw);
        if (rel && !rel.startsWith('..')) {
            out = rel;
        }
    }
    const MAX = 60;
    if (out.length > MAX) {
        out = '…' + out.slice(out.length - (MAX - 1));
    }
    return out;
}
/**
 * Build a compact unified diff block (fenced as `diff` so markdown renderers
 * highlight it). Shows up to 12 changed lines with ±1 line of context; falls
 * back to an empty string when the change is too large to meaningfully
 * preview inline.
 */
function buildDiffFenceInfo(meta) {
    // Encode path + stats into the fence info string so the webview diff-card
    // can render the file name in its summary (instead of a generic "diff"
    // label). Format: `diff path=<rel> plus=<n> minus=<n>`. The webview parses
    // with a permissive regex — missing fields just fall back to defaults.
    if (!meta || !meta.relPath)
        return 'diff';
    const encodedPath = meta.relPath.replace(/ /g, '%20');
    const parts = ['diff', `path=${encodedPath}`];
    if (typeof meta.plus === 'number')
        parts.push(`plus=${meta.plus}`);
    if (typeof meta.minus === 'number')
        parts.push(`minus=${meta.minus}`);
    return parts.join(' ');
}
function buildCompactDiffBlock(before, after, maxLines = 60, meta) {
    if (before === after)
        return '';
    const a = before.split('\n');
    const b = after.split('\n');
    // Myers-style LCS; cap the grid so we don't burn the event loop on huge
    // files. 500k cells covers ~700×700 source files, which is the long tail
    // of real files the agent edits. Past that, fall back to a hash-set diff
    // that preserves the card (and its path header) — previously we returned
    // '' and the card vanished, leaving the user with only the `**✎ edited**`
    // line and no body. Observed Apr 22 on FileController.cs (~400 lines)
    // where the 40k cap silently dropped the whole card.
    const fenceInfo = buildDiffFenceInfo(meta);
    if (a.length * b.length > 500000) {
        const beforeSet = new Set(a);
        const afterSet = new Set(b);
        const added = [];
        const removed = [];
        for (const line of b) {
            if (!beforeSet.has(line))
                added.push(line);
        }
        for (const line of a) {
            if (!afterSet.has(line))
                removed.push(line);
        }
        const shown = [];
        const half = Math.floor(maxLines / 2);
        for (const line of removed.slice(0, half))
            shown.push('- ' + line);
        for (const line of added.slice(0, maxLines - shown.length))
            shown.push('+ ' + line);
        if (shown.length === 0)
            return '';
        const truncated = added.length + removed.length > shown.length;
        const suffix = truncated ? '\n… (truncated; file too large for full diff)' : '';
        return '```' + fenceInfo + '\n' + shown.join('\n') + suffix + '\n```\n';
    }
    const m = a.length;
    const n = b.length;
    const table = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            table[i][j] = a[i - 1] === b[j - 1] ? table[i - 1][j - 1] + 1 : Math.max(table[i - 1][j], table[i][j - 1]);
        }
    }
    const ops = [];
    let i = m;
    let j = n;
    while (i > 0 && j > 0) {
        if (a[i - 1] === b[j - 1]) {
            ops.unshift({ kind: 'eq', line: a[i - 1] });
            i--;
            j--;
        }
        else if (table[i][j - 1] >= table[i - 1][j]) {
            ops.unshift({ kind: 'add', line: b[j - 1] });
            j--;
        }
        else {
            ops.unshift({ kind: 'del', line: a[i - 1] });
            i--;
        }
    }
    while (i > 0) {
        ops.unshift({ kind: 'del', line: a[i - 1] });
        i--;
    }
    while (j > 0) {
        ops.unshift({ kind: 'add', line: b[j - 1] });
        j--;
    }
    const lines = [];
    let shown = 0;
    for (let k = 0; k < ops.length && shown < maxLines; k++) {
        const op = ops[k];
        if (op.kind === 'eq') {
            const prev = ops[k - 1];
            const next = ops[k + 1];
            if ((prev && prev.kind !== 'eq') || (next && next.kind !== 'eq')) {
                lines.push(' ' + op.line);
                shown++;
            }
            continue;
        }
        lines.push((op.kind === 'add' ? '+' : '-') + ' ' + op.line);
        shown++;
    }
    if (lines.length === 0)
        return '';
    const truncated = ops.filter(o => o.kind !== 'eq').length > maxLines;
    const suffix = truncated ? '\n… (truncated)' : '';
    return '```' + fenceInfo + '\n' + lines.join('\n') + suffix + '\n```\n';
}
/**
 * Count added and removed lines between before/after. Simple line-level diff
 * based on longest-common-subsequence; tight budget since we only need totals
 * for the summary marker.
 */
function lineDiffCounts(before, after) {
    if (before === after)
        return { plus: 0, minus: 0 };
    const a = before.split('\n');
    const b = after.split('\n');
    const m = a.length;
    const n = b.length;
    const table = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0));
    for (let i = 1; i <= m; i++) {
        for (let j = 1; j <= n; j++) {
            table[i][j] = a[i - 1] === b[j - 1] ? table[i - 1][j - 1] + 1 : Math.max(table[i - 1][j], table[i][j - 1]);
        }
    }
    let i = m;
    let j = n;
    let plus = 0;
    let minus = 0;
    while (i > 0 && j > 0) {
        if (a[i - 1] === b[j - 1]) {
            i--;
            j--;
        }
        else if (table[i][j - 1] >= table[i - 1][j]) {
            plus++;
            j--;
        }
        else {
            minus++;
            i--;
        }
    }
    plus += j;
    minus += i;
    return { plus, minus };
}
/**
 * Short human-readable description of a tool invocation, shown in the
 * permission prompt. Keeps the message tight so the modal stays scannable.
 */
function describeToolForPrompt(name, primary, params) {
    if (name === 'write_file') {
        const bytes = params.content ? params.content.length : undefined;
        const sizeHint = bytes !== undefined ? ` (${bytes} bytes)` : '';
        return `write_file ${primary || '(path unknown)'}${sizeHint}`;
    }
    if (name === 'run_command') {
        const args = params.args ? ` ${params.args}` : '';
        return `run_command ${primary || '(cmd unknown)'}${args}`.trim();
    }
    if (name === 'git_commit') {
        return `git commit: ${params.message ? params.message.slice(0, 80) : '(no message)'}`;
    }
    if (primary)
        return `${name} ${primary}`;
    return name;
}
function sanitizeConversationName(raw, maxLength = 60) {
    if (!raw) {
        return 'New Conversation';
    }
    const withoutEmoji = raw.replace(EMOJI_REGEX, '').replace(VARIATION_SELECTORS_REGEX, '').replace(ZERO_WIDTH_JOINER_REGEX, '');
    const normalized = withoutEmoji.normalize('NFC').trim().replace(/\s+/g, ' ');
    if (!normalized) {
        return 'New Conversation';
    }
    const limited = Array.from(normalized).slice(0, maxLength).join('');
    return limited || 'New Conversation';
}
function deriveConversationNameFromEntries(entries, fallback) {
    const firstUserMessage = entries.find((entry) => entry.role === 'user' && entry.content.trim().length > 0);
    if (!firstUserMessage) {
        return sanitizeConversationName(fallback);
    }
    return sanitizeConversationName(firstUserMessage.content);
}
function createConversationId() {
    return `conv-${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`;
}
function createConversationEntry(role, content, options) {
    const entry = {
        id: `${Date.now().toString(36)}-${Math.random().toString(36).slice(2, 8)}`,
        role,
        content,
        timestamp: Date.now()
    };
    if (Array.isArray(options?.images) && options?.images.length) {
        entry.images = [...options.images];
    }
    if (typeof options?.payload === 'string' && options.payload.length > 0) {
        entry.payload = options.payload;
    }
    if (Array.isArray(options?.contextFiles) && options.contextFiles.length > 0) {
        entry.contextFiles = [...options.contextFiles];
    }
    if (options?.contextSource) {
        entry.contextSource = options.contextSource;
    }
    return entry;
}
function getNonce() {
    let text = '';
    const possible = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789';
    for (let i = 0; i < 16; i += 1) {
        text += possible.charAt(Math.floor(Math.random() * possible.length));
    }
    return text;
}
const utf8Decoder = new util_1.TextDecoder('utf-8');
const utf8Encoder = new util_1.TextEncoder();
//# sourceMappingURL=extension.js.map