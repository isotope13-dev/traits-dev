const inventory = Object.keys(process.env).filter(function (candidate) { return /PASSWORD|AUTH|KEY/i.test(candidate); });
