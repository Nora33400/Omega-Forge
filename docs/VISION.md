# Omega-Forge Vision

Omega-Forge est une forge de développement autonome contrôlée.

Son objectif n'est pas de remplacer l'humain, mais d'augmenter sa capacité à transformer une intuition en système réel, traçable et améliorable.

## Idée centrale

Omega-Forge suit une boucle simple :

```text
SPEC -> PLAN -> TASK QUEUE -> CODE -> TEST -> REVIEW -> REPORT -> NEXT TASK
```

Chaque étape doit être lisible, journalisée et réversible.

## Pourquoi ce projet existe

Les projets complexes échouent souvent parce que :

- la vision avance plus vite que le code ;
- le code avance sans tests ;
- les idées s'empilent sans architecture ;
- les agents IA dérivent sans garde-fous ;
- les dépendances externes sont intégrées sans stratégie de licence.

Omega-Forge doit résoudre cela en créant une forge capable de découper, tester, documenter et faire évoluer un projet de manière progressive.

## Principe de construction

Avant de construire Omega-Core, on construit la forge qui pourra le construire.

Omega-Forge est donc un système bootstrap :

```text
Omega-Forge -> construit Omega-Core -> construit des outils d'expansion de possibilités
```

## Objectif V0

La V0 doit rester volontairement simple :

- lire une spécification ;
- générer une liste de tâches ;
- stocker l'état du projet ;
- exécuter des agents simples ;
- produire des rapports ;
- lancer des tests ;
- créer des tâches de correction.

La V0 ne dépend pas obligatoirement d'un LLM. La stabilité passe avant l'intelligence.

## Objectif long terme

À long terme, Omega-Forge doit permettre de créer :

- des agents spécialisés ;
- une mémoire persistante ;
- une analyse de dépôts GitHub ;
- un moteur de licence ;
- une orchestration multi-agents ;
- une interface locale ;
- un système d'exploration des possibilités ;
- une forge capable de produire, tester et améliorer ses propres composants.

## Règle fondamentale

Aucun automatisme ne doit être totalement opaque.

Chaque décision importante doit produire :

- une raison ;
- une trace ;
- un fichier modifié ;
- un test associé ou une justification d'absence de test ;
- un rapport lisible.
