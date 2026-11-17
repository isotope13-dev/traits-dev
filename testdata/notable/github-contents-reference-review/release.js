export async function writeReleaseNotes(octokit, owner, repo, notes) {
  return octokit.rest.repos.createOrUpdateFileContents({
    owner, repo, path: 'CHANGELOG.md', message: 'Update release notes',
    content: Buffer.from(notes).toString('base64')
  });
}
