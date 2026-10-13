import { execSync } from "node:child_process";
execSync(`rsync -a --delete --exclude Singleton* "${src}/" "${dst}/"`);
