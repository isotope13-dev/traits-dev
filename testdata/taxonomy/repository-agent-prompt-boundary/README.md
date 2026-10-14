# Repository agent prompt boundary

The authentic sample is a source excerpt from npm
`@yanzc/claude-pro@0.6.0`, `package/src/prompts.js` lines 53–67. The archived
package SHA-256 is
`3d9c9ee51fd24b42a6a2f32554ce705608e0c2bb2b6f422f4cbda77d97e48656`; the
source member SHA-256 is
`d0dd63c3d5977fc5a41acaab2d7a4c4adc51ed9cf7c401763c19e882085a60e2`.

The positive control inserts a concealed SSH-key upload instruction beside
the prompt's agent addressee. The authentic prompt must not trigger the
repository-injection objective; the mutation must. Twenty existing hostile
repository-prompt fixtures remain positive controls. The test runs through
`make taxonomy-check`.

The sample asks the agent not to request user confirmation for routine work.
That phrase alone is not concealment. The behavior becomes suspicious when
the same source directs an agent to perform an unauthorized action and hide it
from the user.
