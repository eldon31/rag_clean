# Qdrant Deployment Preparation - Manual Steps

## STEP 1: Start Docker Desktop
1. Open Docker Desktop application
2. Wait for it to fully start (icon turns green)
3. Verify it's running

## STEP 2: Start Qdrant
Run ONE of these commands:

### Option A: Using docker-compose (Recommended)
```powershell
docker-compose up -d
```

### Option B: Using docker run
```powershell
docker run -d -p 6333:6333 -p 6334:6334 -v qdrant_storage:/qdrant/storage --name qdrant qdrant/qdrant:latest
```

## STEP 3: Verify Qdrant is Running
Open in browser: http://localhost:6333/dashboard

## STEP 4: Delete All Collections (Fresh Start)
```powershell
python scripts/reset_qdrant.py
```

## STEP 5: Ready for Deployment!

### What's Next:
1. **Wait** for Kaggle embedding to complete (~1-1.5 min with data parallelism)
2. **Download** from Kaggle:
   - `docling_embeddings.jsonl`
   - `docling_embedding_summary.json`
3. **Place** files in: `output/docling/embeddings/`
4. **Upload** to Qdrant:
   ```powershell
   python scripts/upload_to_qdrant.py
   ```

## Troubleshooting

### Docker not found
- Start Docker Desktop manually
- Wait 30 seconds for it to initialize

### Qdrant not responding
```powershell
# Check if container is running
docker ps

# Restart if needed
docker restart qdrant

# Check logs
docker logs qdrant
```

### Port already in use
```powershell
# Stop existing Qdrant
docker stop qdrant
docker rm qdrant

# Start fresh
docker-compose up -d
```
