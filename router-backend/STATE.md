# STATE
PROJECT: LLM Cost Optimizer — backend
LAST PHASE COMPLETED: P0
NEXT PHASE: P1
MODE: mock (no API keys anywhere)
FILES THAT EXIST AND WORK:
- requirements.txt
FILES NOT WRITTEN YET:
- config.py, models.py, benchmark.json, classifier.py,
cache.py, router.py, judge.py, store.py, main.py
DECISIONS ALREADY LOCKED (do not revisit):
- Python + FastAPI + sqlite3 + in-memory dict cache
- Two tiers: "cheap" and "frontier"
- Cheap: $0.25 per 1M input, $1.25 per 1M output
- Frontier: $3.00 per 1M input, $15.00 per 1M output
- Cached input tokens billed at 10% of input price
- Tokens estimated as len(text) // 4
- Routing threshold default 0.45
- 50 benchmark queries: 30 easy, 20 hard
- Judge scores 1-5 by word overlap with reference answer
CURRENT BLOCKER: non

## Folder structure 
router-backend
- venv
- benchmark.json
- cache.py
- classifier.py
- config.py
- judge.py
- main.py
- models.py
- requirements.txt
- router.py
- STATE.md
- store.py



