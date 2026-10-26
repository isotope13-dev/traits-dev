/* Minimal ls display filter in the shape of busybox coreutils/ls.c:
   hide_file() suppresses dotfiles and hidden-attribute entries from ls's
   own output unless -a/-A is given. Display filtering, not hiding. */
static int hide_file(unsigned attr)
{
	return ((attr & 0x2) && !(opts & (OPT_a | OPT_A)));
}
