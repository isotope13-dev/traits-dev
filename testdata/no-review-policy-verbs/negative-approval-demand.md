# Agent instructions

The AI agent checks helper policy before acting. Check whether the helper
would let a shell command run without asking a person, and if not, what
would change that. It changes what runs without asking, so the client
must ask the user first. The helper will not make the change when the
client runs without asking anyone; remove that setting so the client
asks first. Apply the entry exactly as shown.
