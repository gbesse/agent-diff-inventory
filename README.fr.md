# Agent Diff Inventory

**Repérez les fichiers non ignorés changés sur disque par un agent, même si sa revue les omet.**

[English](README.md) · Français · [Español](README.es.md)

## Projets voisins

- [Codex #50202](https://github.com/openai/codex/issues/50202) — Signale des modifications par script absentes d’une vue de revue.
- [Agent Diff Auditor](https://github.com/gaye-lamine/Agent-Diff-Auditor) — Analyse un diff déjà fourni ; cet outil inventorie indépendamment le répertoire avant et après.

## Essayer

```sh
python3 inventory.py demo --lang fr
```

## Utiliser vos données

```sh
python3 inventory.py snapshot --repo /path/to/repo --out /tmp/agent-baseline.json
python3 inventory.py compare --repo /path/to/repo --baseline /tmp/agent-baseline.json --lang fr
```

Prenez un état initial hors du dépôt Git avant l’exécution de l’agent, puis comparez après. Utilise `git ls-files` et SHA-256 pour signaler les fichiers suivis ou non ignorés ajoutés, modifiés et supprimés.

## Périmètre et limites

Intégration Git réelle ; aucune intégration à l’interface Codex. Comparez vous-même cette liste à la revue. Les fichiers ignorés sont exclus. Le JSON contient noms et empreintes de fichiers : gardez-le local.

## Tests

```sh
python3 -m unittest discover -s tests -v
```

Python 3.11+ · MIT · v0.1.0-alpha.1
