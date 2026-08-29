import json
import os
from datetime import datetime

def generate_basic_svg(stats_data):
    channels = stats_data.get('channels', [])
    sorted_channels = sorted(channels, key=lambda x: x['metrics']['overall_score'], reverse=True)
    
    width = 800
    height = len(sorted_channels) * 50 + 100
    
    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
    <svg width="{width}" height="{height}" version="1.1" xmlns="http://www.w3.org/2000/svg">
    <defs>
        <linearGradient id="grad-green" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#16a34a"/>
            <stop offset="100%" stop-color="#4ade80"/>
        </linearGradient>
        <linearGradient id="grad-yellow" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#ca8a04"/>
            <stop offset="100%" stop-color="#fde047"/>
        </linearGradient>
        <linearGradient id="grad-red" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="#dc2626"/>
            <stop offset="100%" stop-color="#f87171"/>
        </linearGradient>
        <linearGradient id="shimmer" x1="0%" y1="0%" x2="100%" y2="0%">
            <stop offset="0%" stop-color="rgba(255,255,255,0)"/>
            <stop offset="50%" stop-color="rgba(255,255,255,0.4)"/>
            <stop offset="100%" stop-color="rgba(255,255,255,0)"/>
        </linearGradient>
        <filter id="glow" x="-20%" y="-20%" width="140%" height="140%">
            <feGaussianBlur stdDeviation="1.5" result="blur" />
            <feComposite in="SourceGraphic" in2="blur" operator="over" />
        </filter>
    </defs>
    <style>
        .bg-rect {{ fill: #0f172a; }}
        .title {{ font: bold 22px 'Segoe UI', Arial, sans-serif; fill: #f8fafc; }}
        .row {{ font: bold 15px 'Segoe UI', Arial, sans-serif; fill: #38bdf8; filter: url(#glow); }}
        .score {{ font: bold 14px 'Segoe UI', Arial, sans-serif; fill: #f1f5f9; }}
        @keyframes shimmer-anim {{
            0% {{ transform: translateX(-100%); }}
            100% {{ transform: translateX(200%); }}
        }}
        .shimmer-rect {{
            animation: shimmer-anim 2.5s infinite linear;
        }}
    </style>
    <rect width="100%" height="100%" class="bg-rect"/>
    <text x="400" y="45" text-anchor="middle" class="title">Channel Performance Overview</text>'''
    
    for idx, channel in enumerate(sorted_channels):
        y = 80 + (idx * 50)
        name = channel['url'].split('/')[-1]
        score = channel['metrics']['overall_score']
        success = (channel['metrics']['success_count'] / 
                  max(1, channel['metrics']['success_count'] + channel['metrics']['fail_count'])) * 100
        
        bar_width = min(500, 5 * score)
        color_id = 'grad-green' if score >= 70 else 'grad-yellow' if score >= 50 else 'grad-red'
        
        svg += f'''
        <rect x="150" y="{y}" width="500" height="30" fill="#1e293b" rx="6"/>
        <clipPath id="clip-{idx}">
            <rect x="150" y="{y}" width="{bar_width}" height="30" rx="6"/>
        </clipPath>
        <rect x="150" y="{y}" width="{bar_width}" height="30" fill="url(#{color_id})" rx="6"/>
        <g clip-path="url(#clip-{idx})">
            <rect x="150" y="{y}" width="100%" height="30" fill="url(#shimmer)" class="shimmer-rect"/>
        </g>
        <text x="135" y="{y+20}" text-anchor="end" class="row">{name}</text>
        <text x="665" y="{y+20}" text-anchor="start" class="score">{score:.1f}% (S:{success:.0f}%)</text>'''
    
    svg += '</svg>'
    return svg

def _status_meta(score):
    if score >= 70:
        return 'good', 'Healthy'
    if score >= 50:
        return 'warn', 'Degraded'
    if score >= 30:
        return 'risk', 'At Risk'
    return 'bad', 'Disabled Range'

def _build_report_dataset(stats_data):
    channels = stats_data.get('channels', [])
    history = stats_data.get('history', [])
    sorted_channels = sorted(channels, key=lambda x: x['metrics']['overall_score'], reverse=True)

    total_channels = len(channels)
    active_channels = sum(1 for c in channels if c['enabled'])
    total_valid_configs = sum(c['metrics']['valid_configs'] for c in channels)
    total_unique_configs = sum(c['metrics']['unique_configs'] for c in channels)

    avg_score = (sum(c['metrics']['overall_score'] for c in channels) / max(1, total_channels))
    avg_success_rate = (sum((c['metrics']['success_count'] / max(1, c['metrics']['success_count'] + c['metrics']['fail_count'])) * 100 for c in channels) / max(1, total_channels))
    avg_response_time = (sum(c['metrics']['avg_response_time'] for c in channels) / max(1, total_channels))

    protocol_totals = {}
    for c in channels:
        for proto, count in (c['metrics'].get('protocol_counts') or {}).items():
            protocol_totals[proto] = protocol_totals.get(proto, 0) + count

    score_buckets = {'90-100': 0, '70-89': 0, '50-69': 0, '30-49': 0, '0-29': 0}
    for c in channels:
        s = c['metrics']['overall_score']
        if s >= 90:
            score_buckets['90-100'] += 1
        elif s >= 70:
            score_buckets['70-89'] += 1
        elif s >= 50:
            score_buckets['50-69'] += 1
        elif s >= 30:
            score_buckets['30-49'] += 1
        else:
            score_buckets['0-29'] += 1

    responsive_channels = [c for c in channels if c['metrics']['avg_response_time'] > 0]
    fastest = sorted(responsive_channels, key=lambda x: x['metrics']['avg_response_time'])[:12]

    top_performers = sorted_channels[:5]
    bottom_performers = sorted_channels[-5:][::-1] if len(sorted_channels) > 5 else []

    table_rows = []
    for c in sorted_channels:
        success_rate = (c['metrics']['success_count'] / max(1, c['metrics']['success_count'] + c['metrics']['fail_count'])) * 100
        status_class, status_label = _status_meta(c['metrics']['overall_score'])
        table_rows.append({
            'name': c['url'].split('/')[-1] or c['url'],
            'url': c['url'],
            'enabled': c['enabled'],
            'status_class': status_class,
            'status_label': status_label,
            'score': round(c['metrics']['overall_score'], 1),
            'success_rate': round(success_rate, 1),
            'response_time': round(c['metrics']['avg_response_time'], 2),
            'valid_configs': c['metrics']['valid_configs'],
            'total_configs': c['metrics']['total_configs'],
            'unique_configs': c['metrics']['unique_configs'],
            'last_success': c['metrics']['last_success'] or 'Never'
        })

    trend = [{
        'timestamp': h.get('timestamp'),
        'avg_score': h.get('avg_score', 0),
        'total_valid_configs': h.get('total_valid_configs', 0),
        'active_channels': h.get('active_channels', 0)
    } for h in history]

    return {
        'generated_at': stats_data.get('timestamp', 'N/A'),
        'summary': {
            'total_channels': total_channels,
            'active_channels': active_channels,
            'total_valid_configs': total_valid_configs,
            'total_unique_configs': total_unique_configs,
            'avg_score': round(avg_score, 1),
            'avg_success_rate': round(avg_success_rate, 1),
            'avg_response_time': round(avg_response_time, 2)
        },
        'protocol_totals': protocol_totals,
        'score_buckets': score_buckets,
        'fastest': [{'name': c['url'].split('/')[-1] or c['url'], 'response_time': c['metrics']['avg_response_time']} for c in fastest],
        'top_performers': [{'name': c['url'].split('/')[-1] or c['url'], 'score': round(c['metrics']['overall_score'], 1)} for c in top_performers],
        'bottom_performers': [{'name': c['url'].split('/')[-1] or c['url'], 'score': round(c['metrics']['overall_score'], 1)} for c in bottom_performers],
        'table_rows': table_rows,
        'trend': trend
    }

def generate_html_report(stats_data):
    data = _build_report_dataset(stats_data)
    summary = data['summary']
    data_json = json.dumps(data, ensure_ascii=False)

    table_rows_html = ''
    for row in data['table_rows']:
        table_rows_html += f'''
                        <tr class="t-row" data-name="{row['name'].lower()}" data-score="{row['score']}" data-success="{row['success_rate']}" data-response="{row['response_time']}" data-valid="{row['valid_configs']}">
                            <td class="c-name">
                                <span class="dot dot-{row['status_class']}"></span>
                                <span>{row['name']}</span>
                            </td>
                            <td><span class="pill pill-{row['status_class']}">{row['status_label']}</span></td>
                            <td class="mono">{row['score']}%</td>
                            <td class="mono">{row['success_rate']}%</td>
                            <td class="mono">{row['response_time']}s</td>
                            <td class="mono">{row['valid_configs']}/{row['total_configs']}</td>
                            <td class="mono muted">{row['last_success']}</td>
                        </tr>'''

    top_html = ''.join(f'<div class="perf-row"><span class="perf-name">{p["name"]}</span><span class="perf-score good-text">{p["score"]}%</span></div>' for p in data['top_performers'])
    bottom_html = ''.join(f'<div class="perf-row"><span class="perf-name">{p["name"]}</span><span class="perf-score bad-text">{p["score"]}%</span></div>' for p in data['bottom_performers'])

    gauge_score = summary['avg_score']
    gauge_circumference = 2 * 3.14159265 * 80
    gauge_offset = gauge_circumference * (1 - min(100, max(0, gauge_score)) / 100)

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Multi — Source Intelligence Report</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500;600&display=swap" rel="stylesheet">
<script src="https://cdnjs.cloudflare.com/ajax/libs/Chart.js/4.4.4/chart.umd.min.js"></script>
<style>
:root {{
    --bg: #0a0e14;
    --surface: #121826;
    --surface-2: #1a2233;
    --border: #232d40;
    --text: #e6edf7;
    --muted: #8b96ab;
    --accent: #38bdf8;
    --good: #34d399;
    --warn: #fbbf24;
    --risk: #fb923c;
    --bad: #f87171;
    --radius: 14px;
}}
* {{ box-sizing: border-box; }}
body {{
    margin: 0;
    background: radial-gradient(circle at 15% 0%, #101a2e 0%, var(--bg) 45%);
    color: var(--text);
    font-family: 'Inter', system-ui, sans-serif;
    -webkit-font-smoothing: antialiased;
}}
.wrap {{ max-width: 1280px; margin: 0 auto; padding: 28px 20px 60px; }}
h1, h2, h3 {{ font-family: 'Space Grotesk', 'Inter', sans-serif; margin: 0; }}
.mono {{ font-family: 'JetBrains Mono', monospace; font-variant-numeric: tabular-nums; }}
.muted {{ color: var(--muted); }}
header.top {{
    display: flex; align-items: center; justify-content: space-between; flex-wrap: wrap; gap: 16px;
    padding-bottom: 22px; border-bottom: 1px solid var(--border); margin-bottom: 28px;
}}
.brand {{ display: flex; align-items: center; gap: 12px; }}
.pulse {{
    width: 10px; height: 10px; border-radius: 50%; background: var(--good);
    box-shadow: 0 0 0 0 rgba(52,211,153,0.6); animation: pulse 2s infinite;
}}
@keyframes pulse {{
    0% {{ box-shadow: 0 0 0 0 rgba(52,211,153,0.55); }}
    70% {{ box-shadow: 0 0 0 9px rgba(52,211,153,0); }}
    100% {{ box-shadow: 0 0 0 0 rgba(52,211,153,0); }}
}}
@media (prefers-reduced-motion: reduce) {{
    .pulse {{ animation: none; }}
    * {{ scroll-behavior: auto !important; }}
}}
.brand-title {{ font-size: 20px; font-weight: 700; letter-spacing: -0.01em; }}
.brand-sub {{ font-size: 12.5px; color: var(--muted); margin-top: 2px; }}
.links {{ display: flex; gap: 10px; }}
.links a {{
    display: flex; align-items: center; justify-content: center; width: 36px; height: 36px;
    border-radius: 10px; background: var(--surface); border: 1px solid var(--border);
    color: var(--muted); transition: 0.15s ease;
}}
.links a:hover {{ color: var(--accent); border-color: var(--accent); }}
.links svg {{ width: 17px; height: 17px; }}

.hero {{
    display: grid; grid-template-columns: 220px 1fr; gap: 28px; align-items: center;
    background: linear-gradient(150deg, var(--surface) 0%, var(--surface-2) 100%);
    border: 1px solid var(--border); border-radius: var(--radius); padding: 28px; margin-bottom: 24px;
}}
.gauge-wrap {{ display: flex; align-items: center; justify-content: center; position: relative; }}
.gauge-num {{ position: absolute; text-align: center; }}
.gauge-num .val {{ font-family: 'Space Grotesk', sans-serif; font-size: 34px; font-weight: 700; }}
.gauge-num .lbl {{ font-size: 11px; color: var(--muted); text-transform: uppercase; letter-spacing: 0.08em; margin-top: 2px; }}
.stat-grid {{ display: grid; grid-template-columns: repeat(4, 1fr); gap: 14px; }}
.stat-card {{ background: rgba(255,255,255,0.02); border: 1px solid var(--border); border-radius: 10px; padding: 14px 16px; }}
.stat-card .n {{ font-family: 'Space Grotesk', sans-serif; font-size: 24px; font-weight: 700; }}
.stat-card .l {{ font-size: 12px; color: var(--muted); margin-top: 4px; }}

.grid-2 {{ display: grid; grid-template-columns: 1.3fr 1fr; gap: 20px; margin-bottom: 20px; }}
.grid-3 {{ display: grid; grid-template-columns: repeat(3, 1fr); gap: 20px; margin-bottom: 20px; }}
@media (max-width: 900px) {{
    .hero {{ grid-template-columns: 1fr; }}
    .stat-grid {{ grid-template-columns: repeat(2, 1fr); }}
    .grid-2, .grid-3 {{ grid-template-columns: 1fr; }}
}}

.card {{
    background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 20px;
}}
.card h3 {{ font-size: 15px; font-weight: 600; margin-bottom: 14px; }}
.card .chart-box {{ position: relative; height: 220px; }}

.perf-row {{ display: flex; justify-content: space-between; padding: 8px 0; border-bottom: 1px solid var(--border); font-size: 13.5px; }}
.perf-row:last-child {{ border-bottom: none; }}
.perf-name {{ color: var(--text); }}
.good-text {{ color: var(--good); font-family: 'JetBrains Mono', monospace; }}
.bad-text {{ color: var(--bad); font-family: 'JetBrains Mono', monospace; }}

.table-card {{ background: var(--surface); border: 1px solid var(--border); border-radius: var(--radius); padding: 20px; }}
.table-top {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 16px; flex-wrap: wrap; gap: 12px; }}
#search {{
    background: var(--surface-2); border: 1px solid var(--border); color: var(--text);
    padding: 9px 14px; border-radius: 8px; font-size: 13.5px; width: 260px; outline: none;
}}
#search:focus {{ border-color: var(--accent); }}
.table-scroll {{ overflow-x: auto; }}
table {{ width: 100%; border-collapse: collapse; font-size: 13.5px; }}
th {{
    text-align: left; padding: 10px 12px; color: var(--muted); font-weight: 600; font-size: 11.5px;
    text-transform: uppercase; letter-spacing: 0.05em; border-bottom: 1px solid var(--border); cursor: pointer; user-select: none;
    white-space: nowrap;
}}
th:hover {{ color: var(--accent); }}
th.sorted::after {{ content: ' ↓'; }}
th.sorted.asc::after {{ content: ' ↑'; }}
td {{ padding: 10px 12px; border-bottom: 1px solid var(--border); white-space: nowrap; }}
.c-name {{ display: flex; align-items: center; gap: 9px; }}
.dot {{ width: 8px; height: 8px; border-radius: 50%; flex-shrink: 0; }}
.dot-good {{ background: var(--good); }}
.dot-warn {{ background: var(--warn); }}
.dot-risk {{ background: var(--risk); }}
.dot-bad {{ background: var(--bad); }}
.pill {{ font-size: 11px; padding: 3px 9px; border-radius: 20px; font-weight: 600; }}
.pill-good {{ background: rgba(52,211,153,0.14); color: var(--good); }}
.pill-warn {{ background: rgba(251,191,36,0.14); color: var(--warn); }}
.pill-risk {{ background: rgba(251,146,60,0.14); color: var(--risk); }}
.pill-bad {{ background: rgba(248,113,113,0.14); color: var(--bad); }}
.legend-note {{ font-size: 11.5px; color: var(--muted); margin-top: 14px; }}

footer {{ margin-top: 32px; text-align: center; color: var(--muted); font-size: 12.5px; }}
footer a {{ color: var(--accent); text-decoration: none; }}
.empty {{ text-align: center; padding: 60px 20px; color: var(--muted); }}
</style>
</head>
<body>
<div class="wrap">
    <header class="top">
        <div class="brand">
            <span class="pulse"></span>
            <div>
                <div class="brand-title">Multi — Source Intelligence Report</div>
                <div class="brand-sub mono">Last run: {data['generated_at']}</div>
            </div>
        </div>
        <div class="links">
            <a href="https://github.com/4n0nymou3" target="_blank" title="GitHub Profile"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/></svg></a>
            <a href="https://github.com/4n0nymou3/multi-proxy-config-fetcher" target="_blank" title="Repository"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M4 4a2 2 0 012-2h10.5A1.5 1.5 0 0118 3.5V21l-6-3-6 3V6a2 2 0 00-2-2z"/></svg></a>
            <a href="https://x.com/4n0nymou3" target="_blank" title="X (Twitter)"><svg viewBox="0 0 24 24" fill="currentColor"><path d="M18.244 2.25h3.308l-7.227 8.26 8.502 11.24H16.17l-5.214-6.817L4.99 21.75H1.68l7.73-8.835L1.254 2.25H8.08l4.713 6.231zm-1.161 17.52h1.833L7.084 4.126H5.117z"/></svg></a>
        </div>
    </header>

    <div class="hero">
        <div class="gauge-wrap">
            <svg width="180" height="180" viewBox="0 0 180 180">
                <circle cx="90" cy="90" r="80" fill="none" stroke="var(--surface-2)" stroke-width="14"/>
                <circle id="gauge-ring" cx="90" cy="90" r="80" fill="none" stroke="var(--accent)" stroke-width="14"
                    stroke-linecap="round" transform="rotate(-90 90 90)"
                    stroke-dasharray="{gauge_circumference:.2f}" stroke-dashoffset="{gauge_circumference:.2f}"
                    data-target-offset="{gauge_offset:.2f}"/>
            </svg>
            <div class="gauge-num">
                <div class="val mono" id="gauge-value">0%</div>
                <div class="lbl">Avg Health</div>
            </div>
        </div>
        <div class="stat-grid">
            <div class="stat-card"><div class="n">{summary['active_channels']}<span class="muted" style="font-size:15px"> / {summary['total_channels']}</span></div><div class="l">Active Sources</div></div>
            <div class="stat-card"><div class="n mono">{summary['total_valid_configs']}</div><div class="l">Valid Configs Fetched</div></div>
            <div class="stat-card"><div class="n mono">{summary['total_unique_configs']}</div><div class="l">Unique Configs</div></div>
            <div class="stat-card"><div class="n mono">{summary['avg_response_time']}s</div><div class="l">Avg Response Time</div></div>
        </div>
    </div>

    <div class="grid-3">
        <div class="card">
            <h3>Protocol Distribution</h3>
            <div class="chart-box"><canvas id="chart-protocol"></canvas></div>
        </div>
        <div class="card">
            <h3>Source Health Distribution</h3>
            <div class="chart-box"><canvas id="chart-score"></canvas></div>
            <div class="legend-note">Sources scoring under 30% are auto-disabled by the pipeline.</div>
        </div>
        <div class="card">
            <h3>Fastest Sources (avg response)</h3>
            <div class="chart-box"><canvas id="chart-speed"></canvas></div>
        </div>
    </div>

    <div class="grid-2">
        <div class="card">
            <h3>Health Score Trend</h3>
            <div class="chart-box" id="trend-box"><canvas id="chart-trend"></canvas></div>
        </div>
        <div class="card">
            <h3>Top &amp; Bottom Performers</h3>
            <div style="margin-bottom:14px">{top_html or '<div class="perf-row muted">No data yet</div>'}</div>
            <div style="border-top:1px dashed var(--border);padding-top:10px">{bottom_html or ''}</div>
        </div>
    </div>

    <div class="table-card">
        <div class="table-top">
            <h3>All Sources</h3>
            <input id="search" type="text" placeholder="Search sources...">
        </div>
        <div class="table-scroll">
            <table id="main-table">
                <thead>
                    <tr>
                        <th data-key="name">Source</th>
                        <th data-key="status_class">Status</th>
                        <th data-key="score" class="sorted">Score</th>
                        <th data-key="success">Success Rate</th>
                        <th data-key="response">Response</th>
                        <th data-key="valid">Valid/Total</th>
                        <th>Last Success</th>
                    </tr>
                </thead>
                <tbody>{table_rows_html}
                </tbody>
            </table>
        </div>
    </div>

    <footer>
        Generated automatically by <a href="https://github.com/4n0nymou3/multi-proxy-config-fetcher" target="_blank">multi-proxy-config-fetcher</a> · Made with 💚 by Anonymous
    </footer>
</div>
<script>
const REPORT_DATA = {data_json};

(function() {{
    const ring = document.getElementById('gauge-ring');
    const valueEl = document.getElementById('gauge-value');
    const target = parseFloat(ring.dataset.targetOffset);
    const total = parseFloat(ring.getAttribute('stroke-dasharray'));
    const finalScore = {gauge_score};
    const reduced = window.matchMedia('(prefers-reduced-motion: reduce)').matches;
    const duration = reduced ? 0 : 900;
    const start = performance.now();
    function frame(now) {{
        const p = duration === 0 ? 1 : Math.min(1, (now - start) / duration);
        ring.setAttribute('stroke-dashoffset', total - (total - target) * p);
        valueEl.textContent = (finalScore * p).toFixed(1) + '%';
        if (p < 1) requestAnimationFrame(frame);
    }}
    requestAnimationFrame(frame);
}})();

Chart.defaults.color = '#8b96ab';
Chart.defaults.font.family = "'Inter', sans-serif";
Chart.defaults.borderColor = '#232d40';

const protoEntries = Object.entries(REPORT_DATA.protocol_totals).sort((a,b) => b[1]-a[1]);
new Chart(document.getElementById('chart-protocol'), {{
    type: 'doughnut',
    data: {{
        labels: protoEntries.map(e => e[0].replace('://','')),
        datasets: [{{
            data: protoEntries.map(e => e[1]),
            backgroundColor: ['#38bdf8','#34d399','#fbbf24','#fb923c','#f87171','#a78bfa','#f472b6'],
            borderColor: '#121826',
            borderWidth: 2
        }}]
    }},
    options: {{ maintainAspectRatio: false, plugins: {{ legend: {{ position: 'bottom', labels: {{ boxWidth: 10, padding: 10, font: {{ size: 11 }} }} }} }} }}
}});

const buckets = REPORT_DATA.score_buckets;
new Chart(document.getElementById('chart-score'), {{
    type: 'bar',
    data: {{
        labels: Object.keys(buckets),
        datasets: [{{
            data: Object.values(buckets),
            backgroundColor: ['#34d399','#38bdf8','#fbbf24','#fb923c','#f87171'],
            borderRadius: 6,
            maxBarThickness: 34
        }}]
    }},
    options: {{ maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }}, scales: {{ y: {{ beginAtZero: true, ticks: {{ precision: 0 }}, grid: {{ color: '#1a2233' }} }}, x: {{ grid: {{ display: false }} }} }} }}
}});

const fastest = REPORT_DATA.fastest;
new Chart(document.getElementById('chart-speed'), {{
    type: 'bar',
    data: {{
        labels: fastest.map(f => f.name.length > 16 ? f.name.slice(0,16)+'…' : f.name),
        datasets: [{{
            data: fastest.map(f => f.response_time),
            backgroundColor: '#38bdf8',
            borderRadius: 6,
            maxBarThickness: 16
        }}]
    }},
    options: {{
        indexAxis: 'y', maintainAspectRatio: false, plugins: {{ legend: {{ display: false }} }},
        scales: {{ x: {{ grid: {{ color: '#1a2233' }} }}, y: {{ grid: {{ display: false }}, ticks: {{ font: {{ size: 10.5 }} }} }} }}
    }}
}});

const trend = REPORT_DATA.trend;
if (trend.length >= 2) {{
    new Chart(document.getElementById('chart-trend'), {{
        type: 'line',
        data: {{
            labels: trend.map(t => new Date(t.timestamp).toLocaleString(undefined, {{month:'short', day:'numeric', hour:'2-digit', minute:'2-digit'}})),
            datasets: [
                {{ label: 'Avg Score', data: trend.map(t => t.avg_score), borderColor: '#38bdf8', backgroundColor: 'rgba(56,189,248,0.12)', fill: true, tension: 0.35, yAxisID: 'y' }},
                {{ label: 'Valid Configs', data: trend.map(t => t.total_valid_configs), borderColor: '#34d399', backgroundColor: 'transparent', tension: 0.35, yAxisID: 'y1' }}
            ]
        }},
        options: {{
            maintainAspectRatio: false,
            plugins: {{ legend: {{ position: 'bottom', labels: {{ boxWidth: 10, font: {{ size: 11 }} }} }} }},
            scales: {{
                y: {{ position: 'left', grid: {{ color: '#1a2233' }} }},
                y1: {{ position: 'right', grid: {{ display: false }} }},
                x: {{ grid: {{ display: false }}, ticks: {{ maxRotation: 0, font: {{ size: 10 }} }} }}
            }}
        }}
    }});
}} else {{
    document.getElementById('trend-box').innerHTML = '<div class="empty">Trend needs at least 2 runs of history. Check back after the next scheduled run.</div>';
}}

const table = document.getElementById('main-table');
const tbody = table.querySelector('tbody');
const searchInput = document.getElementById('search');
searchInput.addEventListener('input', () => {{
    const q = searchInput.value.toLowerCase();
    tbody.querySelectorAll('.t-row').forEach(row => {{
        row.style.display = row.dataset.name.includes(q) ? '' : 'none';
    }});
}});

let currentSort = {{ key: 'score', asc: false }};
table.querySelectorAll('th[data-key]').forEach(th => {{
    th.addEventListener('click', () => {{
        const key = th.dataset.key;
        const asc = currentSort.key === key ? !currentSort.asc : false;
        currentSort = {{ key, asc }};
        table.querySelectorAll('th[data-key]').forEach(h => h.classList.remove('sorted','asc'));
        th.classList.add('sorted');
        if (asc) th.classList.add('asc');
        const rows = Array.from(tbody.querySelectorAll('.t-row'));
        const attrMap = {{ name: 'name', status_class: 'name', score: 'score', success: 'success', response: 'response', valid: 'valid' }};
        rows.sort((a, b) => {{
            const attr = attrMap[key] || key;
            let av = a.dataset[attr], bv = b.dataset[attr];
            if (!isNaN(parseFloat(av)) && key !== 'name') {{ av = parseFloat(av); bv = parseFloat(bv); }}
            if (av < bv) return asc ? -1 : 1;
            if (av > bv) return asc ? 1 : -1;
            return 0;
        }});
        rows.forEach(r => tbody.appendChild(r));
    }});
}});
</script>
</body>
</html>'''
    
    return html

def main():
    try:
        with open('configs/channel_stats.json', 'r') as f:
            stats_data = json.load(f)
        
        if not stats_data:
            stats_data = {"channels": [], "timestamp": datetime.now().isoformat()}

        os.makedirs('assets', exist_ok=True)
        
        svg_content = generate_basic_svg(stats_data)
        with open('assets/channel_stats_chart.svg', 'w', encoding='utf-8') as f:
            f.write(svg_content)
        
        html_content = generate_html_report(stats_data)
        with open('assets/performance_report.html', 'w', encoding='utf-8') as f:
            f.write(html_content)
        
        print("Successfully generated chart and report!")
        
    except FileNotFoundError:
        print("Error: configs/channel_stats.json not found. Skipping chart generation.")
    except Exception as e:
        print(f"Error generating outputs: {str(e)}")

if __name__ == '__main__':
    main()