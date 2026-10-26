import { tsImport } from "tsx/esm/api";
export const load = (file: string) => tsImport(file, import.meta.url);
