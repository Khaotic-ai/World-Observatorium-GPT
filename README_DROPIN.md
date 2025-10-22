
# World Observatorium — Lunar Gate Drop-in (Windows)
Generated: 2025-10-19T02:56:28.517104Z

## Install
1. Unzip into `C:\World-Observatorium-GPT` (allow overwrite).
2. `pip install fastapi uvicorn requests tomli`
3. Run API: `scripts\run_uvicorn.ps1`
4. Expose:  `scripts\run_cloudflared.ps1` → copy printed https URL.
5. Edit `config.toml` BASE to that URL.
6. Test:
   - `python .\observatorium.py | more`
   - `python .\observatorium_report.py`

Notes: Partial outputs mean missing adapters (expected). Wind is m/s; PM2.5 is µg/m³.
