'use strict';

/**
 * Claude 配置工具函数
 * 供 setapi_cc.js、setapi_cx.js 等命令模块共享使用
 */

var fs = require('fs');
var path = require('path');
var { execSync, spawnSync } = require('child_process');

// ============================================================
// AI 渠道列表（运行时由 fetchConfig 从服务端拉取填充）
// ============================================================
var API_CHANNELS = [];

// Codex 渠道列表（运行时由 fetchConfig 从服务端 cxChannels 填充）
var CX_CHANNELS = [];

// weds 渠道列表（运行时由 fetchConfig 从服务端 wedsChannels 填充）
var WEDS_CHANNELS = [];

// 公告列表（运行时由 fetchConfig 从服务端拉取填充）
var noticeList = [];

// weds 公告列表（运行时由 fetchConfig 从服务端 noticeWedsList 填充）
var noticeWedsList = [];

// jcc.json 中保存最后一次手动输入 Token 的内部字段名
var LAST_MANUAL_AUTH_TOKEN_KEY = '__lastManualAuthToken';

/**
 * 使用 Node.js 18 内置 fetch 读取远程文本，并提供超时控制
 * @param {string} url 请求地址
 * @param {number} timeoutMs 超时时间（毫秒）
 * @returns {Promise<{ ok: boolean, status: number, text: string }>}
 */
async function fetchRemoteText(url, timeoutMs) {
    var controller = new AbortController();
    var timer = setTimeout(function () {
        controller.abort();
    }, timeoutMs);
    try {
        var res = await fetch(url, { signal: controller.signal });
        var text = await res.text();
        return { ok: res.ok, status: res.status, text: text };
    } finally {
        clearTimeout(timer);
    }
}

/**
 * 从当前入口文件名推断正在运行的 CLI 命令名
 * @returns {string} jcc、jcx、weds 或空字符串
 */
function getCurrentCliName() {
    var entryName = path.basename(process.argv[1] || '').toLowerCase();
    if (entryName === 'jcx' || entryName === 'jcx.js') return 'jcx';
    if (entryName === 'jcc' || entryName === 'jcc.js') return 'jcc';
    if (entryName === 'weds' || entryName === 'weds.js') return 'weds';
    return '';
}

/**
 * 升级完成后重新运行当前 CLI，并保留本次传入的全部参数
 * @returns {void}
 */
function rerunCurrentCli() {
    var cliName = getCurrentCliName();
    if (!cliName) {
        console.log('[fetchConfig] 升级完成，未识别当前 CLI，请重新运行');
        process.exit(0);
    }

    // 传递临时环境变量，避免新进程在版本缓存异常时反复触发升级。
    var childEnv = Object.assign({}, process.env, {
        BASE_PARTS_AI_SKIP_SELF_UPDATE: '1',
    });
    var args = process.argv.slice(2);
    console.log('[fetchConfig] 升级完成，正在重新运行: ' + cliName + (args.length ? ' ' + args.join(' ') : ''));
    var result = spawnSync(cliName, args, {
        stdio: 'inherit',
        shell: process.platform === 'win32',
        env: childEnv,
    });

    if (result.error) {
        console.warn('[fetchConfig] 重新运行失败:', result.error.message);
        process.exit(1);
    }
    if (result.signal) {
        console.warn('[fetchConfig] 重新运行被信号中断:', result.signal);
        process.exit(1);
    }
    process.exit(typeof result.status === 'number' ? result.status : 0);
}

/**
 * 从服务端拉取渠道配置，并检查 jcc 自身是否需要升级
 * @param {object} buildCfg getBuildCfg 返回的配置对象
 * @returns {Promise<void>}
 */
async function fetchConfig(buildCfg) {
    var url = 'https://jai.jaskle.cn/hm/hm_pub/ai_cc_cfg?r=' + Math.random();
    try {
        var response = await fetchRemoteText(url, 8000);
        if (!response.ok) {
            console.warn('[fetchConfig] 请求失败: HTTP ' + response.status);
            return;
        }

        var result = JSON.parse(response.text);
        if (result.code === 0 && result.data) {
            // 将服务端返回的渠道列表填充到 API_CHANNELS
            if (Array.isArray(result.data.channels)) {
                API_CHANNELS.length = 0;
                result.data.channels.forEach(function (ch) {
                    API_CHANNELS.push(ch);
                });
                console.log('[fetchConfig] 已拉取 ' + API_CHANNELS.length + ' 个渠道');
            }
            // 将服务端返回的 Codex 渠道列表填充到 CX_CHANNELS
            if (Array.isArray(result.data.cxChannels)) {
                CX_CHANNELS.length = 0;
                result.data.cxChannels.forEach(function (ch) {
                    CX_CHANNELS.push(ch);
                });
                console.log('[fetchConfig] 已拉取 ' + CX_CHANNELS.length + ' 个 Codex 渠道');
            }
            // 将服务端返回的 weds 渠道列表填充到 WEDS_CHANNELS
            if (Array.isArray(result.data.wedsChannels)) {
                WEDS_CHANNELS.length = 0;
                result.data.wedsChannels.forEach(function (ch) {
                    WEDS_CHANNELS.push(ch);
                });
                console.log('[fetchConfig] 已拉取 ' + WEDS_CHANNELS.length + ' 个 weds 渠道');
            }
            // 解析公告列表
            if (Array.isArray(result.data.noticeList)) {
                noticeList.length = 0;
                result.data.noticeList.forEach(function (item) {
                    noticeList.push(item);
                });
            }
            // 解析 weds 公告列表
            if (Array.isArray(result.data.noticeWedsList)) {
                noticeWedsList.length = 0;
                result.data.noticeWedsList.forEach(function (item) {
                    noticeWedsList.push(item);
                });
            }
            // 检查 jcc 自身版本，若需要升级则询问用户确认后安装
            var currentVer = '';
            try { currentVer = require('../package.json').version; } catch (e) { }
            var newVer = result.data.newVer || '';
            // 比较语义化版本号，仅当服务端版本大于当前版本时才升级
            function semverGt(a, b) {
                var pa = a.split('.').map(Number);
                var pb = b.split('.').map(Number);
                for (var i = 0; i < 3; i++) {
                    if ((pa[i] || 0) > (pb[i] || 0)) return true;
                    if ((pa[i] || 0) < (pb[i] || 0)) return false;
                }
                return false;
            }
            if (newVer && process.env.BASE_PARTS_AI_SKIP_SELF_UPDATE !== '1' && semverGt(newVer, currentVer)) {
                console.log('[fetchConfig] 检测到新版本: ' + newVer + '（当前 ' + currentVer + '）');
                var confirmed = "yes"
                // confirmed = await select({
                //     message: '是否立即升级？',
                //     default: 'yes',
                //     choices: [
                //         { name: '立即升级', value: 'yes' },
                //         { name: '跳过', value: 'no' },
                //     ],
                // });
                if (confirmed === 'yes') {
                    console.log('[fetchConfig] 正在升级...');
                    // 用 select 上下选，默认高亮"立即升级"
                    try {
                        var tgzUrl = 'https://jdwfiles.oss-cn-hangzhou.aliyuncs.com/npm_pkg/base_parts_ai-' + newVer + '.tgz';
                        spawnSync('npm', ['install', '-g', tgzUrl, '--force'], {stdio: 'inherit'});
                        rerunCurrentCli();
                    } catch (e) {
                        console.warn('[fetchConfig] 自动升级失败:', e.message);
                    }
                } else {
                    console.log('[fetchConfig] 已跳过升级，继续使用当前版本');
                }
            }
        } else {
            console.warn('[fetchConfig] 服务端返回异常:', result.msg || JSON.stringify(result));
        }
    } catch (e) {
        if (e && e.name === 'AbortError') {
            console.warn('[fetchConfig] 请求超时');
        } else if (e instanceof SyntaxError) {
            console.warn('[fetchConfig] 解析响应失败:', e.message);
        } else {
            console.warn('[fetchConfig] 请求失败:', e.message);
        }
    }
}

/**
 * 读取 JSON 文件，出错返回默认值
 * @param {string} filePath 文件路径
 * @param {*} defaultVal 出错时的默认值
 * @returns {*}
 */
function readJsonFile(filePath, defaultVal) {
    try {
        var content = fs.readFileSync(filePath, 'utf8');
        return JSON.parse(content);
    } catch (e) {
        return defaultVal;
    }
}

/**
 * 写入 JSON 文件（自动创建目录）
 * @param {string} filePath 文件路径
 * @param {*} data 要写入的对象
 */
function writeJsonFile(filePath, data) {
    var dir = path.dirname(filePath);
    if (!fs.existsSync(dir)) {
        fs.mkdirSync(dir, { recursive: true });
    }
    fs.writeFileSync(filePath, JSON.stringify(data, null, 4), 'utf8');
}

/**
 * 读取 settings.json，确保 env 字段存在
 * @param {string} settingsPath settings.json 路径
 * @returns {object}
 */
function loadSettings(settingsPath) {
    var settings = readJsonFile(settingsPath, {});
    if (!settings.env) {
        settings.env = {};
    }
    return settings;
}

/**
 * 获取 ai_tip 接口使用的当前系统标识
 * 将 Node.js 平台和 CPU 架构归一化为服务端识别的 os 参数
 * @returns {string} 例如 windows_x64、linux_x64、macos_arm64
 */
function getAiTipOsParam() {
    var platformMap = {
        win32: 'windows',
        linux: 'linux',
        darwin: 'macos',
    };
    var archMap = {
        ia32: 'x86',
        x64: 'x64',
        arm: 'arm',
        arm64: 'arm64',
    };
    var platformName = platformMap[process.platform] || process.platform;
    var archName = archMap[process.arch] || process.arch;
    return platformName + '_' + archName;
}

/**
 * 构建 SessionStart Hook 中调用 ai_tip 的命令
 * os 参数在写入配置时按当前运行环境固定，避免运行时依赖占位符替换
 * @returns {string}
 */
function buildAiTipCommand() {
    return 'curl -s -m 5 ' + buildAiTipUrl('cc');
}

/**
 * 构建 ai_tip 接口地址
 * @param {string} cli 客户端标识，例如 cc 或 cx
 * @returns {string}
 */
function buildAiTipUrl(cli) {
    return 'https://jai.jaskle.cn/hm/pub/ai_tip?cli=' + cli + '-' + getAiTipOsParam();
}

/**
 * 读取远程文本内容，失败时返回空字符串
 * @param {string} url 请求地址
 * @returns {Promise<string>}
 */
async function fetchText(url) {
    try {
        var response = await fetchRemoteText(url, 8000);
        if (!response.ok) {
            console.warn('[fetchText] 请求失败: HTTP ' + response.status);
            return '';
        }
        return response.text;
    } catch (e) {
        if (e && e.name === 'AbortError') {
            console.warn('[fetchText] 请求超时');
        } else {
            console.warn('[fetchText] 请求失败:', e.message);
        }
        return '';
    }
}

/**
 * 获取渠道配置中强制指定的 ANTHROPIC_AUTH_TOKEN
 * 仅当服务端 envObj 显式带有非空 Token 时返回，用于跳过用户输入
 * @param {object} channel 渠道配置对象
 * @returns {string}
 */
function getChannelAuthToken(channel) {
    if (!channel || !channel.envObj || !Object.prototype.hasOwnProperty.call(channel.envObj, 'ANTHROPIC_AUTH_TOKEN')) {
        return '';
    }
    var token = channel.envObj.ANTHROPIC_AUTH_TOKEN;
    return typeof token === 'string' ? token.trim() : '';
}

/**
 * 记录最后一次由用户手动输入的 Token
 * 该值只作为后续输入提示默认值，不代表当前渠道配置
 * @param {object} jccJson jcc.json 对象
 * @param {string} token 用户手动输入的 Token
 */
function saveLastManualAuthToken(jccJson, token) {
    if (!jccJson.keys) { jccJson.keys = {}; }
    if (token) {
        jccJson.keys[LAST_MANUAL_AUTH_TOKEN_KEY] = token;
    }
}

/**
 * 获取最后一次手动输入的 Token
 * @param {object} jccJson jcc.json 对象
 * @returns {string}
 */
function getLastManualAuthToken(jccJson) {
    return (jccJson.keys && jccJson.keys[LAST_MANUAL_AUTH_TOKEN_KEY]) || '';
}

/**
 * 计算需要提示用户输入 Token 时的默认值
 * 优先使用当前渠道缓存；只有该渠道无缓存时，才使用当前渠道配置或最后一次手动 Token 兜底
 * @param {object} jccJson jcc.json 对象
 * @param {string} channelId 当前渠道 id
 * @param {object} settings Claude settings.json 对象
 * @returns {string}
 */
function getManualAuthTokenDefault(jccJson, channelId, settings) {
    var cachedToken = (jccJson.keys && jccJson.keys[channelId]) || '';
    var currentToken = (settings.env && settings.env.ANTHROPIC_AUTH_TOKEN) || '';
    var currentChannelToken = (!settings.__jid || settings.__jid === channelId) ? currentToken : '';
    return cachedToken || currentChannelToken || getLastManualAuthToken(jccJson) || currentToken;
}

/**
 * 根据 settings 中的 __jid 字段匹配当前渠道
 * @param {object} settings Claude settings.json 对象
 * @param {Array<object>} channels 渠道列表，默认使用 API_CHANNELS
 * @returns {{ channel: object|null, key: string, jid: string }}
 */
function getCurrentInfo(settings, channels) {
    var channelList = channels || API_CHANNELS;
    // 当前渠道 id，存储在 settings 顶层 __jid 字段
    var currentJid = settings.__jid || '';
    var currentKey = (settings.env && settings.env.ANTHROPIC_AUTH_TOKEN) || '';
    // 按 id 匹配渠道
    var channel = currentJid ? (channelList.find(function (c) { return c.id === currentJid; }) || null) : null;
    return { channel: channel, key: currentKey, jid: currentJid };
}

/**
 * 对 API Key 做脱敏显示（前4后4，中间****）
 * @param {string} key
 * @returns {string}
 */
function maskKey(key) {
    if (!key) return '(未设置)';
    if (key.length > 8) return key.slice(0, 4) + '****' + key.slice(-4);
    return '****';
}

/**
 * 打印当前渠道和Key状态
 * @param {object} settings Claude settings.json 对象
 * @param {Array<object>} channels 渠道列表，默认使用 API_CHANNELS
 */
function printCurrentInfo(settings, channels) {
    var info = getCurrentInfo(settings, channels);
    // console.log('\n====== 当前 Claude 配置 ======');
    let curSelectedChannel = '(' + (info.jid || '未设置') + ')';
    if (info.channel) {
        curSelectedChannel = info.channel.name;
    }
    console.log('\x1b[33m当前渠道: ' + curSelectedChannel + ', Key: ' + maskKey(info.key) + '');
    console.log('============================================================\x1b[0m\n');
}

/**
 * 显示公告信息（黄色字体逐行输出），有公告时等待用户按回车继续
 * @param {string} type 公告类型，weds 使用 noticeWedsList，其它使用默认 noticeList
 * @returns {Promise<void>}
 */
function showNotice(type) {
    var list = type === 'weds' ? noticeWedsList : noticeList;
    if (!list.length) return Promise.resolve();
    console.log('\n\x1b[33m=========================== 公告 ===========================');
    list.forEach(function (line) {
        console.log(line);
    });
    console.log('============================================================\x1b[0m');
    // // 等待用户按回车继续
    // return new Promise(function (resolve) {
    //     var rl = readline.createInterface({ input: process.stdin, output: process.stdout });
    //     rl.question('按回车键继续...', function () {
    //         rl.close();
    //         resolve();
    //     });
    // });
}

module.exports = {
    API_CHANNELS,
    CX_CHANNELS,
    WEDS_CHANNELS,
    fetchConfig,
    fetchText,
    readJsonFile,
    writeJsonFile,
    loadSettings,
    getAiTipOsParam,
    buildAiTipUrl,
    buildAiTipCommand,
    getChannelAuthToken,
    saveLastManualAuthToken,
    getLastManualAuthToken,
    getManualAuthTokenDefault,
    getCurrentInfo,
    maskKey,
    printCurrentInfo,
    showNotice,
    noticeList,
    noticeWedsList,
};
