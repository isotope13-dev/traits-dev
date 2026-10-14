Skill-SSH tunnel needs a skill-sized carrier
==================================================

`packaged-agent-skill-ssh-key-tunnel` pooled its legs across whole source
trees: a skill manifest in one corner, CI testbox SSH setup in another,
and documented remote tunnels elsewhere scored "skill deploys SSH access".
The composite now carries the same 32MB carrier bound as its CI siblings:
a skill package is kilobytes, a monorepo is not one. Small carriers still
convict.

Run `python3 testdata/skill-ssh-carrier-bound/check.py
<scratch-directory>`. `evil-skill-positive.zip` (skill entry plus
`authorized_keys` append and `ssh -R` in one small package) must report
the trait. The OpenClaw tree (76MB, legs in unrelated features) is the
negative and stays silent.
