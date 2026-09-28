function deduplicateAll(depGraph, duplicates) {
  const { depPathsMap, remainingDuplicates } = deduplicateDepPaths(duplicates, depGraph)
  if (remainingDuplicates.length === duplicates.length) return depPathsMap

  for (const node of Object.values(depGraph)) {
    for (const [alias, childDepPath] of Object.entries(node.children)) {
      if (depPathsMap[childDepPath]) node.children[alias] = depPathsMap[childDepPath]
    }
  }

  if (Object.keys(depPathsMap).length > 0) {
    return { ...depPathsMap, ...deduplicateAll(depGraph, remainingDuplicates) }
  }
  return depPathsMap
}

function deduplicateDepPaths(duplicates) {
  const depPathsMap = {}
  return { depPathsMap, remainingDuplicates: duplicates }
}

export { deduplicateAll }
