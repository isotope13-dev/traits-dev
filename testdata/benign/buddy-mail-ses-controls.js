// Benign control: buddy-style mail provisioning. Resolves the operator's own
// AWS credentials to operate the operator's own mail infrastructure over
// the SES API.
const { readFileSync, existsSync } = require('node:fs')

function loadSesCredentials(profile) {
  const credentialsPath = `${process.env.HOME}/.aws/credentials`
  if ((!process.env.AWS_ACCESS_KEY_ID || !process.env.AWS_SECRET_ACCESS_KEY) && existsSync(credentialsPath)) {
    for (const line of readFileSync(credentialsPath, 'utf8').split('\n')) {
      const separator = line.indexOf('=')
      if (separator > 0) {
        const key = line.slice(0, separator).trim()
        const value = line.slice(separator + 1).trim()
        if (key === 'aws_access_key_id') process.env.AWS_ACCESS_KEY_ID = value
        if (key === 'aws_secret_access_key') process.env.AWS_SECRET_ACCESS_KEY = value
      }
    }
  }
  return { profile, region: process.env.AWS_REGION || 'us-east-1' }
}

function mailCommands(buddy) {
  buddy.command('mail:storage:kms:ensure', 'Create the production mail KMS key').action(async (options) => {
    const { profile, region } = loadSesCredentials(options.profile)
    const response = await fetch(`https://email.${region}.amazonaws.com/`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: `Action=ListIdentities&Version=2010-12-01`,
    })
    console.log(`mail-storage kms ensure for ${profile}: ${response.status}`)
  })
}

module.exports = { mailCommands }
