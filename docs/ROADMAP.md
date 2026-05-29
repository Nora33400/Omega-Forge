# Omega-Forge Roadmap

## Sprint 0 - Fondation

Objectif : rendre le depot lisible, installable et testable.

- [x] Creer le depot
- [x] Ajouter la vision
- [x] Ajouter la specification V0
- [ ] Ajouter l'architecture
- [ ] Ajouter la politique de licence
- [ ] Ajouter le package Python minimal
- [ ] Ajouter les tests initiaux

## Sprint 1 - Noyau V0

Objectif : disposer d'une boucle de taches locale.

- Task Queue persistante en JSON
- Project State persistante en JSON
- Report generator
- CLI minimale
- Tests unitaires

## Sprint 2 - Agents deterministes

Objectif : disposer d'agents simples avant de brancher des LLM.

- BaseAgent
- PlannerAgent
- TesterAgent
- ReviewerAgent
- Generation de taches depuis une spec Markdown
- Rapport de revue simple

## Sprint 3 - GitHub Bootstrap

Objectif : transformer les decisions en issues, fichiers ou rapports GitHub.

- Lecture de roadmap
- Creation d'issues
- Mise a jour de rapports
- Journalisation des commits

## Sprint 4 - Integration open-source controlee

Objectif : importer seulement ce qui respecte la strategie licence.

- License scanner
- Vendor manifest
- Scripts de clonage
- Third-party notices
- Adapters au lieu de copies directes quand possible

## Sprint 5 - Omega-Core initial

Objectif : commencer le moteur de possibilites.

- Graphe d'idees
- Memoire persistante
- Evaluation d'hypotheses
- Exploration de chemins possibles

## Definition de succes V0

Omega-Forge V0 est reussie quand :

1. le projet s'installe ;
2. les tests passent ;
3. une spec genere des taches ;
4. les taches peuvent changer de statut ;
5. un rapport Markdown est produit ;
6. la prochaine iteration peut etre decidee depuis ce rapport.
