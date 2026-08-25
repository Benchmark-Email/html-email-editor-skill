---
name: benchmark-html-email
description: Write production-ready HTML email that can be pasted straight into the HTML editor in Benchmark Email. Use whenever someone asks to build, write, generate, fix, or convert an HTML email, email template, newsletter, or campaign for Benchmark Email, or mentions pasting HTML into Benchmark, the Custom HTML editor, or sending a designer's or AI-generated HTML through Benchmark. Also use when reviewing existing email HTML for inbox compatibility before sending it with Benchmark.
license: Provided by Benchmark Email for use with a Benchmark Email account.
---

# Benchmark HTML Email

Build one complete, self-contained HTML document that a Benchmark Email customer can paste
into the Custom HTML editor and send without editing the code.

## Work in this order

**1. Read. 2. Ask only if still stuck. 3. Build. 4. Review. 5. Hand over.**

The order matters more than any single rule here. Asking before reading is the most common way
this goes wrong: the answers are usually on the pages already, and a question the customer
should not have been asked costs their patience and your credibility.

## Step 1 — read everything first

**Read everything they linked, not just the homepage.** Fetch the brand's site for colors, the
logo's hosted image URL, tone of voice, and what the business does. Then fetch every other URL
in the brief and write from what is actually on those pages. If they linked a product update,
name the things in it. If they linked a blog, reference real posts. An email that says
"explore the latest improvements" is what you get when nobody opened the page.

Pulling colors from the site beats asking for hex codes, which most marketers do not know. If
you cannot fetch pages, say so in one line and ask for the colors, a logo link, and the details
you would have read.

## Step 2 — ask only if you are still stuck

Reading answers most of it. **Ask nothing you could have answered by reading.** After reading,
ask only about what the pages could not settle and that you would otherwise have to invent.

In practice that is usually one thing: which of several links or topics should lead. Often it is
nothing, and you should go straight to building.

A brief can contain every required field and still leave you inventing. "Include the release
notes, a link to the blog, or any other email marketing topics" is a menu, not a decision. Two
links with no stated priority is not a decision either. That is worth one question.

When you do ask: up to four short questions in one message, each with your best answer offered
as a default so they can reply "go" and be done. Return no HTML in that message. Ask about what
they want, not how it gets built. "Which of these should be the main thing someone clicks?"
rather than "what is the CTA URL."

Never ask before you have finished reading. Never ask, start work, hit a second problem, and
come back — that turns a two-minute task into a five-round interrogation. One round trip at
most.

**Never invent** a URL, price, date, statistic, or claim about the business.

## Step 3 — writing the copy

The technical rules below produce email that renders. They do not produce email anyone wants
to read. Generic copy is the most common failure in AI-written email, and it comes from
writing about a linked page instead of from it.

- Lead with the most specific, useful thing you have. Never open with a general statement about
  the category. "Whether you are planning your next campaign, growing your list, or checking
  what is working" is the sentence to delete, not write.
- Name real things. "Three new things in the July update: scheduled reports, faster list
  imports, and a rebuilt segment builder" beats "explore the latest improvements."
- Cut any sentence that would be equally true in a competitor's email. If it survives a
  find-and-replace of the company name, it is not doing any work.
- Avoid the hedging triad ("whether you are doing A, B, or C"). Pick the one that matters.
- Short sentences, one idea each. Write like a person telling someone something useful.
- One primary action, one button. A second action goes in as a plain text link so the hierarchy
  is obvious. Two equally weighted buttons make the reader choose, and most choose neither.
- Do not pad to fill a layout. A short email that says something specific beats a long one that
  does not.
- Vary the sections structurally. Three identical heading-paragraph-button blocks read as a
  template even when the words are fine.
- Match the tone they asked for. If they did not name one, match the tone of the site you read.

## Step 4 — review your own work before showing it

Before you hand over the HTML, reread it as a picky email developer paid to find everything
wrong with it. Work this list literally and fix what you find. Do not narrate the step.

1. **Light text.** Every light `color:` value has a `background-color` on the *same* tag, not
   only on a parent. Otherwise make the text dark.
2. **Images.** Every `src` is a URL you actually loaded. No `.svg`, no `.webp`. Every `img` has
   `alt`, `width`, and `display:block`.
3. **Footer.** Search for "unsubscribe", "manage preferences", "opt out", "report abuse",
   "view in browser", and any street address or postal code. There must be none.
4. **Sanitizer.** No `<script>`, `<form>`, `<iframe>`, `<embed>`, `<object>`, no `on*` attribute.
5. **Merge tags.** No `{{...}}`, `*|...|*`, `%%...%%`. Placeholders are plain uppercase, with
   the fallback in an HTML comment.
6. **Layout.** Every table has `role="presentation" cellpadding="0" cellspacing="0" border="0"`.
   No flex, grid, float, position. Container at 600px via both attribute and `max-width`.
7. **Type.** Nothing under 14px. Every text-bearing `<td>` carries its own `font-family`. Web
   fonts have a web-safe fallback right behind them.
8. **Structure.** `<!DOCTYPE html>` to `</html>`, every tag closed, nothing after the sign-off.
9. **Images off.** Reread it with every image failing to load. It must still make sense and the
   call to action must still be visible.
10. **Copy.** Any sentence equally true in a competitor's email gets deleted or made specific.

If you changed anything, run the list again. `references/validate-email-html.py` in this skill
checks most of the same things mechanically — run it when you have a shell.

## Step 5 — handing it over

**Prefer handing over a file.** When file tools are available, always write the HTML to a
`.html` file and give the person that file. Benchmark's editor has an "Upload HTML File" path,
so they drag the file in and never copy or paste anything. Every artifact problem below —
citation markers, status labels, stray code fences, a swallowed doctype — only exists on the
copy-paste route. Handing over a file removes the whole class.

Say so when you do it: "Download this and use Upload HTML File in Benchmark rather than
pasting."

**Falling back to the chat.** When file tools are unavailable, return the email as one complete
document from `<!DOCTYPE html>` through `</html>`, in a single fenced code block. Never put the
HTML in a canvas, document, or side panel — copying out of those brings the fence characters
along, and they render as visible text in the email.

Tell them once: copy with the button at the top of the code block, not the "Copy response"
button at the bottom of the message. That second one takes the whole reply, status labels and
citations included.

**Follow up in a second, separate message** with a suggested subject line (up to 80 characters)
and suggested preview text (**50 characters or less**, adding something the subject does not
already say). Both limits are Benchmark's. Note that preview text is the *shorter* of the two here,
which inverts the usual advice — keep it tight rather than padding toward a subject-length line. Both are entered on Benchmark's checklist after the design, so they must never appear
inside the HTML — but suggesting them saves the person writing two more things from scratch. Add
one line there if you swapped a logo for styled text.

**Either way, nothing else in the message carrying the code:** no commentary, and no citations,
source links, reference markers, or footnotes. If you researched pages to write the copy, keep the sources
out of the message carrying the code. A citation marker pasted into the editor renders as
visible junk in the subscriber's inbox — it has happened in testing, and the customer has no
way to know what it is. Explanations and source lists go in a separate message afterwards.

## Benchmark's constraints

These come from how Benchmark stores and sends the HTML. They are not style preferences.

| Constraint | What it means for the code |
|---|---|
| No CSS auto-inlining | Every style that affects layout must be inline on the element |
| Sanitized on save | No `<script>`, `<form>`, `<iframe>`, `<embed>`, `<object>`, or on* event handlers |
| 500 KB maximum | Keep it lean; do not embed large base64 images |
| No image hosting | Every `src` must be a public https:// URL |
| Footer always added | Never write an unsubscribe link, preference link, or mailing address |
| Link tracking rewrites hrefs | Plain complete https:// URLs only; no tracking pixels, no `#` anchors |
| Preview is 600px / 375px | Build the container at 600px and check the mobile stack at 375px |

`<style>` blocks in `<head>` survive and are the right home for `@media` queries. Treat them
as progressive enhancement only: the email must still look correct with the whole block
deleted.

Full detail, including why each rule exists: `references/benchmark-constraints.md`.

## Build pattern

Follow the shell in `assets/starter-template.html`. It is a working 600px single-column
email with a header, hero image, body, bulletproof button, and sign-off, with the Outlook
conditionals already in place. Adapt it rather than starting from a blank file.

The rules the template encodes:

- Layout with `<table role="presentation" cellpadding="0" cellspacing="0" border="0">` only.
  No div, flexbox, grid, float, or position for structure.
- 600px centered container, fluid via `width:100%; max-width:600px`, with explicit `width`
  attributes alongside the CSS.
- Padding on `<td>`, never on `<p>` or `<div>`. Outlook drops most div and margin CSS.
- Buttons are `<td>`-based: background color on the `<td>` as both `bgcolor` and inline CSS,
  then repeated as `background-color` on the `<a>` itself, padded, in contrasting text,
  MSO conditional spacers (`<!--[if mso]>&nbsp;&nbsp;<![endif]-->`) either side of the link for
  Outlook padding. Never nest a second `<a>` inside an MSO conditional around an existing one.
  Never an image-only button.
- Images are **PNG, JPG, or GIF only. Never SVG or WebP** — Gmail and Outlook render neither,
  so the reader sees a broken image or nothing. Check the extension of everything pulled from a
  site, at the time you read the site. See "When the logo is an SVG" below.
  Every image carries alt text, an explicit `width`, and
  `style="display:block; border:0; height:auto"`. The email must read completely with images
  off, so keep essential copy out of images and put background colors behind image areas.
- Web-safe font stacks only. A brand web font goes first with a web-safe fallback right
  behind it, because Gmail and Outlook will not load it.
- Body copy at 14px minimum, 16px preferred, as real selectable text.
- Explicit background colors on `<body>` and the outer wrapper table.
- **Dark text on light backgrounds by default.** Any light-colored text must carry its own
  inline `background-color` on the same tag. See "Light text" below — the rule that keeps whole
  sections from rendering blank.

More patterns, including two-column stacking, VML background images, and dark-mode handling:
`references/email-html-patterns.md`.

## Light text, and why sections go invisible

The most destructive failure in email, because it is invisible in every browser preview.

Background painting is the least reliable part of email rendering, Outlook most of all. If a
band drops out, the light text inside lands on white and the entire section renders as blank
space — headline, body copy, all of it. A preview pane cannot warn you, because it renders the
background correctly.

**Default to dark text on light backgrounds for the whole email.** Do not build full-width
reversed sections. Get emphasis from type scale, weight, spacing, thin rules, and small
accent-colored labels. A well-set light-background email reads better anyway.

If a design genuinely needs light text, the rule is:

> Any element with light-colored text must carry its own `background-color`, inline, on the
> very same tag. A background on the surrounding `<td>` is not enough to rely on.

Buttons therefore declare the color three times — `bgcolor` and `background-color` on the
`<td>`, then `background-color` again on the `<a>` beside the light text color. That third
declaration is what keeps the label readable, and it is why buttons survive when headline
bands do not.

`validate-email-html.py` enforces exactly this and names the offending color.

## When the logo is an SVG

Common, and it must not cost the customer four messages. Work in this order:

1. **Look for a real file, and confirm it loads.** Check the favicon, the `og:image` meta tag,
   and any press or brand page. Only use a URL you actually retrieved successfully. Never
   construct one by pattern or swap an extension and hope — a guessed URL that 404s renders as
   a broken-image icon in every inbox, which is worse than having no logo.
2. **If nothing turns up, do not stall the email.** Fold the question into your single batch of
   questions with this default offered: set the company name as styled text in the header.
   A text header is a legitimate design, it survives blocked images, and it never breaks.
3. **Be tolerant of what comes back.** People send an uploaded file instead of a URL, or a URL
   with the domain clipped off. Say what is missing once, in one line, and re-offer the
   text-header default in the same message. Never ask twice for the same thing.

## Personalization

Do not write Benchmark merge tags. They are unique to each account: `{key}` for the email
address and `{cf_...}` for every other field, where the string after `cf_` differs from one
account to the next. There is no syntax you can derive, and a wrong tag renders as literal
text in the inbox.

Instead, leave a plain uppercase placeholder as visible text where the value belongs, and put
the intended fallback in an HTML comment beside it. The fallback must never appear in the
visible copy, or it ships to the inbox as literal text:

```html
<p style="...">Hi FIRST_NAME_HERE,<!-- fallback: there --></p>
```

Then tell the person to replace each placeholder inside Benchmark, using either:

- the **Personalize** button in the editor, which inserts the correct token for their account
  and lets them set the fallback value, or
- the exact tag listed against that field under **Settings > Contact Fields**, which is where
  every account's own tags are published.

## What never goes in the HTML

- A footer, unsubscribe link, preference-center link, or physical mailing address. Benchmark
  adds all of these to every send automatically, and they cannot be styled or skipped, so
  writing your own produces two footers.
- The subject line, and preview text in any form. Both are entered on Benchmark's email
  checklist after the design is finished, so do not build a hidden preheader block.
- Anything legal or administrative after the sign-off.

## Reviewing HTML someone else wrote

When asked to fix or check existing email HTML, work through
`references/troubleshooting.md`. Report what changed and why, then return the corrected
document. Never silently rewrite the design; if a fix changes how the email looks, say so.

## Handing it back

After the HTML, give these steps once, in plain language:

1. In Benchmark Email, start a new email and choose **Custom HTML**, then **Start from
   Scratch** to paste or **Upload HTML File** to upload.
2. Check the live preview in both Desktop and Mobile views.
3. Replace each placeholder with the **Personalize** button, or with the tag for that field
   from **Settings > Contact Fields**.
4. Send a test and open it in a real inbox.
5. Run the checklist: subject line, preview text, from address, list, schedule or send.

The unsubscribe link and mailing address are added automatically.
