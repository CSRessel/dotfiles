import type { Plugin } from "@opencode-ai/plugin"

export const MyPlugin: Plugin = async ({ app, client, $ }) => {
  return {
    // Type-safe hook implementations
    event: async ({ event }) => {
      // Send notification on session completion
      if (event.type === "session.idle") {
        await $`notify-send "OpenCode Completed" "Session is now idle, awaiting user input"`
      }
    }
  }
}
