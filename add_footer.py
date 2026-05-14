#!/usr/bin/env python3
# coding: utf-8


import argparse
import os
import re
import sys
import xml.etree.ElementTree as ET
from datetime import datetime


# --- Citation constants (edit here if the citation ever changes) ----------
AUTHORS = (
    "Cristina Guardiano, Paola Crisma, Giuseppe Longobardi, "
    "Marco Longhin, Giovanni Battista Matteazzi, "
    "Emanuela Li Destri, Gaia Sorge"
)
YEAR = "2026"
RESOURCE = "The PCM_Hub"
VERSION = "version 1"

# --- Styling (shared between raster and SVG) ------------------------------
TEXT_COLOR_RGB = (68, 68, 68)        
TEXT_COLOR_HEX = "#444444"         
BAND_COLOR_RGB = (255, 255, 255) 
BAND_COLOR_HEX = "white"
PADDING_VERT = 30
PADDING_HORIZ = 40
LINE_SPACING = 8

SVG_NS = "http://www.w3.org/2000/svg"


def build_footer_lines():
    today = datetime.now().strftime("%d/%m/%Y")
    line1 = "Downloaded from:"
    line2 = (
        f"{AUTHORS} (eds). {YEAR}. {RESOURCE} "
        f"({VERSION}, Accessed on {today})"
    )
    return line1, line2


# --- Raster branch (PNG, JPG, ...) ----------------------------------------

def _load_italic_font(size):
    from PIL import ImageFont
    candidates = [
        r"C:\Windows\Fonts\ariali.ttf",
        r"C:\Windows\Fonts\timesi.ttf",
        r"C:\Windows\Fonts\calibrii.ttf",
        "/usr/share/fonts/truetype/dejavu/DejaVuSans-Oblique.ttf",
        "/usr/share/fonts/truetype/liberation/LiberationSans-Italic.ttf",
        "/Library/Fonts/Arial Italic.ttf",
        "/System/Library/Fonts/Supplemental/Arial Italic.ttf",
    ]
    for path in candidates:
        if os.path.exists(path):
            try:
                return ImageFont.truetype(path, size)
            except Exception:
                continue
    return ImageFont.load_default()


def _wrap_to_width(text, font, max_width, draw):
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        w = draw.textbbox((0, 0), trial, font=font)[2]
        if w <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _add_footer_raster(input_path, output_path):
    try:
        from PIL import Image, ImageDraw
    except ImportError:
        sys.exit(
            "Error: Pillow is required for raster images. "
            "Install it with:  pip install Pillow"
        )

    img = Image.open(input_path).convert("RGB")
    width, height = img.size

    font_size = max(12, min(20, width // 90))
    font = _load_italic_font(font_size)

    line1, line2 = build_footer_lines()

    tmp_draw = ImageDraw.Draw(Image.new("RGB", (10, 10)))
    max_text_width = width - 2 * PADDING_HORIZ
    wrapped = _wrap_to_width(line2, font, max_text_width, tmp_draw)
    all_lines = [line1] + wrapped

    line_heights = [
        tmp_draw.textbbox((0, 0), ln, font=font)[3]
        - tmp_draw.textbbox((0, 0), ln, font=font)[1]
        for ln in all_lines
    ]
    text_block_h = sum(line_heights) + LINE_SPACING * (len(all_lines) - 1)
    band_h = text_block_h + 2 * PADDING_VERT

    new_img = Image.new("RGB", (width, height + band_h), BAND_COLOR_RGB)
    new_img.paste(img, (0, 0))

    draw = ImageDraw.Draw(new_img)
    y = height + PADDING_VERT
    for i, line in enumerate(all_lines):
        bbox = draw.textbbox((0, 0), line, font=font)
        text_w = bbox[2] - bbox[0]
        x = (width - text_w) // 2
        draw.text((x, y), line, font=font, fill=TEXT_COLOR_RGB)
        y += line_heights[i] + LINE_SPACING

    new_img.save(output_path)
    return output_path


# --- SVG branch -----------------------------------------------------------

def _parse_dim(value):
    """Extract numeric value + unit from an SVG dimension like '500px'."""
    if value is None:
        return None
    m = re.match(r"^\s*([\d.]+)\s*([a-zA-Z%]*)\s*$", value)
    if not m:
        return None
    return float(m.group(1)), m.group(2)


def _wrap_text_chars(text, max_chars):
    """Greedy word-wrap by approximate character count."""
    words = text.split()
    lines, current = [], ""
    for word in words:
        trial = (current + " " + word).strip()
        if len(trial) <= max_chars or not current:
            current = trial
        else:
            lines.append(current)
            current = word
    if current:
        lines.append(current)
    return lines


def _add_footer_svg(input_path, output_path):
    ET.register_namespace("", SVG_NS)
    tree = ET.parse(input_path)
    root = tree.getroot()

    # Read viewBox (preferred) or fall back to width/height
    viewBox = root.get("viewBox")
    if viewBox:
        vb_x, vb_y, vb_w, vb_h = map(float, viewBox.split())
    else:
        w_parsed = _parse_dim(root.get("width"))
        h_parsed = _parse_dim(root.get("height"))
        vb_x, vb_y = 0.0, 0.0
        vb_w = w_parsed[0] if w_parsed else 500.0
        vb_h = h_parsed[0] if h_parsed else 500.0

    # Footer geometry in viewBox units
    font_size = max(10.0, min(20.0, vb_w / 60.0))
    pad_v = font_size * 1.2
    pad_h = font_size * 2.0
    line_spacing = font_size * 0.4

    line1, line2 = build_footer_lines()

    # Approximate wrap by character count (italic Arial-ish, ~0.5 * size)
    approx_char_width = font_size * 0.5
    max_chars = max(20, int((vb_w - 2 * pad_h) / approx_char_width))
    wrapped = _wrap_text_chars(line2, max_chars)
    all_lines = [line1] + wrapped

    text_block_h = (
        len(all_lines) * font_size
        + (len(all_lines) - 1) * line_spacing
    )
    band_h = text_block_h + 2 * pad_v
    new_vb_h = vb_h + band_h

    # Extend viewBox and physical height proportionally
    root.set("viewBox", f"{vb_x} {vb_y} {vb_w} {new_vb_h}")
    h_attr = root.get("height")
    if h_attr is not None:
        h_parsed = _parse_dim(h_attr)
        if h_parsed:
            new_h_val = h_parsed[0] * (new_vb_h / vb_h)
            root.set("height", f"{new_h_val}{h_parsed[1]}")

    # White band covering the new bottom area
    rect = ET.SubElement(root, f"{{{SVG_NS}}}rect")
    rect.set("x", str(vb_x))
    rect.set("y", str(vb_y + vb_h))
    rect.set("width", str(vb_w))
    rect.set("height", str(band_h))
    rect.set("fill", BAND_COLOR_HEX)
    rect.set("stroke", "none")

    # Centered italic text lines
    y_text = vb_y + vb_h + pad_v + font_size
    for line in all_lines:
        t = ET.SubElement(root, f"{{{SVG_NS}}}text")
        t.set("x", str(vb_x + vb_w / 2.0))
        t.set("y", str(y_text))
        t.set("text-anchor", "middle")
        t.set("font-family", "Arial, Helvetica, sans-serif")
        t.set("font-style", "italic")
        t.set("font-size", str(font_size))
        t.set("fill", TEXT_COLOR_HEX)
        t.text = line
        y_text += font_size + line_spacing

    tree.write(output_path, xml_declaration=True, encoding="utf-8")
    return output_path


# --- Public dispatcher ----------------------------------------------------

def add_footer(input_path, output_path=None):
    if output_path is None:
        base, ext = os.path.splitext(input_path)
        output_path = f"{base}_credits{ext}"

    ext = os.path.splitext(input_path)[1].lower()
    if ext == ".svg":
        result = _add_footer_svg(input_path, output_path)
    else:
        result = _add_footer_raster(input_path, output_path)

    print(f"Saved: {result}")
    return result


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Add PCM_Hub citation footer to a PNG or SVG image."
    )
    parser.add_argument(
        "-i", "--input", required=True,
        help="Input image file path (PNG or SVG)"
    )
    parser.add_argument(
        "-o", "--output", default=None,
        help="Output file path (default: <input>_credits.<ext>)"
    )
    args = parser.parse_args()
    add_footer(args.input, args.output)
