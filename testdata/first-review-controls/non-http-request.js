const fake = {request(options) { return options; }};
fake.request({method:'POST'});
