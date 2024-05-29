import { testAst } from "./ast.js";
import { deleteLogFile } from "./log.js";

if (require.main == module) {
  deleteLogFile();
  testAst();
}
