export function inspect(element) {
  const key = Object.keys(element).find(k => k.startsWith("__reactFiber$"));
  const fiber = element[key];
  return {props: fiber.memoizedProps, state: fiber.memoizedState};
}
