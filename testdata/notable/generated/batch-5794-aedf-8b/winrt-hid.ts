export async function write(device: any, report: any) {
    return device.sendOutputReportAsync(report);
}
