load_git()).default.npmUrlToGitUrl(url);
      const client = new (_git || _load_git()).default(_this.config, gitUrl, _this.hash);

      let out = yield _this.config.requestManager.request({
        url: `${url}/info/refs?service=git-upload-pack`,
        queue: _this.resolver.fetchingQueue
      });

      if (out) {
        // clean up output
        let lines = out.trim().split('\n');

        // remove first two lines which contains compatibility info etc
        lines = lines.slice(2);

        // remove last line which contains the terminator "0000"
        lines.pop();

        // remove line lengths from start of each line
        lines = lines.map(function (line) {
          return line.slice(4);
        });

        out = lines.join('\n');
      } else {
        throw new Error(_this.reporter.lang('hostedGitResolveError'));
      }

      return client.setRefHosted(out);
    })();
  }

  resolveOverHTTP(url) {
    var _this2 = this;

    return (0, (_asyncToGenerator2 || _load_asyncToGenerator()).default)(function* () {
      const commit = yield _this2.getRefOverHTTP(url);
      const config = _this2.config;


      const tarballUrl = _this2.constructor.getTarballUrl(_this2.exploded, commit);

      const tryRegistry = (() => {
        var _ref = (0, (_asyncToGenerator2 || _load_asyncToGenerator()).default)(function* (registry) {
          const filename = (_index |