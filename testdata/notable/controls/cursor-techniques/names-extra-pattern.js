const inventory = Object.keys(process.env).filter(name => /^APP_(?:KEY|SECRET|TOKEN)|PASSWORD|AWS/i.test(name));
