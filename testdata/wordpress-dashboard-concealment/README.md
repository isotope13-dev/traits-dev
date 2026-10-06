The positive fixture reconstructs the documented administrator creation and
`users_list_table_query_args` / `login__not_in` persistence mechanism from
https://patchstack.com/articles/four-ways-back-in-the-wordpress-xss-campaign-that-hides-its-own-admin-account/.

Negative fixtures separate account creation, query exclusion, and hook registration.
The detection describes co-occurrence within one file; it does not prove that
the created and excluded usernames are identical. Both rules are suspicious.

The query observations move from software identity to database query mechanics.
Administrator creation moves from webshell to account persistence. The duplicate
archive-scoped hostile creation rule is consolidated into the file-scoped suspicious
creation rule: the two APIs alone do not prove unauthorized access.

The Eldergrovepro archive fixture moves to the suspicious corpus: a temporary-file
gate and administrator creation do not by themselves establish a hostile result.
