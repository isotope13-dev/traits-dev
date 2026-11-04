const names = Object.keys(process.env).filter(entry => /TOKEN|KEY|SECRET/i.test(process.env[entry]));
