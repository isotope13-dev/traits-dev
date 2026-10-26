/**
 * Returns `true` if the value is a built-in [`ArrayBuffer`](https://example.com/ArrayBuffer) or
 * [`SharedArrayBuffer`](https://example.com/SharedArrayBuffer) instance. See
 * [`ArrayBuffer.isView()`](https://example.com/ArrayBuffer/isView) for the related check.
 * Declaration files carry no executable statements: these doc links alone
 * must not read as a computed-property call cluster.
 */
declare function isAnyArrayBuffer(object: unknown): object is ArrayBufferLike;
export { isAnyArrayBuffer };
