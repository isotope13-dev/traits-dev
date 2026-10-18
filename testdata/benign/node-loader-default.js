import moduleApi from 'node:module';
moduleApi.registerHooks({ resolve(specifier, context, next) { return next(specifier, context); } });
