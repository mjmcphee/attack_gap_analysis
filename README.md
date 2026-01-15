# ATT&CK Gap Analysis Framework

A comprehensive Jupyter Notebook-based tool for automated MITRE ATT&CK gap analysis. This tool helps security teams identify coverage gaps by comparing their threat landscape against their detection capabilities.

## Overview

This framework enables organizations to:

1. **Ingest threat data** from multiple sources (MITRE groups, custom Navigator layers, parsed threat intel)
2. **Weight and aggregate** threats based on organizational priorities
3. **Map detection coverage** using DeTTECT framework
4. **Calculate gaps** between threats and coverage
5. **Generate multi-layered ATT&CK Navigator visualizations** with interactive HTML
6. **Produce detailed reports** with prioritized recommendations

## Features

- **Multi-Source Threat Intelligence**: Load threats from MITRE ATT&CK groups, custom Navigator layers, or parsed threat reports
- **Weighted Threat Composition**: Combine multiple threat actors with organizational weights
- **DeTTECT Integration**: Load existing detection coverage from DeTTECT YAML files
- **Automated Gap Analysis**: Calculate coverage gaps using threat vs. detection scoring
- **Interactive Visualization**: Multi-tab Navigator with composite threat, coverage, and gap layers
- **Actionable Reports**: Markdown and HTML reports with prioritized recommendations

## Installation

### Prerequisites

- Python 3.8 or higher
- Jupyter Notebook
- Git (optional, for cloning)

### Setup

1. Clone or download this repository:
```bash
git clone <repository-url>
cd attack_gap_analysis
```

2. Launch Jupyter Notebook:
```bash
jupyter notebook attack_gap_analysis.ipynb
```

**That's it!** The notebook will automatically install all required dependencies when you run Cell 1.

### Alternative: Manual Installation

If you prefer to install dependencies manually (or the auto-install fails):

```bash
pip install -r requirements.txt
```

Or use a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

**Note:** The optional `attack_parser.py` tool (for parsing threat reports) is automatically downloaded when you run the notebook. Dependencies (beautifulsoup4, lxml, requests) are auto-installed by Cell 1.

## Quick Start

1. **Launch Jupyter Notebook**:
```bash
jupyter notebook attack_gap_analysis.ipynb
```

2. **(Optional) Select ATT&CK Version** (Cell 1):
   - Default is version 18 (latest)
   - Edit `ATTACK_VERSION = "18"` to use a different version (10-18)
   - Restart kernel after changing: `Kernel → Restart & Run All`

3. **Configure Threat Actors** (Cell 8):
   - Edit the `THREAT_ACTORS` configuration
   - Add MITRE groups, custom layers, or threat intel URLs
   - Adjust weights based on organizational priorities (0.0 to 1.0)

4. **Add Coverage Data**:
   - Place your DeTTECT YAML file in `./data/dettect_coverage.yaml`
   - Or use the auto-generated sample file for testing

5. **Run All Cells**:
   - In Jupyter: `Kernel → Restart & Run All`
   - The notebook will execute end-to-end

6. **View Results**:
   - Open `output/gap_analysis_navigator.html` in your browser
   - Read `output/gap_analysis_report.md` for detailed findings

## Usage

### Basic Workflow

The notebook follows this structure:

1. **Setup** (Cells 1-3): Environment configuration and utilities
2. **Data Ingestion** (Cells 4-6): Load MITRE data and Navigator layers
3. **Optional Tools** (Cell 6a): Auto-download attack_parser.py for threat report parsing
4. **Parser Integration** (Cell 7): Initialize attack_parser wrapper
5. **Threat Configuration** (Cells 8-10): Configure threat actors and calculate composite threat
6. **Coverage & Gaps** (Cells 11-12): Load DeTTECT coverage and calculate gaps
7. **Output Generation** (Cells 13-14): Create Navigator visualizations and reports
8. **Summary** (Cell 15): Review outputs and next steps

### Configuring Threat Actors

Edit Cell 8 to customize your threat landscape:

```python
THREAT_ACTORS = [
    {
        'name': 'APT29 (Cozy Bear)',
        'source': 'mitre',
        'identifier': 'G0016',  # MITRE group ID
        'weight': 0.8,
        'description': 'Russian state-sponsored threat actor'
    },
    {
        'name': 'Custom Ransomware Profile',
        'source': 'file',
        'identifier': './layers/ransomware_2024.json',
        'weight': 1.0,
        'description': 'Custom ransomware profile'
    },
    {
        'name': 'Recent CISA Alert',
        'source': 'parsed',
        'identifier': 'https://www.cisa.gov/news-events/cybersecurity-advisories',
        'weight': 0.7,
        'description': 'Parsed from recent advisory'
    }
]
```

### Threat Actor Sources

**MITRE Groups** (`source: 'mitre'`):
- Use any MITRE ATT&CK group ID (e.g., G0016, G0046)
- See Cell 5 output for full list of available groups
- Techniques are automatically loaded from MITRE CTI data

**Custom Layers** (`source: 'file'`):
- Load existing ATT&CK Navigator JSON layers
- Place layer files in `./layers/` directory
- Useful for saved threat profiles or custom threat models

**Parsed Intelligence** (`source: 'parsed'`) - **OPTIONAL**:
- Extracts ATT&CK techniques from threat reports (blogs, advisories, PDFs)
- **Auto-installed** by the notebook (Block 6a downloads it automatically)
- If auto-download fails, manual download: https://github.com/mjmcphee/attack_parser
- Dependencies (requests, beautifulsoup4) already included in requirements.txt
- If not needed, comment out any `'parsed'` threat actors in Block 8

### DeTTECT Coverage

Place your DeTTECT YAML file at `./data/dettect_coverage.yaml`:

```yaml
version: 1.0
name: Organization Coverage
platform: Windows
techniques:
  - technique_id: T1566.001
    visibility:
      - score: 3
    detection:
      - score: 2
  - technique_id: T1059.001
    visibility:
      - score: 4
    detection:
      - score: 3
```

If no file exists, a sample file is auto-generated for demonstration.

## Scoring System

### Threat Scoring (1-5 scale)
- **5**: Signature technique, frequently observed
- **3**: Moderately used
- **1**: Rarely used by this actor

### Coverage Scoring (1-5 scale)
- **5**: Full automated detection with response
- **3**: Manual detection capability
- **1**: Minimal visibility, no detection

### Gap Scoring (-10 to +10 scale)

```
gap_score = (weighted_threat_score - coverage_score) * 2.5
```

**Interpretation:**
- **+10 to +5**: Critical gap (high threat, low coverage)
- **+5 to +2.5**: High priority gap
- **+2.5 to 0**: Medium priority gap
- **0 to -2.5**: Adequate coverage
- **-2.5 to -10**: Over-covered (more coverage than threat warrants)

## Output Files

After execution, the following files are generated in `./output/`:

### Navigator Layers (JSON)
- `composite_threat.json` - Weighted composite threat landscape
- `coverage.json` - Detection coverage map
- `gap_analysis.json` - Gap visualization
- `actor_0_<name>.json`, etc. - Individual threat actor layers

### Interactive Visualization
- `gap_analysis_navigator.html` - Multi-tab Navigator with all layers

### Reports
- `gap_analysis_report.md` - Comprehensive markdown report
- `gap_analysis_report.html` - HTML version (if markdown library installed)

### Supporting Files
- `available_groups.csv` - List of all MITRE threat groups

## Project Structure

```
attack_gap_analysis/
├── attack_gap_analysis.ipynb    # Main Jupyter notebook
├── requirements.txt              # Python dependencies
├── README.md                     # This file
├── data/                         # Input data directory
│   └── dettect_coverage.yaml    # DeTTECT coverage file
├── layers/                       # Custom Navigator layers
├── output/                       # Generated outputs
│   ├── *.json                   # Navigator layer files
│   ├── gap_analysis_navigator.html
│   └── gap_analysis_report.md
└── .gitignore
```

## Troubleshooting

### Common Issues

**Issue**: Block 9 fails with "attack_parser.py not found" when using parsed sources
- **Cause**: Auto-download in Block 6a may have failed due to network issues
- **Solution**:
  1. Check Block 6a output for download errors
  2. Re-run Block 6a to retry download
  3. Or manually download from https://github.com/mjmcphee/attack_parser
  4. Place in project root: `/home/parallels/Desktop/gap_analysis/attack_parser.py`
  5. OR comment out any threat actors with `'source': 'parsed'` in Block 8

**Issue**: Block output shows ATT&CK Version 17 after updating to 18
- **Cause**: Jupyter kernel caches variables from previous runs
- **Solution**: Click **Kernel → Restart & Run All** to clear cached variables

**Issue**: ATT&CK data fails to download
- **Solution**: Check internet connection; data will be cached locally after first download

**Issue**: DeTTECT file not found
- **Solution**: Sample file auto-generates; edit `data/dettect_coverage.yaml` with your coverage

**Issue**: Navigator layers won't load in browser
- **Solution**: Use a modern browser (Chrome, Firefox, Edge); ensure files are in `output/` directory

**Issue**: Empty gap analysis
- **Solution**: Ensure DeTTECT coverage data includes techniques from your threat actors

### Debug Tips

- Check Cell outputs for error messages
- Verify file paths are correct (use absolute paths if needed)
- Review logs for warnings about missing data
- Ensure all dependencies are installed: `pip install -r requirements.txt`

## Configuration Options

### Cell 1: ATT&CK Version Selection

```python
# Change this to use a different version of MITRE ATT&CK
# Available versions: 10, 11, 12, 13, 14, 15, 16, 17, 18
# Latest: 18 (as of January 2026)
ATTACK_VERSION = "18"
```

**Important:** After changing the ATT&CK version:
1. Save the notebook
2. Click **Kernel → Restart & Run All** to clear cached variables
3. The new version will be downloaded and cached in `./data/`

**Why choose a different version?**
- **Consistency:** Match your organization's existing ATT&CK-based tools
- **Stability:** Use a well-tested version for production analysis
- **Comparison:** Run analyses across different versions to track coverage evolution

### Cell 8: Threat Actor Weights

Adjust weights based on:
- Recent threat intelligence
- Industry-specific threats
- Geographic targeting
- Historical incidents

Higher weights (0.8-1.0) = greater organizational concern
Lower weights (0.3-0.5) = monitoring/awareness only

## Advanced Usage

### Custom Color Gradients

Edit Cell 2 to customize Navigator colors:

```python
GRADIENTS = {
    'threat': {
        'colors': ['#ffffff00', '#ff0000'],  # Transparent to Red
        'minValue': 1,
        'maxValue': 5
    }
}
```

### Batch Processing Multiple Configurations

Run the notebook programmatically with different configs:

```python
import papermill as pm

pm.execute_notebook(
    'attack_gap_analysis.ipynb',
    'output_notebook.ipynb',
    parameters={'THREAT_ACTORS': custom_config}
)
```

### Integration with CI/CD

Schedule periodic gap analysis updates:

```bash
# Cron job example (weekly)
0 0 * * 0 cd /path/to/attack_gap_analysis && jupyter nbconvert --execute --to notebook attack_gap_analysis.ipynb
```

## Best Practices

1. **Update Regularly**: Re-run analysis quarterly or after infrastructure changes
2. **Validate Coverage**: Ensure DeTTECT data reflects actual detection capabilities
3. **Prioritize Actionable Gaps**: Focus on techniques with gap scores > 5
4. **Track Over Time**: Save outputs with timestamps to monitor improvement
5. **Share with Stakeholders**: Use HTML outputs for presentations

## Contributing

Contributions welcome! Areas for enhancement:
- Additional threat intelligence sources
- Automated DeTTECT YAML generation
- Technique difficulty/cost estimation
- SIEM/EDR integration
- Excel export with formatting

## Resources

- **MITRE ATT&CK**: https://attack.mitre.org/
- **ATT&CK Navigator**: https://github.com/mitre-attack/attack-navigator
- **DeTTECT Framework**: https://github.com/rabobank-cdc/DeTTECT
- **attack_parser**: https://github.com/mjmcphee/attack_parser

## License

This project is provided as-is for security analysis and detection engineering purposes.

## Support

For issues, questions, or enhancements:
- Open an issue on GitHub
- Review the troubleshooting section
- Check MITRE ATT&CK documentation

---

**Version**: 1.0
**ATT&CK Version**: 18
**Last Updated**: 2026-01-13
