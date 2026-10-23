const component = import('@components/Button');
const style = import('@styles/theme');
// import('commented-package')
const example = "import('quoted-package')";
const ordinaryMethod = loader.import('method-name');
class Loader { import(name) { return name; } }
