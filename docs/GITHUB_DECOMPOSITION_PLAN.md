# GitHub Decomposition Plan

Objectif : decomposer les depots open-source candidats sans les cloner massivement ni fragiliser Omega-Forge.

## Regle principale

On ne copie pas un depot entier par reflexe.

Pour chaque projet, Omega-Forge doit identifier :

- la licence ;
- la valeur utile ;
- les modules ou idees reutilisables ;
- le mode d'integration ideal ;
- les risques techniques ;
- les risques juridiques ;
- les taches a creer.

## Modes d'integration

1. Dependence officielle via package manager.
2. Adaptateur Omega-Forge.
3. Sous-module Git.
4. Vendorisation selective.
5. Reference documentaire uniquement.

## Priorites initiales

### 1. Aider

Usage vise : agent codeur local assiste par LLM.

Integration preferee : dependance ou adaptateur CLI.

Taches :

- verifier licence actuelle ;
- identifier interface CLI minimale ;
- definir un AiderAdapter ;
- tester sur un repo jouet ;
- documenter les limites.

### 2. OpenHands

Usage vise : environnement agent developpeur plus complet.

Integration preferee : reference + adaptateur, pas copie complete au debut.

Taches :

- verifier licence actuelle ;
- identifier modules sandbox/execution ;
- etudier structure agent ;
- comparer avec besoin Omega-Forge ;
- decider integration ou non.

### 3. LangGraph

Usage vise : orchestration de workflows agents sous forme de graphes.

Integration preferee : dependance officielle.

Taches :

- verifier licence ;
- creer un prototype workflow Planner -> Coder -> Tester -> Reviewer ;
- definir checkpointing ;
- documenter la migration depuis agents deterministes V0.

### 4. GraphRAG

Usage vise : memoire documentaire et graphe de connaissance.

Integration preferee : dependance ou inspiration architecturale.

Taches :

- verifier licence ;
- identifier format d'index ;
- tester ingestion docs Omega-Forge ;
- definir KnowledgeAdapter.

### 5. Qdrant

Usage vise : memoire vectorielle haute performance.

Integration preferee : dependance/service externe optionnel.

Taches :

- verifier licence ;
- definir VectorMemoryAdapter ;
- creer mode local/offline ;
- documenter installation.

### 6. LlamaIndex

Usage vise : ingestion documentaire et retrieval.

Integration preferee : dependance officielle.

Taches :

- verifier licence ;
- tester ingestion docs ;
- comparer avec GraphRAG ;
- definir role exact.

### 7. React Flow

Usage vise : visualisation de graphes de taches et d'agents.

Integration preferee : dependance frontend.

Taches :

- verifier licence ;
- definir schema des noeuds ;
- creer prototype UI graphe ;
- connecter aux taches Omega-Forge.

### 8. Tauri

Usage vise : application desktop locale legere.

Integration preferee : shell desktop futur, pas V0.

Taches :

- verifier licence ;
- definir besoin desktop ;
- comparer web local vs desktop ;
- planifier integration V2/V3.

## Sortie attendue de cette decomposition

Chaque depot doit produire un lot de taches Omega-Forge :

```text
repo -> analyse -> decision -> adapter -> tests -> docs
```

## Principe anti-chaos

Aucun depot tiers ne doit entrer dans `core/`.

Les integrations externes vont dans :

```text
adapters/
vendor/
third_party/
```

Le coeur Omega-Forge doit rester petit, lisible et testable.
