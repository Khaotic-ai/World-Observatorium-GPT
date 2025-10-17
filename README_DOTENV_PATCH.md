
# 🌍 World-Observatorium-GPT: Dotenv Integration Patch

This patch enables automatic environment variable loading from a local `.env` file.

## Files
- `.env.example` — template for environment variables
- `dotenv_patch.py` — snippet for orchestrator/app.py
- `requirements_append.txt` — append to your requirements.txt

## Steps
1. Copy `.env.example` → `.env`
2. Add your key inside `.env`:
   ```bash
   NASA_API_KEY=phRrR5fLiKSwsWt32jlLfKqo3q7khXqm51BXUnfC
   ```
3. Add to `orchestrator/app.py` near the top:
   ```python
   from dotenv import load_dotenv
   load_dotenv()
   ```
4. Append to requirements:
   ```bash
   echo "python-dotenv" >> requirements.txt
   ```
5. Run locally:
   ```bash
   uvicorn orchestrator.app:app --reload
   ```

✅ Your app will now securely detect and use environment variables like `NASA_API_KEY`.
