# Fetch and executable-permission review

The legacy shell and direct-IP fetch-and-execute rules now live with command
execution. Rules requiring an executable permission change are grouped in the
`command/chmod` sink alongside existing rules for the same sequence; download
and launch rules without that condition remain under `command/fetch`.

The previous fetch directory had 68 rules. Moving its existing permission-change
rules while migrating the legacy rules leaves 51 rules in each destination.
All direct consumers and exclusions were updated. Filename-based test-directory
exclusions were removed from the reviewed rules because the filename does not
make an observed download-and-launch sequence benign.
