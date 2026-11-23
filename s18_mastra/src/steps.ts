// Watch the agent loop: how many steps it takes, and what happens with a step limit.
import "dotenv/config";
import { Agent } from "@mastra/core/agent";
import { createTool } from "@mastra/core/tools";
import { z } from "zod";
import { stockRows } from "./stock.js";

const checkStock = createTool({
  id: "check-stock",
  description: "Check how many of one product Sara has in stock, and its reorder level.",
  inputSchema: z.object({ item: z.string() }),
  execute: async ({ item }) => stockRows().find((r) => r.item.toLowerCase() === item.toLowerCase()) ?? { error: "not found" },
});

const agent = new Agent({
  id: "shop-helper",
  name: "Shop helper",
  instructions: "You help customers of Sara's shop. Use check-stock. Keep replies short.",
  model: "openai/gpt-5.4-mini",
  tools: { checkStock },
});

const question = "Do you have the ceramic vase?";
for (const maxSteps of [5, 1]) {
  const result = await agent.generate(question, { maxSteps });
  console.log(`maxSteps ${maxSteps}: took ${result.steps.length} step(s), answer: ${JSON.stringify(result.text)}`);
}
