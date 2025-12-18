# The Blood Ledger

A narrative game engine set in Norman England, 1067.

## Launch Protocol

Start all services in separate terminals:

### 1. FalkorDB (Graph Database)
```bash
docker start falkordb
# Or if first time:
# docker run -d --name falkordb -p 6379:6379 -p 3002:3000 falkordb/falkordb
```
- Built-in browser: http://localhost:3002

### 2. Backend (FastAPI)
```bash
cd engine
python3 run.py --reload
```
- Runs on: http://localhost:8000

### 3. Frontend (Next.js)
```bash
cd frontend
npm run dev
```
- Runs on: http://localhost:3000

### 4. FalkorDB Browser
The built-in browser runs automatically with FalkorDB at http://localhost:3002

Alternative (standalone browser):
```bash
cd falkordb-browser
PORT=3001 npm run dev
```

## Moment Graph Sample Data

Seed a minimal camp conversation into FalkorDB for local testing:

```bash
python engine/scripts/seed_moment_sample.py \
  --graph blood_ledger \
  --db-host localhost \
  --db-port 6379 \
  --sample data/samples/moment_sample.yaml
```

After seeding, request `GET /api/view/{playthrough_id}?player_id=char_player` to see the Moment Graph response (location resolves automatically from the player's `AT` relationship).

> Note: GraphOps expects character nodes to use `type: character` with a `character_type` attribute (`player`, `companion`, `major`, `minor`, `background`). The sample file already follows this convention.

## Service Summary

| Service | Port | Purpose |
|---------|------|---------|
| Frontend | 3000 | Game UI |
| Backend | 8000 | API server |
| FalkorDB | 6379 | Graph database |
| FalkorDB Browser (built-in) | 3002 | Graph visualization |
