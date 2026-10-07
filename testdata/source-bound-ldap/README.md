These fixtures model Figure 9 of Arctic Wolf's technical report:
https://arcticwolf.com/resources/blog/inside-fortibleed-reverse-engineering-the-cyberstrike-harvester-behind-a-global-fortigate-credential-factory/

The positive fixture combines a global socket connect override, source binding,
and LDAP selection of preauthentication-disabled and noncomputer SPN accounts.
Documentation addresses and placeholder credentials replace redacted values.
Two suspicious account-discovery findings are expected. This is not proof of
hash extraction, cracking, or unauthorized access.

The negative fixtures independently remove routing, remove LDAP discovery,
or replace both targeted filters. None should match either discovery composite.
The cases.json file records the exact expected findings. All four cases were
checked with cleave's JSON output.
