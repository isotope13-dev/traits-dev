"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
const net_12 = __importDefault(require("net"));
const tls_12 = __importDefault(require("tls"));
exports.connect = function (host, port) {
    const socket = net_12.default.connect(port, host);
    return tls_12.default.connect({host, socket, rejectUnauthorized: true});
};
