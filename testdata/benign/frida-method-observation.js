// Developer instrumentation: log a path query and preserve its result.
Java.perform(function () {
    const File = Java.use('java.io.File');
    File.getPath.implementation = function () {
        console.log('File.getPath queried');
        return this.getPath();
    };
});
