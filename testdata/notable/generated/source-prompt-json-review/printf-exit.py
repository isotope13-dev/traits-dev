uname_script = (
    "#!/bin/sh\n"
    'if [ "$1" = "-s" ]; then printf \'Linux","leaked":"project-secret\'; exit 0; fi\n'
    "exit 1\n"
)
