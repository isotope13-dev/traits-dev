// Fixture: documentation-style mention of WriteProcessMemory and CreateThread
// without any FFI binding import. The hostile composite requires a koffi
// import; plain API prose must never convict.
// See also ../declarations.js for the positive case.

/**
 * Injects a payload into a target process:
 *   1. VirtualAlloc a RWX region in the target.
 *   2. WriteProcessMemory the stage into the region.
 *   3. CreateThread at the region entry point.
 * Documented here for a defensive detection blog post; no imports below.
 */

function describeTechnique() {
    return 'VirtualAlloc + WriteProcessMemory + CreateThread';
}

module.exports = { describeTechnique };
