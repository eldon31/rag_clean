#!/usr/bin/env python3
"""Utility CLI for interacting with the my-knowledge FastMCP server.

This script wraps the FastMCP HTTP client so that common operations like listing
available tools or invoking a specific tool can be performed without manual
Docker commands. It honours standard environment overrides when provided:

- MY_KNOWLEDGE_MCP_URL: base URL of the FastMCP endpoint (default http://localhost:8080/mcp/)
- FASTMCP_LOG_LEVEL: optional log level recognised by FastMCP (forwarded as-is)

Usage examples:
    python scripts/my_knowledge_cli.py list-tools
    python scripts/my_knowledge_cli.py call-tool semantic_search_ultimate \
        --arg query="What is Qdrant?" --arg limit=3

The ``--arg`` flag accepts key=value pairs. Values are parsed as JSON when
possible, otherwise treated as strings.
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
from typing import Any, Dict

from fastmcp import Client

DEFAULT_MCP_URL = os.getenv("MY_KNOWLEDGE_MCP_URL", "http://localhost:8080/mcp/")


def parse_arg(value: str) -> tuple[str, Any]:
    """Parse a key=value pair, coercing JSON values when possible."""
    if "=" not in value:
        raise argparse.ArgumentTypeError("Expected KEY=VALUE format for --arg")

    key, raw = value.split("=", 1)
    try:
        parsed: Any = json.loads(raw)
    except json.JSONDecodeError:
        parsed = raw
    return key, parsed


def build_call_args(pairs: list[tuple[str, Any]]) -> Dict[str, Any]:
    """Construct argument dictionary from parsed key/value pairs."""
    result: Dict[str, Any] = {}
    for key, parsed in pairs:
        result[key] = parsed
    return result


async def list_tools(url: str) -> None:
    async with Client(url) as client:
        tools = await client.list_tools()
        for tool in tools:
            print(f"- {tool.name}: {tool.description}")


async def call_tool(url: str, tool_name: str, call_args: Dict[str, Any]) -> None:
    async with Client(url) as client:
        result = await client.call_tool(tool_name, call_args)
        data = getattr(result, "data", result)
        print(data)


def main() -> int:
    parser = argparse.ArgumentParser(description="Interact with the my-knowledge FastMCP server")
    parser.add_argument("--url", default=DEFAULT_MCP_URL, help=f"FastMCP endpoint (default: {DEFAULT_MCP_URL})")

    subparsers = parser.add_subparsers(dest="command", required=True)

    subparsers.add_parser("list-tools", help="List available FastMCP tools")

    call_parser = subparsers.add_parser("call-tool", help="Invoke a FastMCP tool")
    call_parser.add_argument("tool_name", help="Name of the tool to invoke")
    call_parser.add_argument(
        "--arg",
        dest="args",
        action="append",
        default=[],
        type=parse_arg,
        help="Tool argument expressed as KEY=VALUE. Repeat for multiple arguments.",
    )

    args = parser.parse_args()

    if args.command == "list-tools":
        asyncio.run(list_tools(args.url))
        return 0

    if args.command == "call-tool":
        call_args = build_call_args(args.args)
        asyncio.run(call_tool(args.url, args.tool_name, call_args))
        return 0

    parser.error("Unhandled command")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
