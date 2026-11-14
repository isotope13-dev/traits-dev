import { Octokit } from '@octokit/rest';

const octokit = new Octokit({ auth: process.env.GITHUB_TOKEN });
export const getIssue = (owner, repo, issue_number) =>
  octokit.issues.get({ owner, repo, issue_number });
