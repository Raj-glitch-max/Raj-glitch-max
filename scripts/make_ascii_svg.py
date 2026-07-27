#!/usr/bin/env python3
import sys
import os
from PIL import Image, ImageDraw, ImageFont
import numpy as np

RAMP = " .`:-=+*cs#%@"  # bright (sparse) -> dark (dense)

def generate_fallback_image(path="source-prepped.png", width=300, height=300):
    """Generates a stylish grayscale silhouette portrait if no source image exists."""
    img = Image.new("L", (width, height), 255)
    draw = ImageDraw.Draw(img)
    
    # Draw head / face silhouette with gradients / shading
    center_x, center_y = width // 2, height // 2 - 10
    
    # Head & shoulders
    draw.ellipse([center_x - 110, center_y + 40, center_x + 110, center_y + 220], fill=60)
    draw.ellipse([center_x - 70, center_y - 90, center_x + 70, center_y + 70], fill=40)
    # Face highlights (CLAHE effect simulation)
    draw.ellipse([center_x - 45, center_y - 65, center_x + 45, center_y + 45], fill=120)
    draw.ellipse([center_x - 30, center_y - 50, center_x + 30, center_y + 25], fill=180)
    # Hair / features contour
    draw.arc([center_x - 72, center_y - 92, center_x + 72, center_y + 30], start=180, end=360, fill=20, width=15)
    # Glasses / eyes detail
    draw.rectangle([center_x - 45, center_y - 25, center_x - 10, center_y - 10], fill=30)
    draw.rectangle([center_x + 10, center_y - 25, center_x + 45, center_y - 10], fill=30)
    draw.line([center_x - 10, center_y - 18, center_x + 10, center_y - 18], fill=30, width=3)
    
    img.save(path)
    print(f"Generated fallback prepped image at '{path}'.")

def image_to_ascii_grid(image_path, target_width=100):
    if not os.path.exists(image_path):
        print(f"Notice: '{image_path}' not found. Generating fallback portrait...")
        generate_fallback_image(image_path)

    img = Image.open(image_path).convert("L")
    w, h = img.size
    
    # Monospace aspect ratio adjustment (~0.5 char width/height ratio)
    aspect_ratio = h / w
    target_height = int(target_width * aspect_ratio * 0.52)
    target_height = max(20, min(80, target_height))  # Reasonable range ~50-55 lines
    
    img_resized = img.resize((target_width, target_height), Image.Resampling.LANCZOS)
    pixels = np.array(img_resized)
    
    ascii_rows = []
    ramp_len = len(RAMP)
    
    for row in pixels:
        line_chars = []
        for p in row:
            # 255 is white (index 0 -> ' '), 0 is black (index max -> '@')
            idx = int((255 - int(p)) / 255.0 * (ramp_len - 1))
            idx = max(0, min(ramp_len - 1, idx))
            line_chars.append(RAMP[idx])
        ascii_rows.append("".join(line_chars))
        
    return ascii_rows, target_width, target_height

def make_ascii_svg(image_path="source-prepped.png", output_path="avi-ascii.svg"):
    target_width = 100
    rows, num_cols, num_rows = image_to_ascii_grid(image_path, target_width=target_width)
    
    # Dimensions for output SVG
    svg_width = 370
    padding_x = 12
    padding_top = 36
    padding_bottom = 14
    
    usable_width = svg_width - (padding_x * 2)
    # Character sizing
    font_size = 6.2
    line_height = 7.0
    char_width = usable_width / num_cols
    
    content_height = num_rows * line_height
    svg_height = int(padding_top + content_height + padding_bottom)
    
    # Timing configuration for SMIL animation
    row_dur = 0.06      # Duration per row wipe (seconds)
    row_stagger = 0.03  # Delay between starting successive rows (seconds)
    
    # Escape XML helper
    def xml_escape(text):
        return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;").replace('"', "&quot;").replace(" ", "&#160;")

    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    svg_lines.append('  <style>')
    svg_lines.append('    .bg { fill: #0d1117; rx: 6px; stroke: #30363d; stroke-width: 1px; }')
    svg_lines.append('    .header-dot { rx: 50%; }')
    svg_lines.append('    .ascii-text { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; font-size: ' + f'{font_size:.2f}px' + '; fill: #8b949e; white-space: pre; }')
    svg_lines.append('    .title { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 11px; fill: #8b949e; font-weight: 600; }')
    svg_lines.append('  </style>')
    
    # Terminal frame
    svg_lines.append(f'  <rect width="{svg_width}" height="{svg_height}" class="bg" />')
    # Terminal header controls
    svg_lines.append('  <circle cx="16" cy="16" r="4.5" fill="#ff5f56" />')
    svg_lines.append('  <circle cx="28" cy="16" r="4.5" fill="#ffbd2e" />')
    svg_lines.append('  <circle cx="40" cy="16" r="4.5" fill="#27c93f" />')
    svg_lines.append('  <text x="56" y="19" class="title">portrait.asc</text>')
    
    # Defs for clip paths
    svg_lines.append('  <defs>')
    for y in range(num_rows):
        start_time = y * row_stagger
        y_pos = padding_top + (y * line_height)
        svg_lines.append(f'    <clipPath id="row-clip-{y}">')
        svg_lines.append(f'      <rect x="0" y="{y_pos - 1:.2f}" width="0" height="{line_height + 1:.2f}">')
        svg_lines.append(f'        <animate attributeName="width" from="0" to="{svg_width}" begin="{start_time:.3f}s" dur="{row_dur:.3f}s" fill="freeze" />')
        svg_lines.append('      </rect>')
        svg_lines.append('    </clipPath>')
    svg_lines.append('  </defs>')
    
    # Text group & rows
    svg_lines.append(f'  <g transform="translate({padding_x}, 0)">')
    for y, row_str in enumerate(rows):
        start_time = y * row_stagger
        y_pos = padding_top + (y * line_height) + (line_height * 0.8)
        escaped_str = xml_escape(row_str)
        
        # Wrapped line with clipPath
        svg_lines.append(f'    <g clip-path="url(#row-clip-{y})">')
        svg_lines.append(f'      <text x="0" y="{y_pos:.2f}" class="ascii-text">{escaped_str}</text>')
        svg_lines.append('    </g>')
        
        # Cursor riding the wipe edge
        cursor_y = padding_top + (y * line_height)
        svg_lines.append(f'    <rect x="{padding_x}" y="{cursor_y:.2f}" width="{char_width * 1.5:.2f}" height="{line_height:.2f}" fill="#58a6ff" opacity="0">')
        svg_lines.append(f'      <animate attributeName="x" from="{padding_x}" to="{padding_x + usable_width}" begin="{start_time:.3f}s" dur="{row_dur:.3f}s" fill="freeze" />')
        svg_lines.append(f'      <animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.05;0.95;1" begin="{start_time:.3f}s" dur="{row_dur:.3f}s" fill="freeze" />')
        svg_lines.append('    </rect>')
        
    svg_lines.append('  </g>')
    svg_lines.append('</svg>')
    
    content = "\n".join(svg_lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Successfully generated '{output_path}' ({num_cols}x{num_rows} grid, {svg_width}x{svg_height} SVG).")

if __name__ == "__main__":
    img_path = sys.argv[1] if len(sys.argv) > 1 else "source-prepped.png"
    make_ascii_svg(img_path, "avi-ascii.svg")
