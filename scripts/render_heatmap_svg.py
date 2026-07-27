#!/usr/bin/env python3
import sys
import os
import json
from datetime import datetime

PALETTE = [
    "#161b22",  # 0: none
    "#0e4429",  # 1: dark green
    "#006d32",  # 2: medium green
    "#26a641",  # 3: bright green
    "#39d353",  # 4: vivid green
    "#69f0a0"   # 5: neon top end
]

def render_heatmap_svg(json_path="data/contributions.json", output_path="contrib-heatmap.svg"):
    if not os.path.exists(json_path):
        print(f"Error: JSON file '{json_path}' not found. Run fetch_contributions.py first.")
        sys.exit(1)
        
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        
    days = data.get("days", [])
    total = data.get("total_contributions", sum(d["count"] for d in days))
    
    # SVG Dimensions
    svg_width = 860
    svg_height = 195
    
    # Grid positioning
    grid_x = 48
    grid_y = 52
    cell_size = 10
    cell_gap = 3
    stride = cell_size + cell_gap
    
    # Organise days into weeks (53 weeks max)
    weeks = []
    current_week = []
    
    # Process days chronologically
    for d in days:
        dt = datetime.strptime(d["date"], "%Y-%m-%d")
        # Python weekday: Mon=0 .. Sun=6 -> Convert to Sun=0 .. Sat=6
        wday = (dt.weekday() + 1) % 7
        
        # If starting a new week (Sunday) and current_week is not empty
        if wday == 0 and current_week:
            weeks.append(current_week)
            current_week = []
            
        current_week.append({
            "date": d["date"],
            "count": d["count"],
            "level": d["level"],
            "wday": wday,
            "month": dt.strftime("%b"),
            "dt": dt
        })
        
    if current_week:
        weeks.append(current_week)
        
    # Limit to 53 weeks
    weeks = weeks[-53:]
    
    # SVG header & style
    svg_lines = []
    svg_lines.append(f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {svg_width} {svg_height}" width="{svg_width}" height="{svg_height}">')
    svg_lines.append('  <style>')
    svg_lines.append('    .bg { fill: #0d1117; rx: 6px; stroke: #30363d; stroke-width: 1px; }')
    svg_lines.append('    .title { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 11px; fill: #8b949e; font-weight: 600; }')
    svg_lines.append('    .label { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 9px; fill: #7d8590; }')
    svg_lines.append('    .stat-text { font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Helvetica, Arial, sans-serif; font-size: 11px; fill: #8b949e; font-weight: 500; }')
    svg_lines.append('    .stat-bold { fill: #c9d1d9; font-weight: 600; }')
    svg_lines.append('    @keyframes diagReveal {')
    svg_lines.append('      0% { opacity: 0; transform: translateY(-8px) scale(0.85); }')
    svg_lines.append('      100% { opacity: 1; transform: translateY(0) scale(1.0); }')
    svg_lines.append('    }')
    svg_lines.append('    .cell { animation: diagReveal 0.35s cubic-bezier(0.16, 1, 0.3, 1) forwards; transform-origin: center; }')
    svg_lines.append('  </style>')
    
    # Outer frame
    svg_lines.append(f'  <rect width="{svg_width}" height="{svg_height}" class="bg" />')
    
    # Window dots & title bar
    svg_lines.append('  <circle cx="16" cy="16" r="4.5" fill="#ff5f56" />')
    svg_lines.append('  <circle cx="28" cy="16" r="4.5" fill="#ffbd2e" />')
    svg_lines.append('  <circle cx="40" cy="16" r="4.5" fill="#27c93f" />')
    svg_lines.append('  <text x="56" y="19" class="title">avi@github ~ $ ./contributions.sh</text>')
    
    # Day labels (Mon=1, Wed=3, Fri=5)
    day_labels = [(1, "Mon"), (3, "Wed"), (5, "Fri")]
    for wday_idx, label in day_labels:
        lbl_y = grid_y + (wday_idx * stride) + 8
        svg_lines.append(f'  <text x="{grid_x - 10}" y="{lbl_y}" class="label" text-anchor="end">{label}</text>')
        
    # Month labels along the top
    last_month = ""
    for w_idx, week in enumerate(weeks):
        if not week:
            continue
        first_day_month = week[0]["month"]
        if first_day_month != last_month:
            lbl_x = grid_x + (w_idx * stride)
            svg_lines.append(f'  <text x="{lbl_x}" y="{grid_y - 8}" class="label">{first_day_month}</text>')
            last_month = first_day_month
            
    # Render 53x7 Grid Cells
    svg_lines.append('  <g>')
    for w_idx, week in enumerate(weeks):
        x_pos = grid_x + (w_idx * stride)
        for day_item in week:
            wday = day_item["wday"]
            y_pos = grid_y + (wday * stride)
            cnt = day_item["count"]
            lvl = day_item["level"]
            
            # Map level (0..4, or 5 for top end)
            if cnt >= 25:
                color_idx = 5
            elif lvl in (0, 1, 2, 3, 4):
                color_idx = lvl
            else:
                color_idx = 0
                
            color = PALETTE[color_idx]
            
            # Diagonal reveal delay: (w_idx + wday)
            diag_idx = w_idx + wday
            delay_sec = diag_idx * 0.012
            
            tooltip_str = f"{cnt} contribution{'s' if cnt != 1 else ''} on {day_item['date']}"
            
            svg_lines.append(
                f'    <rect x="{x_pos}" y="{y_pos}" width="{cell_size}" height="{cell_size}" rx="2.5" ry="2.5" '
                f'fill="{color}" class="cell" style="opacity: 0; animation-delay: {delay_sec:.3f}s;">'
                f'<title>{tooltip_str}</title></rect>'
            )
    svg_lines.append('  </g>')
    
    # Footer Stats (Left) & Legend (Right)
    footer_y = grid_y + (7 * stride) + 22
    formatted_total = f"{total:,}"
    svg_lines.append(f'  <text x="{grid_x}" y="{footer_y}" class="stat-text"><tspan class="stat-bold">{formatted_total}</tspan> contributions in the last year</text>')
    
    # Legend
    legend_right_x = svg_width - 24
    legend_start_x = legend_right_x - (len(PALETTE) * (cell_size + 3)) - 50
    
    svg_lines.append(f'  <g transform="translate({legend_start_x}, {footer_y - 9})">')
    svg_lines.append('    <text x="0" y="8" class="label">Less</text>')
    for idx, col in enumerate(PALETTE):
        lx = 28 + (idx * (cell_size + 3))
        svg_lines.append(f'    <rect x="{lx}" y="0" width="{cell_size}" height="{cell_size}" rx="2" fill="{col}" />')
    leg_more_x = 28 + (len(PALETTE) * (cell_size + 3)) + 4
    svg_lines.append(f'    <text x="{leg_more_x}" y="8" class="label">More</text>')
    svg_lines.append('  </g>')
    
    svg_lines.append('</svg>')
    
    content = "\n".join(svg_lines)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"Successfully generated '{output_path}' ({total:,} contributions, {len(weeks)} weeks).")

if __name__ == "__main__":
    jpath = sys.argv[1] if len(sys.argv) > 1 else "data/contributions.json"
    render_heatmap_svg(jpath, "contrib-heatmap.svg")
