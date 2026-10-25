function reportPrivateKeys(file: string, text: string): number {
  const isConformanceVector =
    /(?:^|\/)conformance\/(?:cases|fixtures|vectors)\//.test(
      normalizePath(file),
    )
  const pkHits = isConformanceVector ? [] : scanPrivateKeys(text)
  if (pkHits.length === 0) {
    return 0
  }
  logger.fail(`Private key found in: ${file}`)
  return 1
}

reportPrivateKeys(file, text)
