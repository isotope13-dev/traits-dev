// Benign control for request-write-content-file-variable: Nx Devkit
// Tree.write is a virtual-filesystem generator write, never an HTTP client
// write, so the trait must stay silent here.
tree.write(file, finalContents);
