import * as arbitraryAlias from 'node:module';
arbitraryAlias.register('./custom-loader.mjs', import.meta.url);
