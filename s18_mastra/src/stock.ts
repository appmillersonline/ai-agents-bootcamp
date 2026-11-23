// Sara's stock list (sample data), read from the shared course data folder.
import { readFileSync } from "node:fs";

export type StockRow = { item: string; inStock: number; reorderAt: number };

export function stockRows(): StockRow[] {
  const lines = readFileSync(new URL("../../data/inventory.csv", import.meta.url), "utf8").trim().split("\n");
  return lines.slice(1).map((line) => {
    const [item, inStock, reorderAt] = line.split(",");
    return { item, inStock: Number(inStock), reorderAt: Number(reorderAt) };
  });
}
