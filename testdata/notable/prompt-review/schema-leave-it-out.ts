// Schema metadata advising callers to omit an optional local-only parameter
// inside an agent run is parameter guidance, not prompt injection.
const schema = {
  requestId: describe(
    "Local development shell only. Leave it out inside an agent run.",
  ),
};

export const action = defineAction({
  description:
    "Post one reply on the review thread as the AI agent, and finish the request.",
});
