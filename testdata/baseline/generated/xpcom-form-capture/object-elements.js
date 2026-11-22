var registry = { elements: {} };
function getElements(type) {
  return registry.elements[type] || (registry.elements[type] = {});
}
