# Sentinel File Guide - STOP_AFTER_CHUNKING.flag

## What is the Sentinel File?

The sentinel file `STOP_AFTER_CHUNKING.flag` is a safety mechanism that prevents the embedding stage from running automatically after chunking. This is useful when you want to:
- Review chunks before embedding
- Run chunking and embedding separately
- Debug the chunking process
- Control the pipeline flow manually

## Problem

When you see this message:
```
🛑 Embedding stage skipped: sentinel file detected at /kaggle/working/rag_clean/rag_clean/output/STOP_AFTER_CHUNKING.flag. Remove the file to continue the pipeline.
```

The embedding script ([`embed_collections_v4.py`](scripts/embed_collections_v4.py:241)) checks for this file and exits early if found.

## Solutions

### Solution 1: Remove the Sentinel File (Recommended for Kaggle)

**In your Kaggle notebook, run:**

```python
import os
from pathlib import Path

# For Kaggle environment
sentinel_paths = [
    "/kaggle/working/rag_clean/rag_clean/output/STOP_AFTER_CHUNKING.flag",
    "/kaggle/working/output/STOP_AFTER_CHUNKING.flag",
    "output/STOP_AFTER_CHUNKING.flag",
]

for sentinel_path in sentinel_paths:
    if os.path.exists(sentinel_path):
        os.remove(sentinel_path)
        print(f"✓ Removed sentinel file: {sentinel_path}")
        break
else:
    print("No sentinel file found (already removed or doesn't exist)")
```

### Solution 2: Delete via Shell Command

```bash
# In Kaggle notebook cell with ! prefix
!rm -f /kaggle/working/rag_clean/rag_clean/output/STOP_AFTER_CHUNKING.flag
!rm -f /kaggle/working/output/STOP_AFTER_CHUNKING.flag
```

### Solution 3: Modify the Script (Not Recommended)

If you want to disable the sentinel check entirely, comment out lines 241-246 in [`embed_collections_v4.py`](scripts/embed_collections_v4.py:241):

```python
def main(argv: List[str]) -> int:
    # Comment out or remove these lines:
    # if SENTINEL_PATH.exists():
    #     print(
    #         "🛑 Embedding stage skipped: sentinel file detected at "
    #         f"{SENTINEL_PATH}. Remove the file to continue the pipeline."
    #     )
    #     return 0
    
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s %(message)s")
    # ... rest of code
```

## Complete Kaggle Workflow

### Step 1: Check for Sentinel File

```python
import os

sentinel_file = "/kaggle/working/rag_clean/rag_clean/output/STOP_AFTER_CHUNKING.flag"
if os.path.exists(sentinel_file):
    print(f"⚠️  Sentinel file exists: {sentinel_file}")
    print("Embedding will be skipped unless you remove it.")
else:
    print("✓ No sentinel file - embedding can proceed")
```

### Step 2: Remove Sentinel File

```python
import os

sentinel_file = "/kaggle/working/rag_clean/rag_clean/output/STOP_AFTER_CHUNKING.flag"
if os.path.exists(sentinel_file):
    os.remove(sentinel_file)
    print(f"✓ Removed: {sentinel_file}")
```

### Step 3: Run Embedding

```python
from scripts.embed_collections_v4 import main

# Now run the embedding script
result = main([])  # Empty list uses default arguments
if result == 0:
    print("✓ Embedding completed successfully!")
else:
    print("✗ Embedding failed - check logs above")
```

## One-Line Solution (Copy-Paste Ready)

```python
import os; sentinel = "/kaggle/working/rag_clean/rag_clean/output/STOP_AFTER_CHUNKING.flag"; os.path.exists(sentinel) and os.remove(sentinel) and print(f"✓ Removed: {sentinel}") or print("No sentinel file found")
```

## Why Does This File Exist?

The sentinel file is created by the chunking process to give you control over the pipeline. It's particularly useful in Kaggle where:
1. You might want to verify chunks before embedding (costly GPU time)
2. You want to separate chunking (CPU) and embedding (GPU) stages
3. You're debugging and don't want automatic progression
4. You want to review chunking quality before committing to embedding

## Preventing Sentinel File Creation

If you don't want the sentinel file created in the first place, modify your chunking script to not create it. Look for code that creates `STOP_AFTER_CHUNKING.flag` and comment it out.

## Troubleshooting

### "Permission Denied" Error

```python
import os
import stat

sentinel = "/kaggle/working/rag_clean/rag_clean/output/STOP_AFTER_CHUNKING.flag"
if os.path.exists(sentinel):
    # Make file writable
    os.chmod(sentinel, stat.S_IWRITE)
    os.remove(sentinel)
    print(f"✓ Removed (after fixing permissions): {sentinel}")
```

### "File Not Found" but Still Getting Message

The sentinel path might be different. Check all possible locations:

```python
import os
from pathlib import Path

possible_paths = [
    "/kaggle/working/rag_clean/rag_clean/output/STOP_AFTER_CHUNKING.flag",
    "/kaggle/working/rag_clean/output/STOP_AFTER_CHUNKING.flag",
    "/kaggle/working/output/STOP_AFTER_CHUNKING.flag",
    "./output/STOP_AFTER_CHUNKING.flag",
    "../output/STOP_AFTER_CHUNKING.flag",
]

for path in possible_paths:
    if os.path.exists(path):
        print(f"Found sentinel at: {path}")
        os.remove(path)
        print(f"✓ Removed: {path}")
```

## Best Practice for Kaggle

Add this at the start of your embedding notebook cell:

```python
import os

# Auto-remove sentinel file in Kaggle
sentinel_paths = [
    "/kaggle/working/rag_clean/rag_clean/output/STOP_AFTER_CHUNKING.flag",
    "/kaggle/working/output/STOP_AFTER_CHUNKING.flag",
]

for sentinel in sentinel_paths:
    if os.path.exists(sentinel):
        os.remove(sentinel)
        print(f"✓ Removed sentinel file: {sentinel}")

# Now run your embedding code
from scripts.embed_collections_v4 import main
main([])
```

---

**Quick Reference:**
- **Location**: Defined at line 20 in [`embed_collections_v4.py`](scripts/embed_collections_v4.py:20)
- **Check**: Lines 241-246 in [`embed_collections_v4.py`](scripts/embed_collections_v4.py:241)
- **Quick Fix**: `!rm -f /kaggle/working/*/output/STOP_AFTER_CHUNKING.flag`