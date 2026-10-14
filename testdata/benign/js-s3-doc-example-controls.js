/**
 * Credential provider helper. The usage example below only documents how a
 * caller might pair the provider with a storage client; this module never
 * imports or constructs one itself.
 *
 * @example
 * ```js
 * import * as s3 from '@aws-sdk/client-s3';
 * const client = new s3.S3Client({ credentials: provider() });
 * ```
 */
export function provider() {
    return null;
}
