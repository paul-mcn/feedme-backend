"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
// const server = require('./server');
const index_1 = __importDefault(require("./server/index"));
const config_1 = require("./config");
const origin = (config_1.mode === 'development')
    ? ["http://127.0.0.1:3000", "http://localhost:3000", "http://192.168.20.14:3000"]
    : "https://organisemymeals.com";
const server = new index_1.default(origin);
server.start();
