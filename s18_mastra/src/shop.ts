// Sara's stock check with Mastra, in TypeScript.
import "dotenv/config";
import { Agent } from "@mastra/core/agent";
import { createTool } from "@mastra/core/tools";
import { z } from "zod";
import { stockRows } from "./stock.js";

const checkStock = createTool({
  id: "check-stock",
  description: "Check how many of one product Sara has in stock, and its reorder level.",
  inputSchema: z.object({ item: z.string().describe('Product name, e.g. "Candle trio"') }),
  execute: async ({ item }) =>
    stockRows().find((r) => r.item.toLowerCase() === item.toLowerCase()) ?? { error: `No product '${item}'.` },
});

const agent = new Agent({
  id: "shop-helper",
  name: "Shop helper",
  instructions: "You help customers of Sara's small home-goods shop. Use check-stock. Keep replies short.",
  model: "openai/gpt-5.4-mini",
  tools: { checkStock },
});

const result = await agent.generate("Do you have the ceramic vase and the candle trio?");
console.log(result.text);
console.log("tool calls:", result.toolCalls.map((c) => `${c.payload.toolName}(${JSON.stringify(c.payload.args)})`).join(", "));
