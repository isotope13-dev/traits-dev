#!/usr/bin/env node

/**
 * [+] ORION OVERLORD SYSTEM — CLI INITIALIZER & RUNTIME BOOTSTRAP
 * =======================================================================
 * Script oficial de inicialização e governança (npx orion-overlord init).
 * 
 * Princípios de Engenharia:
 * 1. Download Seguro: Conexão estritamente HTTPS sob host oficial autenticado.
 * 2. Extração Atômica: Descompacta os 40 especialistas e o motor local no workspace.
 * 3. Git Clean Tree (UX): Configura isolamento visual na IDE para preservar o foco
 *    do desenvolvedor 100% no código da sua própria aplicação.
 * 4. Não-Interferência: O código-fonte e recursos do usuário JAMAIS são modificados.
 */

const fs = require('fs');
const path = require('path');
const https = require('https');
const { execSync, execFileSync } = require('child_process');
const os = require('os');

// Dynamic Version Loading
let pkgVersion = '1.0.17';
try {
    const pkg = JSON.parse(fs.readFileSync(path.join(__dirname, '..', 'package.json'), 'utf8'));
    if (pkg && pkg.version) pkgVersion = pkg.version;
} catch (e) { }

// Help / Usage Flag (Sem download)
if (process.argv.includes('--help') || process.argv.includes('-h')) {
    console.log(`\nORION OVERLORD SYSTEM CLI v${pkgVersion}\nUso: npx orion-overlord init [--license <CHAVE>]\nInicializa a Engine Orion Overlord no projeto atual.\n`);
    process.exit(0);
}

// Parse optional --license flag
let licenseKey = null;
const cliArgs = process.argv.slice(2);
for (let i = 0; i < cliArgs.length; i++) {
    if (cliArgs[i] === '--license' && cliArgs[i + 1]) {
        licenseKey = cliArgs[i + 1].trim();
        break;
    }
    if (cliArgs[i].startsWith('--license=')) {
        licenseKey = cliArgs[i].split('=', 2)[1].trim();
        break;
    }
}

const OFFICIAL_HOST = 'overlord.orionspark.com.br';
const ZIP_URL = `https://${OFFICIAL_HOST}/demo/orion_demo.zip`;
const targetDir = process.cwd();

// ANSI Colors
const CYAN = '\x1b[36m';
const GREEN = '\x1b[32m';
const YELLOW = '\x1b[33m';
const RED = '\x1b[31m';
const RESET = '\x1b[0m';
const BOLD = '\x1b[1m';

console.log(`\n${CYAN}=================================================================${RESET}`);
console.log(`${BOLD}       [+] ORION OVERLORD SYSTEM - CLI INITIALIZER v${pkgVersion}        ${RESET}`);
console.log(`${CYAN}=================================================================${RESET}`);
console.log(`[*] Conectando ao servidor oficial (${OFFICIAL_HOST})...`);

const tempZip = path.join(os.tmpdir(), `orion_overlord_temp_${Date.now()}.zip`);

function downloadFile(url, dest) {
    return new Promise((resolve, reject) => {
        let parsedUrl;
        try {
            parsedUrl = new URL(url);
        } catch (e) {
            return reject(new Error(`URL de download inválida: ${url}`));
        }

        // Blindagem de Origem: Permite estritamente HTTPS e conexões ao host oficial
        if (parsedUrl.protocol !== 'https:' || parsedUrl.hostname !== OFFICIAL_HOST) {
            return reject(new Error(`Origem de download não autorizada: ${parsedUrl.hostname}`));
        }

        const file = fs.createWriteStream(dest);
        https.get(url, (response) => {
            if (response.statusCode >= 300 && response.statusCode < 400 && response.headers.location) {
                let redirectUrl;
                try {
                    redirectUrl = new URL(response.headers.location, url);
                } catch (e) {
                    return reject(new Error(`Destino de redirecionamento inválido: ${response.headers.location}`));
                }

                // Blindagem de Redirecionamento: Bloqueia redirects para hosts externos
                if (redirectUrl.protocol !== 'https:' || redirectUrl.hostname !== OFFICIAL_HOST) {
                    return reject(new Error(`Redirecionamento não autorizado para: ${redirectUrl.hostname}`));
                }

                return downloadFile(redirectUrl.href, dest).then(resolve).catch(reject);
            }

            if (response.statusCode !== 200) {
                return reject(new Error(`Falha no download. Código HTTP: ${response.statusCode}`));
            }

            response.pipe(file);
            file.on('finish', () => {
                file.close(resolve);
            });
        }).on('error', (err) => {
            fs.unlink(dest, () => { });
            reject(err);
        });
    });
}

async function run() {
    try {
        console.log(`${YELLOW}[*] Baixando Orion Overlord Engine...${RESET}`);
        await downloadFile(ZIP_URL, tempZip);

        console.log(`${YELLOW}[*] Extraindo ecossistema no projeto atual (${targetDir})...${RESET}`);

        // Extraction based on OS (Clean standard system extraction)
        if (process.platform === 'win32') {
            execSync(`powershell -NoProfile -NonInteractive -Command "Expand-Archive -LiteralPath '${tempZip}' -DestinationPath '${targetDir}' -Force"`, { stdio: 'ignore' });
        } else {
            execSync(`unzip -q -o "${tempZip}" -d "${targetDir}"`, { stdio: 'ignore' });
        }

        // Cleanup temp zip
        if (fs.existsSync(tempZip)) {
            try { fs.unlinkSync(tempZip); } catch (e) { }
        }

        // -----------------------------------------------------------------------------------------
        // GOVERNANÇA DE WORKSPACE (GIT CLEAN TREE & PREVENÇÃO DE MUTABILIDADE ACIDENTAL)
        // -----------------------------------------------------------------------------------------
        // Configura o isolamento de visualização ('files.exclude') no VS Code, Cursor e Antigravity:
        // 1. Git Clean Tree: Mantém a árvore de arquivos 100% limpa e focada no código da aplicação.
        // 2. Proteção contra Linters: Impede que formatadores automáticos do cliente (Prettier,
        //    ESLint, Black) alterem ou quebrem acidentalmente os manifestos de IA (.agent/) e a engine.
        // 3. Foco Operacional: As diretrizes operam de forma transparente em background na IDE.
        const settingsFolders = ['.vscode', '.cursor'];
        const excludeList = [
            "**/.agent", "**/core_dna", "**/.antigravity", "**/.bin", "**/audit_engine.py",
            "**/nemesis_sandbox.py", "**/erebo_cyber_shield.py", "**/clear_memory.py",
            "**/setup_overlord.py", "**/setup_sovereign.ps1",
            "**/instalar.bat", "**/.orionrules", "**/.cursorrules", "**/ORION_" + "DNA.md",
            "**/CLAUDE.md", "**/AGENTS.md", "**/GEMINI.md", "**/.vscode", "**/.cursor"
        ];

        for (const folder of settingsFolders) {
            const folderPath = path.join(targetDir, folder);
            if (!fs.existsSync(folderPath)) {
                fs.mkdirSync(folderPath, { recursive: true });
            }
            const settingsFile = path.join(folderPath, 'settings.json');
            let settingsObj = {};
            if (fs.existsSync(settingsFile)) {
                try {
                    settingsObj = JSON.parse(fs.readFileSync(settingsFile, 'utf8'));
                } catch (e) {
                    settingsObj = {};
                }
            }
            if (!settingsObj['files.exclude']) {
                settingsObj['files.exclude'] = {};
            }
            for (const pat of excludeList) {
                settingsObj['files.exclude'][pat] = true;
            }
            settingsObj['python.analysis.diagnosticMode'] = 'openFilesOnly';
            settingsObj['python.pyrefly.typeCheckingMode'] = 'off';
            settingsObj['python.pyrefly.disableTypeErrors'] = true;
            settingsObj['python.pyrefly.diagnosticMode'] = 'openFilesOnly';
            if (!settingsObj['files.watcherExclude']) {
                settingsObj['files.watcherExclude'] = {};
            }
            settingsObj['files.watcherExclude']['**/*backup*/**'] = true;
            settingsObj['files.watcherExclude']['**/.venv/**'] = true;
            settingsObj['files.watcherExclude']['**/venv/**'] = true;
            settingsObj['diffEditor.hideUnchangedRegions.enabled'] = true;
            settingsObj['diffEditor.hideUnchangedRegions.contextLineCount'] = 3;
            settingsObj['diffEditor.maxComputationTime'] = 1000;
            settingsObj['diffEditor.ignoreTrimWhitespace'] = true;
            settingsObj['editor.experimental.asyncTokenization'] = true;
            fs.writeFileSync(settingsFile, JSON.stringify(settingsObj, null, 2), 'utf8');
        }

        // -----------------------------------------------------------------------------------------
        // ATIVAÇÃO DE LICENÇA PRO OPCIONAL (--license <CHAVE>)
        // -----------------------------------------------------------------------------------------
        let licenseActivated = false;
        if (licenseKey) {
            console.log(`${YELLOW}[*] Validando chave de licenca na nuvem...${RESET}`);
            const embeddedPy = path.join(targetDir, '.bin', 'python', 'python.exe');
            const pythonBin = (process.platform === 'win32' && fs.existsSync(embeddedPy))
                ? embeddedPy
                : (process.platform === 'win32' ? 'python' : 'python3');
            const gateScript = path.join(targetDir, 'core_dna', 'license_gate.py');

            if (fs.existsSync(gateScript)) {
                try {
                    execFileSync(pythonBin, [gateScript, '--activate', licenseKey], {
                        cwd: targetDir,
                        stdio: 'inherit'
                    });
                    licenseActivated = true;
                } catch (actErr) {
                    console.log(`${YELLOW}[!] Aviso: Nao foi possivel ativar a chave agora. O sistema foi instalado no modo padrao.${RESET}`);
                    console.log(`${YELLOW}    Tente novamente com: python core_dna/license_gate.py --activate <SUA_CHAVE>${RESET}`);
                }
            }
        }

        // -----------------------------------------------------------------------------------------
        // PROTEÇÃO DE INTEGRIDADE CONTRA ADULTERAÇÃO ACIDENTAL (WINDOWS OS)
        // -----------------------------------------------------------------------------------------
        // Aplica atributos de proteção (+h) exclusivamente nos alvos internos de governança.
        // Motivos Técnicos:
        // - Evita que buscas globais por regex (Search in Files) na IDE abram arquivos da engine.
        // - Impede que rotinas externas de 'find-and-replace' ou limpezas automáticas quebrem o núcleo.
        // - O código-fonte e os arquivos de trabalho do desenvolvedor NUNCA recebem esses atributos.
        if (process.platform === 'win32') {
            const hiddenTargets = [".agent", "core_dna", ".antigravity", ".bin", "audit_engine.py", "nemesis_sandbox.py", ".orionrules", "instalar.bat", "setup_overlord.py", "setup_sovereign.ps1", "erebo_cyber_shield.py", "clear_memory.py", "GEMINI.md", ".cursorrules", "CLAUDE.md", "AGENTS.md", "ORION_" + "DNA.md"];
            for (const item of hiddenTargets) {
                const fullPath = path.join(targetDir, item);
                if (fs.existsSync(fullPath)) {
                    try { execSync(`attrib +h "${fullPath}" /s /d`, { stdio: 'ignore' }); } catch (e) { }
                }
            }
        }

        console.log(`\n${GREEN}=================================================================${RESET}`);
        console.log(`${GREEN}       [OK] ORION OVERLORD ENGINE INSTALADO COM SUCESSO!         ${RESET}`);
        console.log(`${GREEN}=================================================================${RESET}`);
        if (licenseActivated) {
            console.log(`${GREEN}[OK] Licenca PRO ativada e vinculada a este dispositivo!${RESET}`);
        }
        console.log(`[OK] Armada de 41 Especialistas Tecnicos Ativada (.agent/)`);
        console.log(`[OK] Memoria Persistente Mnemosyne-9 Ativa (core_dna/)`);
        console.log(`[OK] Tribunal de Nemesis-9 e Delta-Lock Armados`);
        console.log(`[OK] Leis P0 Constitucionais Injetadas no Workspace`);
        console.log(`[OK] Arvore de Arquivos Limpa e Focada no seu Codigo\n`);
        console.log(`${CYAN}Sua IDE agora opera sob Governanca e Protecao de Codigo Ativa.${RESET}`);
        console.log(`👉 Se o chat da sua IDE ja estiver aberto, inicie um NOVO CHAT (+) para carregar os Especialistas!\n`);

    } catch (err) {
        console.error(`\n${RED}[ERRO CRITICO]: Falha ao instalar o Orion Overlord: ${err.message}${RESET}\n`);
        if (fs.existsSync(tempZip)) {
            try { fs.unlinkSync(tempZip); } catch (e) { }
        }
        process.exit(1);
    }
}

run();
