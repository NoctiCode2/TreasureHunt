# TreasureHunt

Un projet de simulation d'agents collectant des trésors dans un environnement en grille, avec une gestion intelligente des tâches.

## 📌 Description
Ce projet est une simulation en **Python** utilisant **Pygame** pour l'affichage, où plusieurs agents (or, pierres et coffre) interagissent pour collecter et déposer des trésors. Un système de gestion des tâches assigne dynamiquement les missions aux agents selon leur disponibilité et leur proximité.

## 🚀 Fonctionnalités
- Génération dynamique de trésors sur la grille (hors zone de dépôt).
- Agents spécialisés : collecteurs d'or, de pierres et ouvreurs de coffres.
- Système de gestion des tâches avec assignation intelligente.
- Interface graphique avec **Pygame**.
- Affichage du **score global** et des agents en temps réel.



## 🕹️ Utilisation
- Les agents se déplacent et exécutent automatiquement leurs tâches.
- Les trésors sont générés toutes les 10 itérations.
- L’affichage Pygame montre la grille, les trésors et les agents en mouvement.
- Fermez la fenêtre pour arrêter la simulation.

## 📁 Structure du Projet
```
├── Environment.py        # Gestion de l'environnement (grille, trésors, dépôt)
├── TaskManager.py        # Gestion des tâches et coordination des agents
├── MyAgentGold.py        # Agent collecteur d'or
├── MyAgentStones.py      # Agent collecteur de pierres
├── MyAgentChest.py       # Agent ouvreur de coffre
├── Treasure.py           # Modèle des trésors
├── main.py               # Point d'entrée principal
├── env1.txt              # Fichier de configuration de l'environnement
├── README.md             # Documentation
└── requirements.txt      # Dépendances Python
```

## 📜 Licence
Ce projet est sous licence **MIT**. Vous pouvez l’utiliser, le modifier et le partager librement.


## ✨ Contributeurs
👤 **Nina** - [MyGit]([https://github.com/votre-utilisateur](https://github.com/NoctiCode2))

Les contributions sont les bienvenues ! Créez une **issue** ou soumettez une **pull request**. 🚀

