# Email HTML patterns

Reference snippets for the parts that break most often. All of them assume the Benchmark
constraints in `benchmark-constraints.md`.

## Document shell

```html
<!DOCTYPE html>
<html lang="en" xmlns:v="urn:schemas-microsoft-com:vml" xmlns:o="urn:schemas-microsoft-com:office:office">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <meta name="x-apple-disable-message-reformatting">
  <meta name="color-scheme" content="light">
  <meta name="supported-color-schemes" content="light">
  <title>Descriptive title</title>
  <!--[if mso]>
  <xml><o:OfficeDocumentSettings><o:PixelsPerInch>96</o:PixelsPerInch></o:OfficeDocumentSettings></xml>
  <![endif]-->
  <style>
    /* Progressive enhancement only. The email must work with this block deleted. */
    @media only screen and (max-width: 600px) {
      .stack { display: block !important; width: 100% !important; max-width: 100% !important; }
      .px { padding-left: 20px !important; padding-right: 20px !important; }
      .h1 { font-size: 26px !important; line-height: 32px !important; }
    }
  </style>
</head>
```

Set `lang` to the language of the copy. Benchmark's UI ships in English, Spanish, Japanese,
Portuguese, and Traditional Chinese, and campaigns are written in plenty more.

## 600px container

```html
<body style="margin:0; padding:0; background-color:#F4F4F5;">
<table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%" style="background-color:#F4F4F5;">
  <tr>
    <td align="center" style="padding:24px 12px;">
      <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="600" style="width:100%; max-width:600px; background-color:#FFFFFF;">
        <!-- content rows -->
      </table>
    </td>
  </tr>
</table>
</body>
```

The `width="600"` attribute and the `max-width:600px` style both need to be there. Outlook
reads the attribute; everything else reads the style.

## Bulletproof button

```html
<tr>
  <td align="center" style="padding:8px 24px 32px 24px;">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0">
      <tr>
        <td align="center" bgcolor="#3C247F" style="border-radius:6px;">
          <!--[if mso]>&nbsp;<![endif]-->
          <a href="https://example.com/offer"
             style="display:inline-block; padding:14px 32px; font-family:Arial, Helvetica, sans-serif; font-size:16px; font-weight:bold; line-height:20px; color:#FFFFFF; background-color:#3C247F; text-decoration:none; border-radius:6px; mso-line-height-rule:exactly;">
            Shop the Collection
          </a>
          <!--[if mso]>&nbsp;<![endif]-->
        </td>
      </tr>
    </table>
  </td>
</tr>
```

The background color goes in **three** places: `bgcolor` and CSS on the `<td>`, and again as
`background-color` on the `<a>` itself. That last one is what actually keeps the white label
readable — see "Light text" below. Never make a button out of an image alone; blocked images
turn it into nothing.

## Image

```html
<img src="https://cdn.example.com/hero.jpg"
     alt="Two bags of fall blend coffee on a wooden counter"
     width="600"
     style="display:block; border:0; width:100%; max-width:600px; height:auto;">
```

PNG, JPG, or GIF only. SVG and WebP do not render in Gmail or Outlook, and both look fine in a
browser preview, so the failure is invisible until it reaches a real inbox.

Write alt text a person would understand if the image never loads. Put a background color on
the containing `<td>` so a blocked image leaves a deliberate block of color, not a white gap.

## Two columns that stack

```html
<tr>
  <td style="padding:0 24px;">
    <table role="presentation" cellpadding="0" cellspacing="0" border="0" width="100%">
      <tr>
        <td class="stack" width="50%" valign="top" style="padding:0 12px 24px 0; font-family:Arial, Helvetica, sans-serif; font-size:16px; line-height:24px; color:#3C3549;">
          Left column
        </td>
        <td class="stack" width="50%" valign="top" style="padding:0 0 24px 12px; font-family:Arial, Helvetica, sans-serif; font-size:16px; line-height:24px; color:#3C3549;">
          Right column
        </td>
      </tr>
    </table>
  </td>
</tr>
```

The `.stack` class only works where the `<style>` block survives. Check that the side-by-side
version is still acceptable at 375px, because in some clients that is what people will see.
Read the stacked order out loud: left column then right column has to make sense as a
sequence, not just as a layout.

## Background image with VML fallback for Outlook

```html
<td background="https://cdn.example.com/bg.jpg" bgcolor="#3C247F" valign="top" style="background-image:url('https://cdn.example.com/bg.jpg'); background-size:cover; background-position:center;">
  <!--[if gte mso 9]>
  <v:rect xmlns:v="urn:schemas-microsoft-com:vml" fill="true" stroke="false" style="width:600px; height:300px;">
    <v:fill type="frame" src="https://cdn.example.com/bg.jpg" color="#3C247F" />
    <v:textbox inset="0,0,0,0"><div>
  <![endif]-->
  <!-- real content here -->
  <!--[if gte mso 9]></div></v:textbox></v:rect><![endif]-->
</td>
```

The `bgcolor` is doing the real work. Assume the image will not load somewhere and pick a
color that keeps the text readable on its own.

## Type

Set the font stack on every text-bearing `<td>`. Do not rely on inheritance; Outlook does not
cooperate.

```html
<td style="font-family:Arial, Helvetica, sans-serif; font-size:16px; line-height:24px; color:#3C3549; mso-line-height-rule:exactly;">
```

Safe stacks:

- `Arial, Helvetica, sans-serif`
- `Georgia, 'Times New Roman', serif`
- `Verdana, Geneva, sans-serif`
- `'Trebuchet MS', sans-serif`
- `Tahoma, sans-serif`
- `'Courier New', monospace`

A brand web font goes first with a web-safe fallback immediately behind it:
`'Poppins', Arial, Helvetica, sans-serif`. Design for the fallback, because Gmail and Outlook
will not load the web font.

## Light text: put the background on the same element

The rule: **any element with light-colored text must carry its own `background-color`.** A
background on the surrounding `<td>` is not enough to rely on.

Observed in the Benchmark editor: a colored `<td>` band does not reliably paint, while a
background set on the text-bearing element does. When the band drops out, light text lands on
white and the whole section renders as blank space — and it looks perfect in every browser
preview, so it reaches the inbox unnoticed.

```html
<tr>
  <td bgcolor="#3C247F" style="background-color:#3C247F; padding:44px 48px;">
    <p style="margin:0; font-family:Arial, Helvetica, sans-serif; font-size:36px; line-height:44px; color:#FFFFFF; background-color:#3C247F; mso-line-height-rule:exactly;">
      Headline
    </p>
  </td>
</tr>
```

Belt, braces, and a third strap. But the safer move is to **not build reversed sections at
all.** Dark text on a light background cannot fail this way. Get emphasis from type scale,
weight, rules, and small accent-colored labels instead of full-width color bands.

## Dark mode

Many clients invert colors automatically and none of them ask first.

- Declare `color-scheme` and `supported-color-schemes` as `light` in `<head>`.
- Avoid pure white logos on transparent backgrounds; they vanish when the background inverts.
- Do not rely on a white background to create contrast. Give text an explicit color and its
  container an explicit background color.
- Mid-tone brand colors survive inversion better than near-black or near-white.

## Spacing

Vertical space comes from `<td>` padding or a dedicated spacer row:

```html
<tr><td style="height:32px; line-height:32px; font-size:0;">&nbsp;</td></tr>
```

Never `margin` on a `<p>` or `<div>` for structural spacing. Set `margin:0` on any `<p>` and
control the space with the parent `<td>`.
