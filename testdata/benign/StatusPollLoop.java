// Benign status poll: waits for a background export to report COMPLETED.
// No model endpoint, no UI automation: a plain while loop plus a completion
// word must not read as a model-directed feedback loop.
final class StatusPollLoop {
    String waitForExport(ExportJob job) throws Exception {
        String status = job.status();
        while (!"COMPLETED".equals(status)) {
            Thread.sleep(500);
            status = job.status();
        }
        return status;
    }

    interface ExportJob {
        String status();
    }
}
