#!/usr/bin/env python3
"""Check an HTML email against the Benchmark HTML editor's real constraints."""
import re, sys, os

BANNED_TAGS = ["script", "form", "iframe", "embed", "object", "input", "select", "video"]
FOOTER_WORDS = ["unsubscribe", "manage preferences", "update your preferences",
                "report abuse", "opt out", "opt-out", "view in browser"]
FOREIGN_TAGS = [r"\*\|[A-Z_]+\|\*", r"\{\{[a-z_ ]+\}\}", r"%%[a-z_]+%%", r"\[\[[a-z_]+\]\]"]


def _lum(hexcolor):
    h = hexcolor.lstrip("#")
    if len(h) == 3:
        h = "".join(c * 2 for c in h)
    if len(h) != 6:
        return None
    try:
        r, g, b = (int(h[i:i+2], 16) / 255 for i in (0, 2, 4))
    except ValueError:
        return None
    f = lambda c: c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
    return 0.2126 * f(r) + 0.7152 * f(g) + 0.0722 * f(b)


def fragile_reversed_text(html):
    """Light text that depends on a background set on some OTHER element.

    Observed in the Benchmark editor: a background on a distant wrapper does not
    reliably paint, while one on the text-bearing element -- or on the cell that
    directly contains it -- does. Light text whose only background lives further up
    the tree renders light-on-white and disappears, and it looks perfect in every
    browser preview, so it reaches the inbox.

    Safe: the tag carries its own background, OR the <td> directly containing it
    declares one (bgcolor, inline background-color, or both). That second case is the
    normal, correct construction -- a coloured cell with an <h1> or <p> inside it --
    and flagging it trained people to ignore this check.

    Still caught: a background on a wrapper <table> with the light text in a cell that
    declares none of its own.
    """
    def has_bg(tag):
        return bool(re.search(r'background(-color)?:\s*(#|rgb)', tag, re.I)
                    or re.search(r'\bbgcolor\s*=\s*"[^"]+"', tag, re.I))

    offenders = []
    td_stack = []
    for m in re.finditer(r"<(/?)(td|div|p|span|a|h[1-6]|font|table)\b([^>]*)>", html, re.I):
        closing, name, attrs = m.group(1), m.group(2).lower(), m.group(3)
        tag = m.group(0)

        if name == "td":
            if closing:
                if td_stack:
                    td_stack.pop()
            elif not tag.rstrip().endswith("/>"):
                td_stack.append(tag)
            # a <td> is itself text-bearing; fall through to the colour check below
            if closing:
                continue

        if closing:
            continue

        c = re.search(r"(?<![-\w])color:\s*(#[0-9a-fA-F]{3,6})", tag)
        if not c:
            continue
        lum = _lum(c.group(1))
        if lum is None or lum < 0.55:
            continue

        if has_bg(tag):
            continue
        # The cell directly containing this text counts as its background.
        enclosing = td_stack[-1] if td_stack else None
        if name != "td" and enclosing and has_bg(enclosing):
            continue
        offenders.append(c.group(1))
    return offenders


def check(path):
    html = open(path, encoding="utf-8").read()
    low = html.lower()
    size = os.path.getsize(path)
    fails, warns, passes = [], [], []

    def t(cond, msg):
        (passes if cond else fails).append(msg)

    # Document completeness
    if low.lstrip().startswith("<!doctype html"):
        t(True, "Starts with <!DOCTYPE html>")
    elif "<html" in low:
        t(False, "Missing <!DOCTYPE html> — add it back as the very first line (chat windows often swallow it)")
    else:
        t(False, "Starts with <!DOCTYPE html>")
    t("</html>" in low, "Ends with a closed <html>")
    t("<html lang=" in low, "<html> has a lang attribute")
    t('charset="utf-8"' in low or "charset=utf-8" in low, "Declares UTF-8 charset")
    t('name="viewport"' in low, "Has a viewport meta")
    t("x-apple-disable-message-reformatting" in low, "Has x-apple-disable-message-reformatting")
    t('name="color-scheme"' in low, "Declares color-scheme")
    t("mso-" in low, "Contains MSO/Outlook handling")

    # Sanitizer
    for tag in BANNED_TAGS:
        t(f"<{tag}" not in low, f"No <{tag}> (Benchmark strips it)")
    handlers = re.findall(r"\son(click|load|error|mouseover|mouseout|focus|blur)\s*=", low)
    t(not handlers, "No inline event handlers (Benchmark strips them)")

    # Size
    t(size <= 500_000, f"Under the 500 KB cap ({size:,} bytes)")
    b64 = re.findall(r'src="data:image[^"]{50000,}"', html)
    t(not b64, "No oversized base64 images")

    # Footer duplication
    for w in FOOTER_WORDS:
        t(w not in low, f'No "{w}" (Benchmark appends its own footer)')
    t(not re.search(r"\b\d{5}(-\d{4})?\b(?![^<]*</title>)", re.sub(r"<style.*?</style>", "", html, flags=re.S)),
      "No US ZIP-code-looking string (possible hardcoded address)")

    # Foreign merge tags
    for pat in FOREIGN_TAGS:
        t(not re.search(pat, html), f"No foreign merge tags matching {pat}")

    # Structure
    tables = re.findall(r"<table[^>]*>", low)
    t(tables, "Uses tables for layout")
    no_role = [x for x in tables if "role=\"presentation\"" not in x]
    t(not no_role, f"Every layout table has role=presentation ({len(tables)} tables)")
    missing_attrs = [x for x in tables if not all(a in x for a in ["cellpadding=\"0\"", "cellspacing=\"0\"", "border=\"0\""])]
    t(not missing_attrs, "Every table has cellpadding/cellspacing/border=0")
    for prop in ["display:flex", "display: flex", "display:grid", "display: grid", "float:", "position:absolute"]:
        t(prop not in low, f"No {prop} used for structure")
    t("max-width:600px" in low.replace(" ", "") or "max-width: 600px" in low, "Container constrained to 600px")

    # Inline styles carry the design
    inline = len(re.findall(r'style="', html))
    t(inline >= 10, f"Design carried by inline styles ({inline} style attributes)")

    # Images
    imgs = re.findall(r"<img[^>]*>", html, re.I)
    for i, img in enumerate(imgs, 1):
        il = img.lower()
        t("alt=" in il, f"Image {i} has alt text")
        t("width=" in il, f"Image {i} has an explicit width attribute")
        t("display:block" in il.replace(" ", ""), f"Image {i} has display:block")
        t('src="https://' in il or "src='https://" in il, f"Image {i} uses an absolute https URL")
        t(not re.search(r'src="[^"]+\.(svg|webp)', il), f"Image {i} is not SVG or WebP (Gmail and Outlook render neither)")

    # Links
    hrefs = re.findall(r'href="([^"]*)"', html)
    for h in hrefs:
        t(h.startswith("https://"), f'Link "{h[:50]}" is an absolute https URL')
        t(not h.startswith("#"), f'Link "{h[:50]}" is not a bare anchor')

    # Preview text belongs on the checklist, never in the HTML
    t("mso-hide:all" not in low.replace(" ", ""), "No hidden preheader (preview text is set on the checklist)")

    # Contrast: the failure that renders text invisible
    ghosts = fragile_reversed_text(html)
    if ghosts:
        t(False, f"Light text relies on a background set elsewhere and can render invisible: {', '.join(sorted(set(ghosts))[:4])}")
    else:
        t(True, "All light text carries its own background on the same element")

    # Stray content around the document — usually swept up when copying out of a chat window
    AI_ARTIFACTS = ["fallbackmarkdown", "sources_footnote", "showloginrequiredcard",
                    "matched_text", "```html", "```",
                    # status and reasoning labels the chat UI renders around a response
                    "worked for", "thought for", "thinking", "writing", "analyzing",
                    "searched the web", "reasoned for", "planning"]
    tail = low.rsplit("</html>", 1)[-1].strip() if "</html>" in low else ""
    # anchor on the doctype, or on <html> when the renderer has eaten the doctype
    if "<!doctype" in low:
        head = low.split("<!doctype", 1)[0].strip()
    elif "<html" in low:
        head = low.split("<html", 1)[0].strip()
    else:
        head = ""
    found = sorted({a for a in AI_ARTIFACTS if a in tail or a in head})
    if found:
        t(False, f"Chat-client junk copied in around the HTML — delete it: {', '.join(found[:3])}")
    elif tail or head:
        t(False, f"Stray text outside the document ({len(head)} chars before, {len(tail)} after)")
    else:
        t(True, "Nothing outside the HTML document")
    t("</html>" in low, "Document is complete, not cut off mid-generation")

    # Type
    small = re.findall(r"font-size:\s*(\d+)px", low)
    body_sizes = [int(s) for s in small if 1 < int(s) < 14]
    t(not body_sizes, f"No body copy under 14px (found sizes: {sorted(set(int(s) for s in small))})")
    visible = re.sub(r"<[^>]+>", " ", re.sub(r"<(style|head)\b.*?</\1>", "", html, flags=re.S | re.I))
    words = len([w for w in re.split(r"\s+", visible) if len(w) > 2])
    t(words >= 25, f"Body copy is real selectable text, not an image ({words} words)")

    # Fonts
    stacks = re.findall(r"font-family:([^;\"]*)", low)
    safe = ["arial", "helvetica", "georgia", "verdana", "tahoma", "trebuchet", "courier", "times"]
    for s in set(stacks):
        t(any(w in s for w in safe), f"Font stack has a web-safe fallback: {s.strip()[:60]}")

    # Every text-bearing <td> declares its own font-family. Outlook does not inherit it
    # from a parent, so a cell that omits it falls back to Times New Roman.
    bare = 0
    for cell in re.finditer(r"<td\b([^>]*)>(.*?)</td>", html, re.S | re.I):
        attrs, inner = cell.group(1), cell.group(2)
        text = re.sub(r"<[^>]+>", " ", re.sub(r"<!--.*?-->", "", inner, flags=re.S))
        if len([w for w in re.split(r"\s+", text) if len(w) > 2]) < 3:
            continue  # spacer or image-only cell
        if "font-family" not in attrs.lower() and "font-family" not in inner.lower():
            bare += 1
    t(not bare, f"Every text-bearing <td> declares its own font-family ({bare} without)")

    return fails, passes, size


if __name__ == "__main__":
    exit_code = 0
    for path in sys.argv[1:]:
        fails, passes, size = check(path)
        print(f"\n=== {os.path.basename(path)} ({size:,} bytes) ===")
        print(f"PASS: {len(passes)}   FAIL: {len(fails)}")
        for f in fails:
            print(f"  FAIL  {f}")
            exit_code = 1
        if not fails:
            print("  All constraint checks passed.")
    sys.exit(exit_code)
