# Omega-Forge V0 Specification

## Mission

Omega-Forge V0 transforme une specification claire en une file de taches executable, testable et documentee.

V0 doit rester simple, locale et robuste.

## Non-objectifs V0

V0 ne cherche pas encore a etre une IA autonome complete.

V0 ne clone pas automatiquement de gros depots tiers.

V0 ne modifie pas le systeme utilisateur sans trace explicite.

## Boucle cible

```text
SPEC -> PLAN -> TASKS -> EXECUTE -> TEST -> REPORT -> NEXT TASKS
```

## Composants

### Task Queue

Stocke les taches avec :

- id
- title
- description
- status
- priority
- created_at
- updated_at
- history

Statuts :

- pending
- running
- done
- failed
- blocked

### Project State

Stocke l'etat global du projet :

- version
- active goal
- completed tasks
- failed tasks
- generated reports

### Agents

Les agents V0 sont simples et deterministes.

- PlannerAgent : convertit une specification en taches.
- TesterAgent : lance les tests ou simule un controle.
- ReviewerAgent : produit un retour lisible.

### CLI

Commandes minimales :

```bash
python -m omega_forge.cli init
python -m omega_forge.cli plan --spec docs/SPEC_V0.md
python -m omega_forge.cli tasks list
python -m omega_forge.cli tasks add "Titre" --description "..."
python -m omega_forge.cli tasks done TASK_ID
python -m omega_forge.cli report
```

## Critere de reussite V0

V0 est consideree comme utile si elle peut :

1. initialiser un workspace ;
2. generer des taches depuis une spec ;
3. stocker et relire ces taches ;
4. marquer une tache terminee ;
5. produire un rapport ;
6. passer ses tests unitaires.
