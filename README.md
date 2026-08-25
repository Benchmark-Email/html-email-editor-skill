# Benchmark HTML Email skill

A Claude skill that writes production-ready HTML email you can send straight from the HTML editor
in [Benchmark Email](https://www.benchmarkemail.com). Describe the email in plain language and get
back a complete, inbox-tested HTML file. No coding required.

Built by Benchmark Email. Free to use with a Benchmark Email account.

## Install

Pick one. They install the same skill.

**Claude app** — download
**[benchmark-html-email.skill](https://github.com/Benchmark-Email/html-email-editor-skill/releases/latest/download/benchmark-html-email.skill)**
from the latest release, then upload it in Settings. One file, nothing to unpack.

**Claude Code** — clone this repository into your skills directory and restart:

```bash
git clone https://github.com/Benchmark-Email/html-email-editor-skill.git ~/.claude/skills/benchmark-html-email
```

The files in this repository *are* the skill, so you can read every rule before installing
anything. The release is the same files packaged into a single `.skill` for the app, which cannot
install from a folder.

## Use it

Just ask, in plain language:

> Build an HTML email for our September newsletter, based on this post: [link]

It reads your website for brand colours, logo, and tone, reads whatever else you linked, asks only
what it genuinely cannot work out, then writes the email and checks its own work before showing it
to you. You get a `.html` file to upload, plus a suggested subject line and preview text.

## What it knows that a general assistant does not

Email HTML is not web HTML, and Benchmark has its own constraints on top of that. This skill
encodes both, so the output does not quietly break in the inbox:

- **Tables, not divs.** Inline styles only — there is no CSS inliner, so anything the layout
  depends on has to be on the element.
- **The sanitizer.** `<script>`, `<form>`, `<iframe>`, `<embed>`, `<object>`, and `on*` handlers
  are stripped on save. It never writes them.
- **No SVG or WebP.** Gmail and Outlook render neither. It checks the file extension of every
  image it pulls from your site, and falls back to a styled text header rather than shipping a
  broken logo.
- **The compliance footer is automatic.** It never writes an unsubscribe link or mailing address,
  because Benchmark adds them to every send and two footers is one too many.
- **Merge tags are per-account.** It leaves a plain `FIRST_NAME_HERE` placeholder for you to swap
  with the Personalize button, rather than guessing a tag that would render as literal text.
- **Light text on dark bands.** The most destructive email bug there is, because it looks perfect
  in every preview. It defaults to dark-on-light and defends the exception.

## It checks its own work

`references/validate-email-html.py` is a 60-plus point checker for email HTML. When Claude has a
shell it runs this against its own output before handing anything over, and fixes what fails.

You can run it yourself on any email HTML, from this skill or not:

```bash
python3 references/validate-email-html.py your-email.html
```

It catches things a browser preview cannot show you: an SVG logo, light text that will render
invisible, a citation marker pasted in from a chat window, a cell that will fall back to Times New
Roman in Outlook.

## What is in here

| Path | What it is |
|---|---|
| `SKILL.md` | The skill itself — the rules Claude follows |
| `references/benchmark-constraints.md` | Why each platform rule exists |
| `references/email-html-patterns.md` | Two-column stacking, VML backgrounds, dark mode |
| `references/troubleshooting.md` | Repairing HTML from another platform |
| `references/validate-email-html.py` | The checker |
| `assets/starter-template.html` | A working 600px shell to adapt |

## Feedback

Tell us what broke: [allie@benchmarkemail.com](mailto:allie@benchmarkemail.com?subject=HTML%20Email%20skill%20feedback).
Paste the email it gave you if you still have it — that is the most useful thing you can send.

## Licence

Provided by Benchmark Email for use with a Benchmark Email account. See [LICENSE](LICENSE).
