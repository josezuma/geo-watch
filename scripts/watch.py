"""
geo-watch — Monitor brand citations in AI model outputs.
SQLite-backed CLI with provider adapters for OpenAI, Anthropic, Perplexity.
"""
import sqlite3
import json
import os
import sys
import argparse
from datetime import datetime

DB_PATH = os.environ.get('GEO_WATCH_DB', os.path.join(os.path.dirname(__file__), '..', 'data', 'watch.db'))

def get_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''
        CREATE TABLE IF NOT EXISTS runs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            provider TEXT NOT NULL,
            prompt_id TEXT NOT NULL,
            prompt_text TEXT NOT NULL,
            response TEXT NOT NULL,
            brands_mentioned TEXT,
            score INTEGER DEFAULT 0
        )
    ''')
    conn.execute('''
        CREATE TABLE IF NOT EXISTS brands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL,
            domain TEXT,
            first_seen TEXT NOT NULL,
            total_mentions INTEGER DEFAULT 0,
            avg_score REAL DEFAULT 0
        )
    ''')
    conn.commit()
    return conn

def record_run(db, provider, prompt_id, prompt_text, response, brands_mentioned, score):
    db.execute(
        'INSERT INTO runs (timestamp, provider, prompt_id, prompt_text, response, brands_mentioned, score) VALUES (?, ?, ?, ?, ?, ?, ?)',
        (datetime.utcnow().isoformat(), provider, prompt_id, prompt_text, response, json.dumps(brands_mentioned), score)
    )
    for brand in brands_mentioned:
        db.execute('''
            INSERT INTO brands (name, first_seen, total_mentions) VALUES (?, ?, 1)
            ON CONFLICT(name) DO UPDATE SET total_mentions = total_mentions + 1
        ''', (brand, datetime.utcnow().isoformat()))
    db.commit()

def export_csv(db, output_path):
    import csv
    rows = db.execute('SELECT timestamp, provider, prompt_id, brands_mentioned, score FROM runs ORDER BY timestamp')
    with open(output_path, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['timestamp', 'provider', 'prompt_id', 'brands_mentioned', 'score'])
        for row in rows:
            writer.writerow(row)
    print(f'Exported to {output_path}')

def render_report(db):
    total = db.execute('SELECT COUNT(*) FROM runs').fetchone()[0]
    brands = db.execute('SELECT name, total_mentions FROM brands ORDER BY total_mentions DESC LIMIT 20').fetchall()
    avg_score = db.execute('SELECT AVG(score) FROM runs WHERE score > 0').fetchone()[0] or 0
    
    print(f'\nGEO Watch Report')
    print('=' * 60)
    print(f'Total runs: {total}')
    print(f'Average score: {avg_score:.1f}/10')
    print('Top brands:')
    for name, count in brands[:10]:
        print(f'  {name}: {count} mentions')
    print()

def main():
    parser = argparse.ArgumentParser(description='GEO Watch — Monitor brand citations in AI outputs')
    parser.add_argument('command', nargs='?', default='report', 
                       choices=['run', 'report', 'export', 'init'])
    parser.add_argument('--provider', default='openai', choices=['openai', 'anthropic', 'perplexity'])
    parser.add_argument('--prompt', help='Prompt to run')
    parser.add_argument('--output', help='Export output path')
    
    args = parser.parse_args()
    db = get_db()
    
    if args.command == 'init':
        print(f'Database initialized at {DB_PATH}')
        
    elif args.command == 'report':
        render_report(db)
        
    elif args.command == 'export':
        export_csv(db, args.output or 'geo-watch-export.csv')
        
    elif args.command == 'run':
        if not args.prompt:
            print('Error: --prompt is required for "run" command')
            sys.exit(1)
        print(f'Running prompt: {args.prompt[:80]}...')
        print(f'Provider: {args.provider}')
        print('(API integration requires API keys in environment)')

if __name__ == '__main__':
    main()
