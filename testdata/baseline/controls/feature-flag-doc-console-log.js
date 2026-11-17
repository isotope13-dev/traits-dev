/**
 * Get all feature flag values for a user.
 * @example
 * const allFlags = await client.getAllFlags('user_123')
 * console.log('User flags:', allFlags)
 */
export function describeFlags(allFlags) {
  return Object.keys(allFlags);
}
