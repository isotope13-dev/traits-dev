async function currentBranch(git, repo) {
  const result = await git.exec({ cwd: repo }, "branch", "--show-current");
  return result.stdout.trim();
}

function describeText() {
  return { text: "ordinary editor label" };
}
