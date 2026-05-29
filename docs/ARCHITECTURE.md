# Omega-Forge Architecture

Omega-Forge est organise autour d'une boucle de developpement controlee.

```text
SPEC -> PLAN -> TASK QUEUE -> AGENTS -> TESTS -> REPORT -> NEXT TASKS
```

## Principes

1. Chaque etape doit produire une trace.
2. Chaque agent doit avoir une responsabilite limitee.
3. Le code genere doit etre testable.
4. Les integrations externes doivent passer par des adaptateurs.
5. Les depots tiers doivent rester separes du coeur Omega-Forge.

## Arborescence cible V0

```text
omega_forge/
  core/
    task_queue.py
    project_state.py
    memory.py
    report.py
  agents/
    base.py
    planner.py
    tester.py
    reviewer.py
  cli.py
```

## Core

### Task Queue

Responsable de la creation, de la persistance et du suivi des taches.

### Project State

Responsable de l'etat global du projet : objectif actif, version, compteurs, historique.

### Memory

Memoire V0 tres simple, basee sur un fichier JSON.

### Report

Generation d'un rapport Markdown lisible.

## Agents

### BaseAgent

Classe commune avec nom, role et methode `run`.

### PlannerAgent

Transforme une specification Markdown en taches initiales.

### TesterAgent

Lance ou simule un controle de test.

### ReviewerAgent

Produit une revue humaine lisible.

## CLI

Le CLI est l'entree principale V0.

Commandes prevues :

```bash
python -m omega_forge.cli init
python -m omega_forge.cli plan --spec docs/SPEC_V0.md
python -m omega_forge.cli tasks list
python -m omega_forge.cli tasks add "Titre" --description "..."
python -m omega_forge.cli tasks done TASK_ID
python -m omega_forge.cli report
```

## Integration open-source

Les projets tiers doivent etre integres selon cet ordre de preference :

1. dependance package officielle ;
2. adaptateur interne ;
3. sous-module Git ;
4. copie vendoree uniquement si necessaire et conforme licence.

## Regle anti-derive

Omega-Forge ne doit jamais modifier un fichier sans produire :

- une raison ;
- une tache associee ;
- un rapport ;
- si possible, un test.
