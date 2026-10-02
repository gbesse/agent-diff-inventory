# Agent Diff Inventory

**Detecte archivos no ignorados que cambió un agente en disco, aunque su panel de revisión los omita.**

[English](README.md) · [Français](README.fr.md) · Español

## Proyectos relacionados

- [Codex #50202](https://github.com/openai/codex/issues/50202) — Informa de cambios hechos por scripts que faltan en una vista de revisión.
- [Agent Diff Auditor](https://github.com/gaye-lamine/Agent-Diff-Auditor) — Analiza un diff ya aportado; esta herramienta inventaría el árbol de trabajo antes y después.

## Probar

```sh
python3 inventory.py demo --lang es
```

## Usar sus datos

```sh
python3 inventory.py snapshot --repo /path/to/repo --out /tmp/agent-baseline.json
python3 inventory.py compare --repo /path/to/repo --baseline /tmp/agent-baseline.json --lang es
```

Guarde una línea base fuera del árbol Git antes del agente y compárela después. Usa `git ls-files` y SHA-256 para informar de archivos seguidos o no ignorados añadidos, modificados y eliminados.

## Alcance y límites

Integración real con Git; sin integración con la interfaz de Codex. Compare la lista con el panel usted mismo. Se excluyen archivos ignorados. El JSON contiene nombres y hashes: consérvelo localmente.

## Pruebas

```sh
python3 -m unittest discover -s tests -v
```

Python 3.11+ · MIT · v0.1.0-alpha.1
