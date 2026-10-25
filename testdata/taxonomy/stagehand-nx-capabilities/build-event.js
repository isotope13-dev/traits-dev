// The original Nx executor consumes an async build iterator's result.
async function consume(event) {
  await addToQueue(null, Promise.resolve(event.value));
  return event.value;
}
