// The restock plan again, now typed with a Zod schema (TypeScript's answer to Pydantic).
import "dotenv/config";
import { Agent } from "@mastra/core/agent";
import { createTool } from "@mastra/core/tools";
import { z } from "zod";
import { stockRows } from "./stock.js";

const listStock = createTool({
  id: "list-stock",
  description: "List every product with how many are in stock and its reorder level.",
  inputSchema: z.object({}),
  execute: async () => stockRows(),
});

const RestockPlan = z.object({
  reorders: z.array(z.object({
    item: z.string(),
    inStock: z.number(),
    orderQty: z.number().describe("How many to order to get back to twice the reorder level"),
  })),
  note: z.string().describe("One short sentence for Sara"),
});

const agent = new Agent({
  id: "restock-planner",
  name: "Restock planner",
  instructions: "You plan Sara's restocking. Reorder anything at or below its reorder level.",
  model: "openai/gpt-5.4-mini",
  tools: { listStock },
});

const result = await agent.generate("Make this week's restock plan.", { structuredOutput: { schema: RestockPlan } });
const plan = result.object; // typed: TypeScript knows plan.reorders[0].orderQty is a number
for (const r of plan.reorders) console.log(`${r.item.padEnd(16)} in stock ${String(r.inStock).padStart(2)}  ->  order ${r.orderQty}`);
console.log("Note:", plan.note);
