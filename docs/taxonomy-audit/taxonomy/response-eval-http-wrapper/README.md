# HTTP and wrapper response review

Twenty-two legacy HTTP and wrapper rules moved to execution, navigation,
encoding, URL, syntax, or evidence-profile subjects. Fetching JSON near Base64
decoding and navigation is suspicious navigation, not inherently a hostile
script loader. A paste-service URL, raw-path fragment, and HTTP-client clues do
not establish that a second stage was executed. Encoded callback fragments,
JSON cookie source text, and unbound fetch/decrypt/computed-call combinations
likewise retain descriptions limited to their evidence. Host profiling, HTTP
POST and dynamic code construction remain a probable hostile execution
objective without asserting an established data flow.

The existing positive dropper ancestor consumers retain the migrated
alternatives. The hosts-file and plugin consumers already have appropriate
URL-construction selectors; the hosts-file consumer also already selects the
script-transformation directory. Future additions to these directories require
consumer review.

The browser-navigation leaf held 93 rules. Its navigation observations were
split into location, window opening and refresh; form submission, focus/control,
source fragments and other non-navigation clues moved to their own subjects.
A social-media tasking category moved eleven related rules out of the 77-rule
command-dispatch leaf. Filename observations in that group now describe the
filename, rather than asserting that persistence was installed.

The Base64 encoding leaf held 81 rules. Eleven moved into encoding categories
for command output, file input and output writing, leaving 70 in the original
leaf. Two existing Base64-directory consumers explicitly include the new
Base64-specific leaves, preserving their expanded membership; additions to
those leaves must be reviewed for the same consumers.
