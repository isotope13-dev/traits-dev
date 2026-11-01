# Signed-bundle reference review

Thirteen standalone observations moved out of legacy signed-bundle staging:
executable and DLL filename references, a registry key reference, a mutex name,
and product-name text. A name appearing in a binary is not proof that the named
product is signed, loaded or used for sideloading. The GrooveMigrator and
pack200 filename observations are notable rather than suspicious on their own.
The existing text conditions, sections and size bounds remain unchanged;
consumers were updated. These are unverified references, rather than established
product ownership suitable for a `well-known/` product identity.

The broad dropper ancestor in the hosts-file rule previously included these
observations. Its alternatives explicitly retain them for compatibility while
that consumer's use of weak historical evidence remains under review. The
remaining signed-bundle composites and the remote-thread wrapper are not yet
migrated.

The adjacent library-path directory held 84 traits. Thirty-four references to
Windows system libraries moved to `micro-behaviors/fs/path/system/library`,
leaving 50 in the original directory. Parsed comparisons verified all 84 rules'
conditions and metadata, with cross-directory references updated. No
whole-directory consumers of the original library path were found.
