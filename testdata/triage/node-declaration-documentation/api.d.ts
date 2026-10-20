declare module "example:console" {
    /** Defaults: process.stdin, process.cwd(), eval(source). */
    interface Options {
        "test:stdout": string;
        "test:stderr": string;
        evalCmd: string;
        callback: (result: unknown) => void;
    }
}
