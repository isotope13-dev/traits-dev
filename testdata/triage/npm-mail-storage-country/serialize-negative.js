const serialized = JSON.stringify(err.error); assert.ok(!serialized.includes(sensitiveRefreshToken));
