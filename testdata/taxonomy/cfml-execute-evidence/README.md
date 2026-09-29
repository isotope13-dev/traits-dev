Static call and named-field controls; never execute these files.

The comment-only case reproduced both old execution findings. Literal,
interpolated and opaque output-file values must preserve attribute presence.
Missing attributes, attribute text in another value, another tag, duplicate
attributes, quoted/commented source and an ordinary function with the tag's
name must not be mistaken for CFEXECUTE tag output configuration.
