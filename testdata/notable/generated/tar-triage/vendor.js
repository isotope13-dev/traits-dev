/* Separate vendor modules: locale data, HTTP client, global-object helper. */
(globalThis.webpackChunk = globalThis.webpackChunk || []).push([[1], {
  1: function () { moment.defineLocale("en", {months: ["January"]}); },
  2: function () { return new XMLHttpRequest(); },
  3: function () { return Function("return this")(); }
}]);
