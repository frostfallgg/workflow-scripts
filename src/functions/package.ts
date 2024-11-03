import { mkdirSync } from "fs";
import path from "path";
import { isDirectory } from "util/file-utils";

export function createDistDirectory(buildDir: string) {
	mkdirSync(buildDir);
	const outDir = path.join(buildDir, "out");
	mkdirSync(outDir);
}

export function getDistDirectory(workingDir: string, buildDirName: string) {
	const distDir = path.join(workingDir, buildDirName);
	if (!isDirectory(distDir)) {
		//
	}
}
