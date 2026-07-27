import { readFile, writeFile } from "node:fs/promises";

const readJson = async (path) => JSON.parse(await readFile(path, "utf8"));
const writeJson = async (path, value) =>
  writeFile(path, `${JSON.stringify(value, null, 2)}\n`);

const packageJson = await readJson("package.json");
const pluginJson = await readJson(".claude-plugin/plugin.json");
const packageLock = await readJson("package-lock.json");

pluginJson.version = packageJson.version;
packageLock.version = packageJson.version;
packageLock.packages[""].version = packageJson.version;

await Promise.all([
  writeJson(".claude-plugin/plugin.json", pluginJson),
  writeJson("package-lock.json", packageLock),
]);
