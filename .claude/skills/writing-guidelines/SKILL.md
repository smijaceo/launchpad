---
name: writing-guidelines
description: Review docs/prose for Vercel Writing Guidelines compliance. Use when asked to "review my docs", "check writing style", "audit prose", "review copy voice and tone", or before committing any page under ventures/*/copy/.
metadata:
  author: vercel (adapted for launchpad)
  version: "1.0.0"
  argument-hint: <file-or-pattern>
---

# Writing Guidelines

Review files for compliance with Vercel's Writing Guidelines.

The upstream skill fetches the rules from the network each time. launchpad pins a snapshot instead, so reviews are repeatable: read [references/command.md](references/command.md) (vercel-labs/writing-guidelines commit 83e2316b034c, MIT, see LICENSE). To update, re-copy `command.md` from that repo and record the new commit here.

## launchpad precedence

These rules apply to prose. Where they conflict with `web-design-guidelines` (which asks for Title Case headings), **page headings H1 to H6 use sentence case** and **buttons and nav labels use Title Case**. Rules about code samples, TypeScript, model strings and Vercel docs navigation don't apply to marketing copy. The project's truthful-marketing guardrails in CLAUDE.md always win.

## Usage

1. Read references/command.md
2. Read the specified files
3. Apply all rules
4. Output findings in the terse `file:line` format the rules describe
