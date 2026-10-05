// Benign control for hidden-archive-path: dotenv template paths built from
// `.target` task properties. `.target` is property access, not a `.tar`
// archive, so the trait must stay silent here.
const dotenvFiles = [
  `${task.projectRoot}/.env.${task.target.target}.${task.target.configuration}`,
  `${task.projectRoot}/.${task.target.target}.${task.target.configuration}.env`,
];
