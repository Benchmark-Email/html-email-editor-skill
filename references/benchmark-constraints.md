# How Benchmark Email handles your HTML

Every rule below comes from how the platform stores, sanitizes, and sends the code. Ignoring
one does not produce a warning in the chat window; it produces a broken email in someone's
inbox, or code that silently disappears on save.

## Sent exactly as authored

Benchmark does not run a CSS inliner. Whatever is in the HTML is what goes out.

Practical effect: a class-based stylesheet that looks perfect in a browser preview will
collapse in Gmail, which strips much of what lives outside the element. Every style that
affects layout, spacing, color, or type must be written inline on the element itself.

A `<style>` block in `<head>` is preserved and is the correct home for `@media` queries and
client-specific resets. Build so that deleting the entire block leaves a correct, readable
email. Anything in there is a bonus, never the foundation.

## Sanitized on save

When the HTML is saved, Benchmark removes:

- `<script>` tags
- `<form>` tags and form controls
- `<iframe>`, `<embed>`, and `<object>`
- Inline event handlers: `onclick`, `onload`, `onmouseover`, and every other `on*` attribute

It preserves tables, inline styles, `<style>` blocks, background images, and base64-embedded
images.

This matters most for AI-generated HTML, which often adds a hover handler or a small script
without being asked. None of it survives, and none of it works in email clients anyway.

## 500 KB maximum

The stored HTML body caps at 500 KB. Larger submissions are rejected with a plain-language
error rather than truncated.

Typical agency-built campaigns sit well under this. The realistic way to blow past it is
base64-embedding images. Base64 images are technically preserved, but they eat the budget
fast and several clients clip or block them. Host images and link to them.

## Bring your own hosted images

There is no image gallery or media hosting in this editor. Every `src` must be a public
https:// URL that loads without a login: your website's media library, a CDN, or wherever
your images already live.

Externally hosted images render in the preview and pass through unchanged at send.

A file on someone's desktop cannot appear in anyone's inbox. If the brief supplies local
filenames instead of URLs, ask for hosted addresses before building.

## The compliance footer is always added

Benchmark appends a compliant footer to every send from this editor: unsubscribe link,
report-abuse link, company name, and physical mailing address.

It is unconditional. Benchmark does not scan the HTML to see whether one is already there,
and the footer cannot be styled or turned off. Writing your own means the recipient sees two.

End the email on the content, the sign-off, or the call to action. Nothing legal or
administrative goes after it.

Accounts with no mailing address on file are prompted to add one before they can send,
schedule, or even test-send.

## Links and tracking

Benchmark rewrites links for click tracking and adds its own open-tracking pixel at send.

- Use complete https:// URLs in every `href`.
- Do not add tracking pixels; there is already one.
- Do not use `#` anchor links. They do not work reliably in email clients and interact badly
  with link rewriting.
- Do not use `mailto:` for a primary CTA; many clients handle it unpredictably.

## The preview matches the build targets

The editor's live preview renders at 600px in Desktop mode and 375px in Mobile mode. Building
the container at 600px and checking the stack at 375px means the preview shows what was
designed rather than an approximation.

The preview is the only rendering reference in the editor. It is not an email-client
compatibility checker, so it will not catch an Outlook-specific problem. That is why the
table-based, inline-styled patterns matter: they are what holds up when the preview cannot
tell you it will not.

## Subject line and preview text live on the checklist

Neither belongs in the HTML. Benchmark collects both on the email checklist after the design is
finished, so a subject line or a hidden preheader block written into the document duplicates what
the platform already asks for.

The limits are Benchmark's own:

| Field | Limit |
|---|---|
| Subject line | up to **80 characters** |
| Preview text | **50 characters or less** |

**Preview text is the shorter of the two.** That inverts the usual email-marketing advice, which
assumes a preheader can run longer than the subject and treats 90 to 140 characters as normal. An
assistant working from general knowledge will overshoot this every time, and the overflow is simply
cut. Write preview text that earns its 50 characters by saying something the subject line does not.

## Imperfect HTML is handled, not fixed

The editor accepts imperfect, malformed, or AI-generated HTML without crashing or wiping the
input. Trivial issues such as unclosed tags are repaired quietly. Structural issues that
would change the rendered output surface as plain-English, non-blocking warnings in an issues
panel.

This is deliberately not an HTML linter and not an email-client compatibility checker. A
warning means "this changed something," not "this will look wrong in Outlook." Treat it as a
safety net for bad markup, not as a substitute for building correctly.

## The editor type is locked at creation

Choosing Custom HTML when starting the email locks that campaign to the HTML editor. There is
no switching an existing HTML campaign to the drag-and-drop editor or the reverse.

Everything downstream is identical to any other campaign: the same checklist, test sends,
suppression, scheduling, open and click tracking, reports, and thumbnails in the email
listing.
