const findings = [];
findings.push({ruleId: "AIRA010", category: "prompt_injection", severity: "high", message: "Hidden content block may conceal instructions from human reviewer", suggestion: "Comments addressed to AI assistants that contain override are an attack vector. Remove or rewrite."});
