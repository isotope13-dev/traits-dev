package api
// The ?task=<task> query parameter must be set.
func pause(task string) string { return "/v1/client/allocation/id/pause?task=" + task }
