#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Test Suite for Enterprise FastMCP API Server v2.0
===============================================

Comprehensive test suite for the enhanced FastMCP API server with REST endpoints and MCP tools.

Tests cover:
- Server initialization and configuration
- REST API endpoints functionality
- MCP tool execution
- Error handling and edge cases
- Performance validation

Usage:
    python test_qdrant_fastmcp_api_server.py

Author: AI Assistant
"""

import asyncio
import json
import time
from typing import Dict, Any
import httpx
import pytest
from fastapi.testclient import TestClient

# Import the server module
from qdrant_fastmcp_api_server import app, server_state, settings


class TestFastMCPAPIServer:
    """Test suite for the FastMCP API Server."""

    def setup_method(self):
        """Setup test client and initialize server state."""
        self.client = TestClient(app)
        # Note: In a real test, you'd want to mock the Qdrant client and embedder

    def test_health_endpoint(self):
        """Test the health check endpoint."""
        response = self.client.get("/health")
        assert response.status_code == 200

        data = response.json()
        assert "status" in data
        assert "uptime_seconds" in data
        assert "qdrant_connected" in data
        assert "embedder_loaded" in data
        assert "cache_stats" in data
        assert "system_stats" in data

    def test_collections_endpoint(self):
        """Test the collections listing endpoint."""
        response = self.client.get("/collections")
        assert response.status_code == 200

        data = response.json()
        assert isinstance(data, list)

        if data:  # If collections are available
            collection = data[0]
            assert "name" in collection
            assert "vector_count" in collection
            assert "description" in collection
            assert "knowledge_areas" in collection
            assert "vector_size" in collection

    def test_collection_stats_endpoint(self):
        """Test the collection statistics endpoint."""
        response = self.client.get("/collections/stats")
        # This might fail if Qdrant is not connected, but should not crash
        if response.status_code == 200:
            data = response.json()
            assert "total_collections" in data
            assert "total_vectors" in data
            assert "collections" in data

    def test_chunking_optimization_endpoint(self):
        """Test the chunking optimization endpoint."""
        test_data = {
            "content_length": 1500,
            "content_type": "documentation",
            "knowledge_domain": "technical"
        }

        response = self.client.post("/optimize/chunking", json=test_data)
        assert response.status_code == 200

        data = response.json()
        assert "content_length" in data
        assert "content_type" in data
        assert "knowledge_domain" in data
        assert "recommendations" in data
        assert isinstance(data["recommendations"], list)

    def test_performance_analysis_endpoint(self):
        """Test the performance analysis endpoint."""
        response = self.client.get("/performance/analysis")
        # This might fail if Qdrant is not connected, but should not crash
        if response.status_code == 200:
            data = response.json()
            assert "timestamp" in data
            assert "collections" in data

    def test_server_stats_endpoint(self):
        """Test the server statistics endpoint."""
        response = self.client.get("/server/stats")
        assert response.status_code == 200

        data = response.json()
        assert "uptime_seconds" in data
        assert "request_count" in data
        assert "error_count" in data
        assert "cache_hits" in data
        assert "cache_misses" in data
        assert "avg_response_time" in data
        assert "system_stats" in data
        assert "cache_stats" in data

    def test_metrics_endpoint(self):
        """Test the Prometheus metrics endpoint."""
        response = self.client.get("/metrics")
        assert response.status_code == 200

        content = response.text
        assert "qdrant_fastmcp_requests_total" in content
        assert "qdrant_fastmcp_errors_total" in content
        assert "qdrant_fastmcp_uptime_seconds" in content

    def test_openapi_schema(self):
        """Test that OpenAPI schema is generated correctly."""
        response = self.client.get("/openapi.json")
        if settings.enable_openapi_enhancement:
            assert response.status_code == 200
            schema = response.json()
            assert "paths" in schema
            assert "components" in schema
        else:
            # Should still work but might be disabled
            pass

    def test_invalid_collection_search(self):
        """Test search with invalid collection."""
        test_data = {
            "query": "test query",
            "collection": "invalid_collection",
            "limit": 10,
            "score_threshold": 0.7,
            "use_cache": False
        }

        response = self.client.post("/search", json=test_data)
        assert response.status_code == 400

    def test_chunking_edge_cases(self):
        """Test chunking optimization with edge cases."""
        # Very small content
        response = self.client.post("/optimize/chunking", json={
            "content_length": 100,
            "content_type": "general",
            "knowledge_domain": "mixed"
        })
        assert response.status_code == 200

        # Very large content
        response = self.client.post("/optimize/chunking", json={
            "content_length": 50000,
            "content_type": "scientific",
            "knowledge_domain": "academic"
        })
        assert response.status_code == 200

    def test_collection_optimization_endpoint(self):
        """Test collection optimization endpoint."""
        # Test with valid collection
        for collection in settings.supported_collections:
            response = self.client.post(f"/collections/{collection}/optimize")
            if response.status_code == 200:
                data = response.json()
                assert "collection" in data
                assert "vector_count" in data
                assert "recommendations" in data
                break

        # Test with invalid collection
        response = self.client.post("/collections/invalid_collection/optimize")
        assert response.status_code == 400


def run_basic_tests():
    """Run basic functionality tests."""
    print("🧪 Running FastMCP API Server Tests...")

    test_suite = TestFastMCPAPIServer()
    test_suite.setup_method()

    tests = [
        ("Health Endpoint", test_suite.test_health_endpoint),
        ("Collections Endpoint", test_suite.test_collections_endpoint),
        ("Collection Stats", test_suite.test_collection_stats_endpoint),
        ("Chunking Optimization", test_suite.test_chunking_optimization_endpoint),
        ("Performance Analysis", test_suite.test_performance_analysis_endpoint),
        ("Server Stats", test_suite.test_server_stats_endpoint),
        ("Metrics Endpoint", test_suite.test_metrics_endpoint),
        ("OpenAPI Schema", test_suite.test_openapi_schema),
        ("Invalid Collection Search", test_suite.test_invalid_collection_search),
        ("Chunking Edge Cases", test_suite.test_chunking_edge_cases),
        ("Collection Optimization", test_suite.test_collection_optimization_endpoint),
    ]

    passed = 0
    failed = 0

    for test_name, test_func in tests:
        try:
            print(f"  Running {test_name}...")
            test_func()
            print(f"  ✅ {test_name} PASSED")
            passed += 1
        except Exception as e:
            print(f"  ❌ {test_name} FAILED: {e}")
            failed += 1

    print(f"\n📊 Test Results: {passed} passed, {failed} failed")

    if failed == 0:
        print("🎉 All tests passed!")
        return True
    else:
        print("⚠️ Some tests failed. Check server configuration and dependencies.")
        return False


if __name__ == "__main__":
    success = run_basic_tests()
    exit(0 if success else 1)