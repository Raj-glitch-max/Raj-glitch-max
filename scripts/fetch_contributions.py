#!/usr/bin/env python3
import sys
import os
import re
import json
from datetime import datetime
import requests
from bs4 import BeautifulSoup

def fetch_contributions(username="Raj-glitch-max", output_path="data/contributions.json"):
    url = f"https://github.com/users/{username}/contributions"
    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"Fetching contribution calendar from '{url}'...")
    res = requests.get(url, headers=headers)
    if res.status_code != 200:
        print(f"Error fetching contributions: HTTP {res.status_code}")
        sys.exit(1)
        
    soup = BeautifulSoup(res.text, "html.parser")
    
    # Map tool-tip elements by 'for' attribute to get exact counts
    tooltips = {t["for"]: t.text.strip() for t in soup.find_all("tool-tip") if t.get("for")}
    
    days_data = []
    calendar_days = soup.find_all("td", class_="ContributionCalendar-day")
    
    for td in calendar_days:
        date_str = td.get("data-date")
        if not date_str:
            continue
            
        level = int(td.get("data-level", 0))
        td_id = td.get("id", "")
        tt_text = tooltips.get(td_id, "")
        
        count = 0
        match = re.search(r'(No|\d+)\s+contribution', tt_text)
        if match:
            count = 0 if match.group(1) == "No" else int(match.group(1))
        else:
            # Fallback estimation based on level if tooltip not present
            count = level * 3 if level > 0 else 0
            
        days_data.append({
            "date": date_str,
            "count": count,
            "level": level
        })
        
    # Sort chronologically by date
    days_data.sort(key=lambda d: d["date"])
    
    if not days_data:
        print("Warning: No day cells found in contribution calendar.")
        
    total_contributions = sum(d["count"] for d in days_data)
    
    # Calculate streaks & best day
    current_streak = 0
    longest_streak = 0
    temp_streak = 0
    best_day = {"date": "", "count": 0}
    monthly_totals = {}
    
    for d in days_data:
        cnt = d["count"]
        dt = d["date"]
        month_key = dt[:7]  # YYYY-MM
        
        # Monthly totals
        monthly_totals[month_key] = monthly_totals.get(month_key, 0) + cnt
        
        # Best day
        if cnt > best_day["count"]:
            best_day = {"date": dt, "count": cnt}
            
        # Streak tracking
        if cnt > 0:
            temp_streak += 1
            if temp_streak > longest_streak:
                longest_streak = temp_streak
        else:
            temp_streak = 0
            
    # Calculate current streak ending today/yesterday
    # Check backwards from last day
    curr = 0
    for d in reversed(days_data):
        if d["count"] > 0:
            curr += 1
        elif curr > 0:
            # Allow skipping today if today's count is 0 but yesterday was active
            break
    current_streak = curr
    
    result = {
        "username": username,
        "updated_at": datetime.now().isoformat(),
        "total_contributions": total_contributions,
        "stats": {
            "current_streak": current_streak,
            "longest_streak": longest_streak,
            "best_day": best_day,
            "monthly_totals": monthly_totals
        },
        "days": days_data
    }
    
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2)
        
    print(f"Saved {len(days_data)} days of contribution data ({total_contributions} total contributions) to '{output_path}'.")

if __name__ == "__main__":
    uname = sys.argv[1] if len(sys.argv) > 1 else "Raj-glitch-max"
    fetch_contributions(uname, "data/contributions.json")
