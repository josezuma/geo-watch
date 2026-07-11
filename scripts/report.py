#!/usr/bin/env python3
"""Summarize GEO watch results into a human-readable markdown report."""
import json, sqlite3, os, sys
from datetime import datetime

DB_PATH = os.environ.get('GEO_WATCH_DB', os.path.join(os.path.dirname(__file__), '..', 'data', 'watch.db'))

def generate_report(output_path='geo-report.md'):
    conn = sqlite3.connect(DB_PATH)
    total = conn.execute('SELECT COUNT(*) FROM runs').fetchone()[0]
    brands = conn.execute('SELECT name, total_mentions FROM brands ORDER BY total_mentions DESC').fetchall()
    recent = conn.execute('SELECT timestamp, provider, prompt_id, brands_mentioned FROM runs ORDER BY timestamp DESC LIMIT 10').fetchall()
    conn.close()
    
    lines = [f"# GEO Watch Report — {datetime.utcnow().isoformat()[:10]}", "",
             f"**Total runs:** {total}", "",
             "## Top Brands", "| Brand | Mentions |", "|-------|----------|"]
    for name, count in brands[:20]:
        lines.append(f"| {name} | {count} |")
    
    lines.extend(["", "## Recent Runs", "| Time | Provider | Prompt | Brands |",
                  "|------|----------|--------|--------|"])
    for ts, prov, pid, brands_str in recent:
        lines.append(f"| {ts[:16]} | {prov} | {pid[:30]}... | {brands_str[:40]} |")
    
    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))
    print(f'Report written to {output_path}')

if __name__ == '__main__':
    generate_report(sys.argv[1] if len(sys.argv) > 1 else 'geo-report.md')
