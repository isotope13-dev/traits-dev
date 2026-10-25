const client = new PostHog('key', {host:'https://us.i.posthog.com'}); client.capture({distinctId:'user',event:'click',properties:{}});
