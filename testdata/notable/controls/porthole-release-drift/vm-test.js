import { runInThisContext } from "node:vm";
describe("registration", () => {
  const register = runInThisContext("(fn, title, body) => fn(title, body)");
});
