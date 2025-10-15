pytest tests/ -m "not slow"  # Fast tests only
pytest tests/ -m "slow"      # Slow tests only