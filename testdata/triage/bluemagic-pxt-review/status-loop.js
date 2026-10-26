for (let pending = queue.shift(); pending; pending = queue.shift()) {
    processItem(pending);
}
