#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
SIMPLE FASTAPI APP - No lifespan, no complex initialization
"""

from fastapi import FastAPI

app = FastAPI(
    title="Simple FastAPI Test",
    description="Testing basic FastAPI functionality",
    version="1.0.0"
)

@app.get("/api/health")
async def health():
    return {"status": "healthy", "message": "Simple FastAPI test"}

@app.get("/")
async def root():
    return {"message": "Hello World"}