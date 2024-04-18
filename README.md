# dbt's `pre-commit` hooks

This repository hosts dbt's `pre-commit` hooks.

To use a hook, add an entry in your `.pre-commit-config.yaml` that looks like this:
```yaml
repos:
-   repo: https://github.com/dbt-labs/pre-commit-hooks
    rev: v0.1.0
    hooks:
    -   id: dbt-core-check
```
