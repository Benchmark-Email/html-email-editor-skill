# Reviewing and fixing existing email HTML

Use this when someone brings HTML written elsewhere: a designer's file, an export from
another platform, or output from a different AI tool.

Work the checklist in order. Report what changed and why. If a fix alters how the email
looks, say so before returning the code.

## 1. Things Benchmark will strip

Search for and remove:

- `<script>` blocks
- `<form>`, `<input>`, `<select>`, `<button type=...>`
- `<iframe>`, `<embed>`, `<object>`
- Any `on*` attribute: `onclick`, `onload`, `onmouseover`, `onerror`

If any of these carried real behavior, say what was lost rather than replacing it silently.
Interactive elements have no working equivalent in email.

## 2. Styles that will not survive

- Any style in a `<style>` block or external stylesheet that the layout depends on. Move it
  inline onto the element. Leave `@media` queries in the block.
- `<link rel="stylesheet">` and `@import`. Remove; nothing external loads.
- CSS custom properties (`var(--brand)`). Resolve them to literal values.
- `flex`, `grid`, `float`, `position`. Rebuild the structure as nested tables.
- `margin` used for structural spacing. Move to `<td>` padding or spacer rows.

## 3. Footer duplication

The single most common problem with HTML written for another platform.

Find and delete any unsubscribe link, "manage preferences" or "update your preferences" link,
"view in browser" link tied to another platform, physical mailing address, or another
platform's merge tags in a footer (`*|UNSUB|*`, `{{unsubscribe}}`, `%%unsubscribe%%`, and
similar).

Benchmark adds its own compliant footer to every send. Anything left behind shows up twice.

## 4. Foreign merge tags

Other platforms' tokens render as literal text in Benchmark. Replace each with a plain
uppercase placeholder and note it for the person to fix with the Personalize button:

| Found | Replace with |
|---|---|
| `*\|FNAME\|*` | `FIRST_NAME_HERE` |
| `{{first_name}}` | `FIRST_NAME_HERE` |
| `%%first_name%%` | `FIRST_NAME_HERE` |
| `[[first_name]]` | `FIRST_NAME_HERE` |

Do not translate them into Benchmark tags. The correct token depends on the account's own
field names, and a malformed one renders as visible text in the inbox.

## 5. Images

- Any `.svg` or `.webp` image source. Gmail and Outlook render neither, so the reader sees a
  broken image or nothing. This is easy to miss because both render perfectly in a browser
  preview. Ask for a PNG or JPG. Logos pulled from a website are the usual offender.
- Any `src` that is a relative path, a `file://` path, or a `cid:` reference will not load.
  Ask for a public https:// URL.
- Any `http://` URL should become `https://`.
- Add missing `alt` text, `width`, and `style="display:block; border:0; height:auto"`.
- Flag any image carrying essential copy. Blocked images make it unreadable, and screen
  readers never see it.
- Flag base64 images larger than roughly 50 KB against the 500 KB total.

## 6. Size

Check the total byte count. Over 500 KB is rejected on save. The usual cause is embedded
base64 images; the usual fix is hosting them.

## 7. Width and structure

- Container wider than 600px, or with no `max-width`. Constrain it.
- Missing `role="presentation"` on layout tables. Add it.
- Missing `cellpadding="0" cellspacing="0" border="0"`. Add it.
- Tables with a CSS width but no `width` attribute. Outlook needs the attribute.

## 8. Type and contrast

- Body copy under 14px. Raise it.
- Missing font stack on a text-bearing `<td>`. Add it; inheritance is unreliable in Outlook.
- Web fonts with no web-safe fallback. Add one.
- Low contrast between text and background. Fix it, and check that it still holds if the
  client inverts colors.
- **Light text whose background lives on the surrounding `<td>` rather than on the text element
  itself.** Add `background-color` inline to the same tag as the text, or change the text to a
  dark color. A colored `<td>` band does not reliably paint; when it drops out the section
  renders as blank space. Browser previews never show this. Best fix is usually to rebuild the
  section as dark text on a light background.
- **Any image URL that was constructed rather than retrieved.** Load it. A 404 renders as a
  broken-image icon.

## 9. Links

- Relative `href` values. Make them absolute https:// URLs.
- `#` anchors. Remove or point them somewhere real.
- Tracking pixels from another platform. Remove; Benchmark adds its own.

## 10. What to hand back

The corrected complete document, plus a short list of what changed. Call out separately:

- Anything removed that the person may have wanted (interactive elements, a footer they wrote
  on purpose)
- Anything still needed from them (hosted image URLs, a real CTA link)
- Anywhere the fix changed the design

## The warnings panel is not this checklist

Benchmark's editor flags structural changes it made to malformed markup in a non-blocking
issues panel. That is a safety net for broken tags, not an inbox-compatibility review. A
clean panel does not mean the email will render well in Outlook. This checklist is what
covers that.
