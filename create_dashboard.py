#!/usr/bin/env python3
"""
Create Integrated Dashboard with Report Embedded
Run this after completing the notebook analysis to create a unified dashboard
"""

import json
import base64
from pathlib import Path
import markdown

# Paths
OUTPUT_DIR = Path("./output")
report_file = OUTPUT_DIR / 'gap_analysis_report.md'
dashboard_file = OUTPUT_DIR / 'gap_analysis_dashboard.html'

# Find all layer files
layer_files = {
    '🔥 Composite Threat': OUTPUT_DIR / 'composite_threat.json',
    '🛡️ Coverage': OUTPUT_DIR / 'coverage.json',
    '📊 Gap Analysis': OUTPUT_DIR / 'gap_analysis.json',
}

# Add actor layers
for layer_path in OUTPUT_DIR.glob('actor_*.json'):
    layer_name = layer_path.stem.replace('actor_', '').replace('_', ' ')
    layer_files[f'👥 {layer_name.title()}'] = layer_path

# Read and convert markdown report
report_html = ""
if report_file.exists():
    with open(report_file, 'r') as f:
        md_content = f.read()
    report_html = markdown.markdown(md_content, extensions=['tables'])
else:
    report_html = "<p><em>Report not found. Run the notebook first.</em></p>"

# Load all layers
all_layers = []
layer_tags = []
download_links = []

for tab_name, layer_path in layer_files.items():
    if not layer_path.exists():
        continue

    with open(layer_path, 'r') as f:
        layer_json = json.load(f)

    all_layers.append(layer_json)
    technique_count = len(layer_json.get('techniques', []))

    layer_tags.append(f'''
    <div class="layer-tag">
        <h4>{tab_name}</h4>
        <div class="stats">📊 {technique_count} techniques</div>
    </div>
    ''')

    download_links.append(f'<a href="{layer_path.name}" download="{layer_path.name}" class="btn-small">{layer_path.name}</a>')

# Add CSV data export link if it exists
csv_file = OUTPUT_DIR / 'complete_ttp_data.csv'
if csv_file.exists():
    download_links.append(f'<a href="{csv_file.name}" download="{csv_file.name}" class="btn-small" style="background: #28a745;">📊 {csv_file.name}</a>')

# Create Navigator URL
all_layers_json = json.dumps(all_layers)
all_layers_b64 = base64.b64encode(all_layers_json.encode('utf-8')).decode('utf-8')
navigator_url = f"https://mitre-attack.github.io/attack-navigator/#layerURL=data:application/json;base64,{all_layers_b64}"

# HTML Template
html = f"""<!DOCTYPE html>
<html>
<head>
    <title>ATT&CK Gap Analysis - Dashboard</title>
    <style>
        * {{ box-sizing: border-box; }}
        body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background: #f5f5f5; }}
        .container {{ max-width: 1400px; margin: 0 auto; padding: 30px; }}
        .header {{
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white; padding: 30px; border-radius: 12px;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1); margin-bottom: 30px;
        }}
        .header h1 {{ margin: 0 0 10px 0; }}
        .header p {{ margin: 5px 0; opacity: 0.9; }}
        .card {{ background: white; padding: 30px; border-radius: 12px; box-shadow: 0 2px 8px rgba(0,0,0,0.1); margin-bottom: 30px; }}
        .card h2 {{ margin: 0 0 20px 0; color: #333; }}
        .btn-large {{
            display: inline-block; padding: 16px 32px; background: #007bff; color: white;
            text-decoration: none; border-radius: 8px; font-weight: 600; font-size: 18px;
            transition: all 0.2s; box-shadow: 0 2px 4px rgba(0,123,255,0.3);
        }}
        .btn-large:hover {{ background: #0056b3; transform: translateY(-2px); box-shadow: 0 4px 8px rgba(0,123,255,0.4); }}
        .layer-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(250px, 1fr)); gap: 15px; margin-top: 20px; }}
        .layer-tag {{ padding: 12px 16px; background: #f8f9fa; border-left: 4px solid #007bff; border-radius: 4px; }}
        .layer-tag h4 {{ margin: 0 0 5px 0; font-size: 14px; color: #333; }}
        .layer-tag .stats {{ font-size: 12px; color: #888; }}
        .report-section {{
            background: white; padding: 40px; border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1); line-height: 1.6;
        }}
        .report-section h1 {{ color: #333; border-bottom: 3px solid #007bff; padding-bottom: 10px; }}
        .report-section h2 {{ color: #555; margin-top: 30px; }}
        .report-section h3 {{ color: #666; margin-top: 20px; }}
        .report-section table {{ border-collapse: collapse; width: 100%; margin: 20px 0; font-size: 14px; }}
        .report-section th, .report-section td {{ border: 1px solid #ddd; padding: 12px 8px; text-align: left; }}
        .report-section th {{ background: #007bff; color: white; font-weight: 600; }}
        .report-section tr:nth-child(even) {{ background: #f8f9fa; }}
        .instructions {{
            background: #e7f3ff; border-left: 4px solid #007bff; padding: 20px;
            border-radius: 8px; margin: 20px 0;
        }}
        .instructions h3 {{ margin: 0 0 10px 0; color: #004085; }}
        .instructions ul {{ margin: 10px 0; padding-left: 20px; color: #004085; }}
        .download-links {{ margin-top: 20px; padding: 15px; background: #f8f9fa; border-radius: 8px; }}
        .download-links h4 {{ margin: 0 0 10px 0; color: #333; }}
        .btn-small {{
            display: inline-block; padding: 8px 16px; background: #6c757d; color: white;
            text-decoration: none; border-radius: 6px; font-size: 14px; margin: 5px 5px 5px 0;
            transition: background 0.2s;
        }}
        .btn-small:hover {{ background: #545b62; }}
        .footer {{ text-align: center; color: #888; font-size: 14px; margin-top: 40px; padding: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>🎯 ATT&CK Gap Analysis Dashboard</h1>
            <p>Comprehensive threat-informed defense gap analysis</p>
            <p><strong>One-stop shop:</strong> Navigator layers, analysis report, and downloads</p>
        </div>

        <div class="card">
            <h2>🚀 Interactive Navigator</h2>
            <p style="color: #666; margin-bottom: 20px;">
                Open all {len(all_layers)} layers as tabs in ATT&CK Navigator for interactive analysis
            </p>
            <a href="{navigator_url}" target="_blank" class="btn-large">
                Open Multi-Layer Navigator
            </a>

            <div class="instructions">
                <h3>💡 Navigator Features</h3>
                <ul>
                    <li>Switch between layers using tabs at the top</li>
                    <li>Use "Create Layer from other layers" to combine/compare</li>
                    <li>Filter by tactics, platforms, or search terms</li>
                    <li>Export customized views for reports</li>
                </ul>
            </div>

            <div class="layer-grid">
                {''.join(layer_tags)}
            </div>

            <div class="download-links">
                <h4>💾 Download Files</h4>
                <p style="margin-bottom: 15px; color: #666; font-size: 14px;">
                    Download Navigator JSON files to manually upload or the complete TTP data CSV for analysis in Excel/Google Sheets:
                </p>
                {''.join(download_links)}
            </div>
        </div>

        <div class="report-section">
            {report_html}
        </div>

        <div class="footer">
            <p>Generated by ATT&CK Gap Analysis Framework</p>
            <p>Powered by MITRE ATT&CK® | <a href="https://attack.mitre.org" target="_blank">attack.mitre.org</a></p>
        </div>
    </div>
</body>
</html>
"""

# Write dashboard
with open(dashboard_file, 'w') as f:
    f.write(html)

print(f"✅ Integrated dashboard created!")
print(f"📁 Location: {dashboard_file.absolute()}")
print(f"\n🌐 Open in browser: file://{dashboard_file.absolute()}")
print(f"\n💡 This dashboard includes:")
print(f"   • Multi-layer Navigator link (all layers as tabs)")
print(f"   • Complete gap analysis report embedded")
print(f"   • Download links for all layer JSON files")
if csv_file.exists():
    print(f"   • Download link for complete TTP data CSV")
print(f"   • Print-friendly format")
