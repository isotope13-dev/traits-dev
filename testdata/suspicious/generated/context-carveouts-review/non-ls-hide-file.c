static int hide_file(const char *path)
{
	return unlink(path);
}
