const loader = { require: function (modules) { this.modules = modules; } };
loader.require(options.modules);
loader.require(resolveName());
this.require(options["require"]);
Scriptaculous.require(path + "effects.js");
