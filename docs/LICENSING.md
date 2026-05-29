# Omega-Forge Licensing Policy

Omega-Forge vise une commercialisation future possible. Les dependances et codes tiers doivent donc etre selectionnes avec prudence.

## Licences autorisees par defaut

Les licences suivantes sont compatibles avec une integration commerciale classique, sous reserve de conserver les notices :

- MIT
- Apache-2.0
- BSD-2-Clause
- BSD-3-Clause
- ISC

## Licences a verifier avant integration

- MPL-2.0
- EPL
- LGPL

Ces licences peuvent etre acceptables selon le mode d'integration, mais elles demandent une analyse plus precise.

## Licences a eviter pour le coeur ferme

- GPL
- AGPL
- SSPL
- BUSL / BSL non expiree
- licences custom restrictives

Ces licences peuvent imposer des obligations fortes, notamment l'ouverture du code source derive ou des contraintes d'usage reseau.

## Strategie d'integration

Ordre de preference :

1. Utiliser une dependance officielle via package manager.
2. Ecrire un adaptateur interne autour de l'outil.
3. Utiliser un sous-module Git.
4. Vendoriser une copie uniquement si necessaire.

## Regles obligatoires

Chaque dependance externe doit etre referencee dans :

- `third_party/THIRD_PARTY_NOTICES.md`
- `vendor_manifest.json`

Chaque entree doit contenir :

- nom du projet ;
- URL du depot ;
- licence ;
- usage prevu ;
- mode d'integration ;
- date de verification.

## Repos candidats initiaux

Candidats permissifs a verifier au moment exact de l'integration :

- LangGraph
- AutoGen
- CrewAI
- Chroma
- Qdrant
- LanceDB
- LlamaIndex
- Haystack
- OpenHands
- Aider
- GraphRAG
- PaperQA
- NetworkX
- Cytoscape.js
- React Flow
- Tauri

## Principe cle

Omega-Forge doit rester une forge propre : les briques externes augmentent le systeme, mais ne doivent pas rendre son coeur juridiquement fragile.
