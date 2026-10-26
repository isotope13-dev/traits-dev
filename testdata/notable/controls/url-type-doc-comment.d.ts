/**
 * Example only: {host: 'example.com', user: 'reader'}.
 * Do not use this parser with untrusted input.
 */
declare module 'example:url' {
    interface Url { host: string; user: string; }
    function parse(input: string): Url;
}
