// Static analysis controls; never execute.
type ModuleType = import('type-package').Module;
type ModuleNamespace = typeof import('type-package');
loadType<typeof import('type-package')>();
const quoted = "import('quoted-package')";
// import('comment-package');
loader.import('member-package');
import('@components/button');
import('@pages/home');
import('@utils/helper');
import('@hooks/state');
import('@constants/config');
import('@apis/client');
import('@styles/theme');
import('@types/model');
