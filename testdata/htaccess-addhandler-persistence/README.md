htaccess AddHandler persistence drop
====================================

`htaccess-addhandler-persistence` convicts a PHP file that writes an
.htaccess mapping a data suffix (.cache/.dat/.log) to the PHP handler:
server-config persistence turning an inert data drop into an executable
webshell, the AddHandler twin of the user.ini prepend drop. The write must
sit within 2048 bytes of the directive so documentation that merely
mentions AddHandler, plain rewrite-rule drops, and far-apart coincidences
do not convict.

Run `python3 testdata/htaccess-addhandler-persistence/verify.py
<scratch-directory>`. The persistence-drop positive must report the
hostile; the rewrite-only, docs-only, and far-apart negatives must not.
