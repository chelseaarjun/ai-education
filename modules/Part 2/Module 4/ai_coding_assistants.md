# AI Coding Assistants: Features, Key Files, and Best Practices

This guide highlights some of the features, configuration files, commands, and actionable tips for the leading AI coding assistants: **Claude Code**, **GitHub Copilot**, **Cursor**, **Amazon Q Developer**, and **Cline**. This is just a reference—the space is evolving rapidly, so always consult the official documentation of these assistants for the most up-to-date information.

---

## Claude Code

**Key Features & Files**
- **`CLAUDE.md`**
  - Special file (in repo root, subfolders, or `~/.claude/CLAUDE.md`) automatically pulled into context.
  - Use for: code style, commands, workflow, testing instructions, project quirks, etc.
  - [Best Practices & Examples](https://www.anthropic.com/engineering/claude-code-best-practices)
- **Custom Slash Commands**
  - Store prompt templates in `.claude/commands/` (e.g., `.claude/commands/fix-github-issue.md`).
  - Use `/` in Claude to access these as reusable workflows.
- **Safe YOLO Mode**
  - Lets Claude run commands with fewer permission prompts (configure via allowlist or CLI flags).
- **Headless Mode**
  - Run Claude non-interactively for CI, automation, or scripting (`claude -p "prompt"`).
- **Tool Allowlist**
  - Control which tools Claude can use via `/allowed-tools`, settings files, or CLI flags.
- **MCP Integration**
  - Use `.mcp.json` for project-wide tool/server access.

**Tips & Best Practices**
- Use `/clear` to reset context between tasks.
- Use checklists and scratchpads (Markdown files or GitHub issues) for complex, multi-step workflows.
- Pipe data into Claude (`cat file.txt | claude`) for logs, CSVs, etc.
- Use multiple Claude sessions or worktrees for parallel tasks and code review.
- Regularly tune and iterate on your `CLAUDE.md` for best results.
- [Full best practices](https://www.anthropic.com/engineering/claude-code-best-practices)

---

## GitHub Copilot

**Key Features & Files**
- **`.github/copilot-instructions.md`**
  - Project-level custom instructions for Copilot Chat and coding agent.
  - Use for: coding standards, preferred tools, project context, style guides.
  - [How to use](https://docs.github.com/en/copilot/customizing-copilot/adding-repository-custom-instructions-for-github-copilot)
- **Prompt Files**
  - Store reusable prompt instructions in `.github/prompts/` (public preview).
  - Attach in Copilot Chat for context-rich, repeatable workflows.
- **Copilot Chat**
  - Conversational AI for code explanations, debugging, and learning APIs.
- **Copilot CLI**
  - Shell command suggestions and explanations.
- **Pull Request Support**
  - Suggests PR descriptions, code reviews, and explanations.

**Tips & Best Practices**
- Reference files and style guides in `.github/copilot-instructions.md` for consistent output.
- Use prompt files for complex, repeatable instructions.
- Use Copilot Chat for debugging, code explanations, and learning new APIs.
- Always review and edit generated code—Copilot can make mistakes or hallucinate APIs.
- Use Copilot CLI for shell productivity and automation.
- Leverage test generation for quick scaffolding, but validate coverage and correctness.
- Keep your codebase clean and well-documented—Copilot leverages comments and docstrings.

---

## Cursor

**Key Features & Files**
- **`.cursorrules.md`**
  - Project-level rules for coding standards and workflow.
- **Slash Commands**
  - `/explain`, `/test`, etc., for quick actions.
- **MCP Integration**
  - Connect to external data, live docs, and more.
- **Project Templates**
  - Start new projects with AI-powered templates.

**Tips & Best Practices**
- Use `@cursorrules` for project standards.
- Reference files/functions in chat for precise help.
- Use MCP for live data/external context.
- Try `/` commands for quick actions.
- Use project templates for fast setup.

---

## Amazon Q Developer

**Key Features & Files**
- **AWS Context**
  - Deep integration with AWS services and resources.
- **Security Analysis**
  - Automated code security and compliance checks.
- **Infrastructure as Code**
  - Generate and explain CloudFormation, CDK, and Terraform templates.
- **CLI Integration**
  - Amazon Q CLI for command-line productivity and automation.
- **No project-level config file**
  - Context is managed via AWS project settings and credentials.

**Tips & Best Practices**
- Use Q for generating and explaining AWS infrastructure code.
- Leverage security analysis for compliance and best practices.
- Use the CLI for automating repetitive AWS tasks.
- Provide clear AWS context (region, service, resource names) for best results.
- Always review generated infrastructure code for security and cost implications.

---

## Cline

**Key Features & Files**
- **`.clinerules/` directory**
  - Place Markdown files with coding standards, documentation requirements, and workflow rules here. All files in this directory are combined into a unified set of rules for the project.
  - [Cline Rules Guide](https://docs.cline.bot/features/cline-rules)
- **`.clineignore`**
  - Exclude files and folders from Cline's context (like `.gitignore`).
  - [Prompt Engineering Guide](https://docs.cline.bot/prompting/prompt-engineering-guide)
- **Custom Slash Commands**
  - Store prompt templates and workflows in `.clinerules/` or use slash commands in chat for quick actions.
- **Plan & Act**
  - Structured, multi-step planning and execution for complex tasks.
  - [Plan & Act](https://docs.cline.bot/features/plan-and-act)
- **@ Mentions**
  - Reference files, folders, or people in prompts for precise context.
  - [@ Mentions](https://docs.cline.bot/features/at-mentions/overview)
- **Workflows**
  - Automate multi-step coding or project tasks with slash commands and workflows.
  - [Workflows](https://docs.cline.bot/features/slash-commands/workflows)
- **MCP Servers**
  - Integrate with external databases, live docs, and more via MCP protocol. Configure with `.mcp.json`.
  - [MCP Overview](https://docs.cline.bot/features/mcp-servers/overview)
- **Memory Bank**
  - Persistent memory for context and project knowledge.
  - [Memory Bank](https://docs.cline.bot/prompting/prompt-engineering-guide#cline-memory-bank)
- **Drag & Drop**
  - Drag files into chat for context or analysis.
- **Checkpoints**
  - Save and restore project states during development.
- **Auto Approve**
  - Automatically approve certain actions for faster workflows.

**Tips & Best Practices**
- Use @-mentions for precise context in prompts.
- Store standards and rules in `.clinerules/` for team-wide consistency.
- Use Plan & Act for breaking down and executing complex tasks.
- Integrate MCP for external data and live documentation.
- Use drag & drop for quick context sharing.
- Try checkpoints for safe experimentation and easy rollback.
- Regularly update `.clineignore` to keep context relevant and secure.
- [Prompt Engineering Guide](https://docs.cline.bot/prompting/prompt-engineering-guide) for advanced tips.

---

## General Tips for All AI Coding Assistants

- **Give URLs to fetch**: Many assistants can fetch and analyze content from URLs.
- **Give images**: Some can analyze images if provided.
- **Mention/reference files in prompts**: Use file names, or copy and paste code or docs into your prompt for best results.
- **Clear context/start over**: Use commands like `/clear` or start a new chat to reset the assistant's context.
- **Use checklists and scratchpads**: For complex workflows, have the assistant use a Markdown file or issue as a checklist and working scratchpad.
- **Break down large tasks**: Divide complex requests into smaller, focused prompts for better results.
- **Iterate and refine**: Review, test, and refine the assistant's output—don't expect perfection on the first try. 