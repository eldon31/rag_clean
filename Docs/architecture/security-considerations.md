# Security Considerations

- Ensure queries logged in telemetry are truncated/anonymized per existing privacy rules.
- When writing rerank/sparse artifacts, avoid storing full query text if privacy compliance requires redaction.
- Validate CLI inputs (Pydantic or argparse) to prevent invalid model selections causing unsafe downloads.
