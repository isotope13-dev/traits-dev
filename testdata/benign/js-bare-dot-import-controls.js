// A bare `.tld/` specifier is a package name, never a hidden-directory
// reference. Seen in the wild as `.com/` split from an IDN host inside
// swagger-ui sourcemap fixture text; the hidden-dir atoms require a
// leading ./, ../ or / path segment.
import y from ".com/y";
console.log(y);
