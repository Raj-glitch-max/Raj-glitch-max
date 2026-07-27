#!/usr/bin/env python3
import os
import sys

def make_info_card(output_path="info-card.svg"):
    is_static = os.environ.get("STATIC") == "1"
    
    svg_width = 490
    svg_height = 405
    
    # Information rows for neofetch card
    rows = [
        {"type": "user", "key": "avi", "val": "Patil", "host": "github"},
        {"type": "sep", "val": "------------------------------------------------"},
        {"type": "row", "key": "OS", "val": "Linux / DevOps Engine", "color": "#58a6ff"},
        {"type": "row", "key": "Now", "val": "Building focused, composable CLI tools for cloud infrastructure", "color": "#79c0ff"},
        {"type": "row", "key": "Prev", "val": "Production AWS & Kubernetes Infra, Automated Self-Healing Systems", "color": "#d2a8ff"},
        {"type": "row", "key": "Stack", "val": "AWS · Kubernetes · Terraform · Docker · Python · Go · Linux", "color": "#7ee787"},
        {"type": "row", "key": "Highlights", "val": "tf-why · K8s Incident Diagnosis Benchmark · AI Self-Healing CI/CD", "color": "#ffa657"},
        {"type": "sep", "val": "------------------------------------------------"},
        {"type": "colors", "val": ["#ff5f56", "#ffbd2e", "#27c93f", "#58a6ff", "#bc8cff", "#39d353"]}
    ]
    
    css_anim = "" if is_static else """
    @keyframes slideFade {
      0% { opacity: 0; transform: translateY(6px); }
      100% { opacity: 1; transform: translateY(0); }
    }
    .anim-line {
      animation: slideFade 0.4s ease-out forwards;
    }
    """
    
    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    svg_lines.append('  <style>')
    svg_lines.append('    .bg { fill: #0d1117; rx: 6px; stroke: #30363d; stroke-width: 1px; }')
    svg_lines.append('    .title { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 11px; fill: #8b949e; font-weight: 600; }')
    svg_lines.append('    .term-text { font-family: ui-monospace, SFMono-Regular, "SF Mono", Menlo, Consolas, "Liberation Mono", monospace; font-size: 11.5px; }')
    svg_lines.append('    .user { fill: #58a6ff; font-weight: bold; }')
    svg_lines.append('    .host { fill: #bc8cff; font-weight: bold; }')
    svg_lines.append('    .at { fill: #c9d1d9; }')
    svg_lines.append('    .sep { fill: #30363d; }')
    svg_lines.append('    .key { font-weight: bold; }')
    svg_lines.append('    .val { fill: #c9d1d9; }')
    svg_lines.append(css_anim)
    svg_lines.append('  </style>')
    
    # Outer terminal card
    svg_lines.append(f'  <rect width="{svg_width}" height="{svg_height}" class="bg" />')
    
    # Window controls
    svg_lines.append('  <circle cx="16" cy="16" r="4.5" fill="#ff5f56" />')
    svg_lines.append('  <circle cx="28" cy="16" r="4.5" fill="#ffbd2e" />')
    svg_lines.append('  <circle cx="40" cy="16" r="4.5" fill="#27c93f" />')
    svg_lines.append('  <text x="56" y="19" class="title">avi@github ~ neofetch</text>')
    
    # Content rows
    start_y = 52
    line_spacing = 34
    
    for idx, item in enumerate(rows):
        y_pos = start_y + (idx * line_spacing)
        delay = 0.05 + (idx * 0.08)
        
        anim_attr = "" if is_static else f'class="anim-line" style="opacity: 0; animation-delay: {delay:.2f}s;"'
        
        svg_lines.append(f'  <g transform="translate(18, {y_pos})" {anim_attr}>')
        
        if item["type"] == "user":
            svg_lines.append(f'    <text x="0" y="0" class="term-text"><tspan class="user">{item["key"]}</tspan><tspan class="at">@</tspan><tspan class="host">{item["host"]}</tspan></text>')
        elif item["type"] == "sep":
            svg_lines.append(f'    <text x="0" y="0" class="term-text sep">{item["val"]}</text>')
        elif item["type"] == "row":
            key_col = item.get("color", "#58a6ff")
            # Word wrap or truncate if val is long
            val_text = item["val"]
            if len(val_text) > 48:
                val_text = val_text[:45] + "..."
            svg_lines.append(f'    <text x="0" y="0" class="term-text">')
            svg_lines.append(f'      <tspan fill="{key_col}" class="key">{item["key"]:<10}</tspan>')
            svg_lines.append(f'      <tspan class="sep">:&nbsp;</tspan>')
            svg_lines.append(f'      <tspan class="val">{val_text}</tspan>')
            svg_lines.append(f'    </text>')
        elif item["type"] == "colors":
            swatch_code = ""
            for c_idx, color in enumerate(item["val"]):
                swatch_code += f'<rect x="{c_idx * 24}" y="-10" width="18" height="12" rx="2" fill="{color}" />'
            svg_lines.append(f'    <g transform="translate(0, 0)">{swatch_code}</g>')
            
        svg_lines.append('  </g>')
        
    svg_lines.append('</svg>')
    
    content = "\n".join(svg_lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Successfully generated '{output_path}' (Static mode: {is_static}).")

if __name__ == "__main__":
    make_info_card("info-card.svg")
