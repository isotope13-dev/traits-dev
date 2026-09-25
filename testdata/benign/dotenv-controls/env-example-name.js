// Project-health helper: `.env.example` is generic dotenv vocabulary,
// not a marker of any particular application stack.
const INSPECTABLE = new Set(['Gemfile', 'Procfile', '.env', '.env.example']);

function isInspectable(name) {
  return /\.(js|json|md|env)$/i.test(name) || INSPECTABLE.has(name);
}

module.exports = { isInspectable };
