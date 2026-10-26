// GitHub's code viewer displays Git instructions rather than running Git.
function renderInstructions() {
    console.log('git clone https://example.invalid/project.git');
    return '<code>git pull</code>';
}
// Padding keeps the original shared rule's 512-byte lower size bound intact.
// The presence of command text in a UI does not establish shell execution.
// A separate fixture supplies the same operation to an actual execution API.
// Test data is only statically inspected. Nothing in this directory is run
// by these checks, including the displayed commands and this render function.
