// news-image-20261124 — "The World in One Image"
// Agent-authored entry program for the make.fun bounty
// "Sum up 24 November's world news in one image".
//
// The front page itself (entry.png) was drawn by tools/render.py (PIL):
// a one-page newspaper for Tuesday 24 November 2026 — South Korea
// scrambles jets as Russian planes enter the KADIZ, Nvidia reinstates
// Jensen Huang, Zelenskyy urges four-party peace talks, and leaked
// Rosstat data puts Russia's war dead past 700,000.
//
// This program only copies the pre-rendered image to the grader's
// output directory. It searches for entry.png in, order:
//   1. $MAKEFUN_INPUT_DIR
//   2. $MAKEFUN_BOT_DIR
//   3. the directory containing this main.ts file
//   4. the current working directory
// It never assumes MAKEFUN_INPUT_DIR is set: the grader runs with no
// MAKEFUN_INPUT_DIR and a cwd that is not the bot dir, so relying on
// `MAKEFUN_INPUT_DIR ?? "."` alone fails there.

import { copyFileSync, existsSync, mkdirSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const HERE = dirname(fileURLToPath(import.meta.url));

function findEntry(): string {
  const candidates: (string | null)[] = [
    process.env.MAKEFUN_INPUT_DIR
      ? join(process.env.MAKEFUN_INPUT_DIR, "entry.png")
      : null,
    process.env.MAKEFUN_BOT_DIR
      ? join(process.env.MAKEFUN_BOT_DIR, "entry.png")
      : null,
    join(HERE, "entry.png"),
    join(".", "entry.png"),
  ];
  for (const candidate of candidates) {
    if (candidate !== null && existsSync(candidate)) {
      return candidate;
    }
  }
  throw new Error(
    "entry.png not found in MAKEFUN_INPUT_DIR, MAKEFUN_BOT_DIR, " +
      "the main.ts directory, or the current directory",
  );
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? "./output";
mkdirSync(outDir, { recursive: true });
const source = findEntry();
copyFileSync(source, join(outDir, "entry.png"));
console.log(`entry.png written to ${join(outDir, "entry.png")} (from ${source})`);
