// Mastra worker for Project 8: the same board and the same three tools, in TypeScript.
import "dotenv/config";
import { DatabaseSync } from "node:sqlite";
import { readFileSync, writeFileSync } from "node:fs";
import { Agent } from "@mastra/core/agent";
import { createTool } from "@mastra/core/tools";
import { z } from "zod";

const loop = new URL("../../s18_frameworks/agent_loop/", import.meta.url);
const db = new DatabaseSync(new URL("board.db", loop).pathname);
type Task = { id: number; title: string; file: string; note: string };

const readTask = createTool({
  id: "read_task",
  description: "Get your current task from the shared board, plus the launch brief.",
  inputSchema: z.object({}),
  execute: async () => {
    const t = db.prepare("SELECT * FROM tasks WHERE owner = 'mastra' AND status != 'done' ORDER BY id LIMIT 1").get() as Task | undefined;
    if (!t) return { error: "No task for you." };
    db.prepare("UPDATE tasks SET status = 'working' WHERE id = ?").run(t.id);
    const brief = readFileSync(new URL("../../data/launch_brief.md", import.meta.url), "utf8");
    return { task_id: t.id, title: t.title, file: t.file, note: t.note, brief };
  },
});

const saveFile = createTool({
  id: "save_file",
  description: "Save your finished piece into the shared outbox folder.",
  inputSchema: z.object({ file: z.string(), content: z.string() }),
  execute: async ({ file, content }) => {
    writeFileSync(new URL(`outbox/${file}`, loop), content);
    return `Saved ${file} (${content.split(/\s+/).filter(Boolean).length} words).`;
  },
});

const completeTask = createTool({
  id: "complete_task",
  description: "Mark your task as done on the shared board.",
  inputSchema: z.object({ task_id: z.number() }),
  execute: async ({ task_id }) => {
    db.prepare("UPDATE tasks SET status = 'done', note = '' WHERE id = ?").run(task_id);
    return "Marked done.";
  },
});

const agent = new Agent({
  id: "mastra-worker",
  name: "Mastra worker",
  instructions: "You are a worker on Sara's launch team. First call read_task to get your job and the launch brief. " +
    "Write the piece, then call save_file with the exact file name from the task. Finally call complete_task. Use only facts from the brief. " +
    "If the task has a note, it says what to fix: follow it exactly. " +
    "Respect any word limit in the title; save_file tells you the word count, so check it and save again if needed.",
  model: "openai/gpt-5.4-mini",
  tools: { readTask, saveFile, completeTask },
});

await agent.generate("Do your task on the board.", { maxSteps: 8 });
