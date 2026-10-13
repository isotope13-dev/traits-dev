import {readdirSync} from "node:fs";
const first = readdirSync(root, {withFileTypes:true});
const second = readdirSync(other, {withFileTypes:true});
const dirs = first.filter(entry => entry.isDirectory());
const otherDirs = second.filter(entry => entry.isDirectory());
