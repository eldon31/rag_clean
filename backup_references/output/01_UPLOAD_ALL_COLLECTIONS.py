#!/usr/bin/env python3
"""
Master script to upload all collections sequentially
Runs all upload scripts in the correct order
"""

import subprocess
import sys
import logging
from pathlib import Path

# Setup logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_upload_script(script_path: Path):
    """Run an upload script and check for errors"""
    logger.info(f"\n{'='*60}")
    logger.info(f"Running: {script_path.name}")
    logger.info(f"{'='*60}\n")
    
    result = subprocess.run(
        [sys.executable, str(script_path)],
        capture_output=False,
        text=True
    )
    
    if result.returncode != 0:
        logger.error(f"❌ Failed to run {script_path.name}")
        return False
    
    logger.info(f"✅ Completed: {script_path.name}\n")
    return True

def main():
    """Upload all collections"""
    
    # Get script directory
    script_dir = Path(__file__).parent
    
    # Define upload scripts in order
    upload_scripts = [
        script_dir / "Docling_v4_outputs" / "Docling_v4_upload_script.py",
        script_dir / "FAST_DOCS_v4_outputs" / "FAST_DOCS_v4_upload_script.py",
        script_dir / "pydantic_pydantic_v4_outputs" / "pydantic_pydantic_v4_upload_script.py",
        script_dir / "Qdrant_v4_outputs" / "Qdrant_v4_upload_script.py",
        script_dir / "Sentence_Transformers_v4_outputs" / "Sentence_Transformers_v4_upload_script.py"
    ]
    
    # Check all scripts exist
    missing = [s for s in upload_scripts if not s.exists()]
    if missing:
        logger.error("❌ Missing upload scripts:")
        for s in missing:
            logger.error(f"   - {s}")
        sys.exit(1)
    
    logger.info("🚀 Starting sequential upload of all collections...")
    logger.info(f"📊 Total collections to upload: {len(upload_scripts)}\n")
    
    # Run each script
    success_count = 0
    failed_scripts = []
    
    for script_path in upload_scripts:
        if run_upload_script(script_path):
            success_count += 1
        else:
            failed_scripts.append(script_path.name)
    
    # Summary
    logger.info("\n" + "="*60)
    logger.info("UPLOAD SUMMARY")
    logger.info("="*60)
    logger.info(f"✅ Successful: {success_count}/{len(upload_scripts)}")
    
    if failed_scripts:
        logger.error(f"❌ Failed: {len(failed_scripts)}")
        for name in failed_scripts:
            logger.error(f"   - {name}")
        sys.exit(1)
    else:
        logger.info("🎉 All collections uploaded successfully!")

if __name__ == "__main__":
    main()
