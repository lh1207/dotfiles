---
name: save-prompt-cache
description: Compatibility entrypoint for older vault completion instructions. Native prompt caching is managed by Claude Code itself.
---

# Save Prompt Cache compatibility

Invoke the local `obsidian-save` skill and follow its shared vault workflow.
Require its saved-or-skipped receipt in the selected vault before declaring
completion. Do not create a second receipt in a separate cache directory.

This legacy name refers to knowledge persistence. It does not save, synchronize,
or configure provider prompt caches, and a receipt does not prove a cache hit.
