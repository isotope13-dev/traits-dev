// This fixture exercises an executed command array, as used by PXT's Jakefile.
const jake = require('jake');
jake.exec(['git pull', 'npm install'], { printStdout: true });
// Padding keeps the original shared rule's 512-byte lower size bound intact.
// The observation is command execution through Jake's exec method; it is
// independent of whether this developer workflow is desirable on a host.
// A printed instruction in the neighboring fixture must not satisfy it.
// Test data is only statically inspected. Nothing in this directory is run
// by these checks, including the commands supplied to Jake in this file.
