// A tenant-scoped secret store uses its own encrypted gateway credential.
export async function load(db, tenant, vault) {
  const result = await db.query("SELECT encrypted_key FROM gateway_keys WHERE tenant_id = $1", [tenant]);
  return result.rows.length ? vault.decrypt(result.rows[0].encrypted_key) : null;
}
