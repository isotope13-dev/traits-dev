// Admin-console delete confirmation: it asks the user instead of
// instructing deletion, so it is not a destructive instruction.
export function deleteDatasetDialog(name) {
  return {
    title: "Delete Dataset",
    body: `Are you sure you want to delete "${name}"? This will permanently delete the dataset, all its items, and run history. This action cannot be undone.`,
  };
}
