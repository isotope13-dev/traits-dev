function getClass() {
  return project.addSourceFileAtPath(FILE).getFirstDescendantByKind(SyntaxKind.ClassDeclaration);
}
function body(name) {
  const cls = getClass();
  return cls.getMethod(name);
}
