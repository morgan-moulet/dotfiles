# 🪟 Tmux Cheatsheet & Command Reference

> **Complete reference guide covering both everyday basic commands and advanced features optimized for AI Coding Agents, Multi-Pane Workflows & Homelab Orchestration.**  
> Managed via [Chezmoi](https://www.chezmoi.io/) (`dot_tmux.conf` → `~/.tmux.conf`).

---

## ⚡ The Basics & Dual Prefix

This configuration supports **two prefix keys** interchangeably:
* **`Ctrl + a`** *(Recommended — ergonomic, fast, standard screen-like)*
* **`Ctrl + b`** *(Default tmux standard)*

> 💡 **Notation :** Dans ce guide, **`Prefix`** signifie appuyer sur `Ctrl + a` (ou `Ctrl + b`), relâcher, puis appuyer sur la touche indiquée.

---

## 🖥️ Commandes CLI de Base (Depuis votre terminal)

Ces commandes s'exécutent directement dans votre shell (Fish, Bash, Zsh) pour gérer les sessions :

```bash
# Lancer une nouvelle session par défaut
tmux

# Créer une nouvelle session avec un nom explicite (Recommandé)
tmux new -s nom-de-session

# Lister toutes les sessions en cours d'exécution
tmux ls

# Se rattacher à la dernière session active
tmux a
# ou
tmux attach

# Se rattacher à une session précise par son nom
tmux a -t nom-de-session

# Détacher la session en cours (depuis l'intérieur de tmux)
# Raccourci : Prefix + d (la session continue de tourner en arrière-plan)

# Renommer une session existante depuis le shell
tmux rename-session -t ancien-nom nouveau-nom

# Fermer / tuer une session précise
tmux kill-session -t nom-de-session

# Fermer / tuer TOUTES les sessions et quitter le serveur tmux
tmux kill-server
```

---

## ⌨️ Raccourcis de Base Indispensables (Dans tmux)

Les commandes fondamentales que tout utilisateur de tmux doit connaître :

| Raccourci | Action | Description |
| :--- | :--- | :--- |
| **`Prefix` + `d`** | **Détacher la session** | Quitte tmux et revient à votre shell normal. Tous vos agents, compilations et scripts continuent de tourner en arrière-plan ! |
| **`Prefix` + `?`** | **Aide intégrée** | Affiche la liste complète de TOUS les raccourcis clavier actifs dans votre configuration. Appuyez sur `q` pour quitter. |
| **`Prefix` + `:`** | **Ligne de commande interne** | Ouvre l'invite interne de tmux en bas de l'écran pour taper des commandes (ex: `:set -g mouse on`, `:source ~/.tmux.conf`). |
| **`Prefix` + `q`** | **Afficher les numéros de panneaux** | Affiche de grands numéros sur chaque panneau. Tapez le chiffre correspondant pour y aller instantanément. |
| **`Prefix` + `o`** | **Panneau suivant** | Passe au panneau suivant en boucle. |
| **`Prefix` + `;`** | **Panneau précédent** | Bascule directement vers le dernier panneau actif. |
| **`Prefix` + `t`** | **Horloge plein écran** | Affiche une horloge numérique géante dans le panneau actif (appuyez sur n'importe quelle touche pour fermer). |
| **`Prefix` + `r`** | **Recharger la configuration** | Recharge à chaud `~/.tmux.conf` avec notification visuelle `✓ tmux.conf reloaded!`. |
| **`exit`** *(dans le shell)* | **Fermer le panneau** | Ferme le shell en cours. Si c'est le dernier panneau, ferme la fenêtre / session. |

---

## 🤖 Super-pouvoirs pour Agents IA & Multi-Panneaux

Raccourcis spécifiquement configurés pour orchestrer plusieurs agents (Claude Code, Antigravity, Aider, OpenHands...) :

| Raccourci | Action | Cas d'usage IA |
| :--- | :--- | :--- |
| **`Prefix` + `S`** | **Synchronisation des panneaux (Toggle)** | Écrit le même texte ou prompt **simultanément dans tous les panneaux**. Idéal pour tester un prompt sur plusieurs modèles en parallèle ou lancer une commande sur plusieurs serveurs. |
| **`Prefix` + `P`** | **Journalisation d'audit en continu (Toggle)** | Enregistre en direct tout le flux stdout/stderr du panneau dans `~/.tmux/logs/%Y%m%d-%H%M%S-#S-#W-#P.log`. Parfait pour auditer les actions d'un agent a posteriori. |
| **`Prefix` + `z`** | **Zoom / Dézoom plein écran** | Agrandit le panneau de l'agent en plein écran pour lire un diff large ou un long flux de pensée, puis revient à la disposition normale. |
| **`Alt` + `Flèches`** | **Changement de panneau instantané** | Bascule entre les agents sans avoir à taper le préfixe. |
| **`Alt` + `h` `j` `k` `l` | **Navigation Vim rapide** | Même chose avec les touches Vim `h` (gauche), `j` (bas), `k` (haut), `l` (droite). |
| **`Prefix` + `\|`** | **Split vertical (côte à côte)** | Divise le panneau verticalement **en conservant le dossier de travail courant**. |
| **`Prefix` + `-`** | **Split horizontal (l'un sous l'autre)** | Divise le panneau horizontalement **en conservant le dossier de travail courant**. |
| **`Prefix` + `x`** | **Fermer le panneau immédiatement** | Ferme le panneau sans la question de confirmation agaçante `kill-pane? (y/n)`. |

---

## 🪟 Gestion des Fenêtres (Onglets)

Les fenêtres se comportent comme des onglets dans votre session tmux :

| Raccourci | Action |
| :--- | :--- |
| **`Prefix` + `c`** | Créer une nouvelle fenêtre (*Create*) dans le dossier courant |
| **`Prefix` + `1` .. `9`** | Aller directement à la fenêtre 1, 2, 3... |
| **`Prefix` + `,`** | Renommer la fenêtre courante (ex: `agent-1`, `logs`, `serveur`) |
| **`Prefix` + `w`** | Arborescence interactive de toutes les fenêtres et sessions |
| **`Prefix` + `n`** | Fenêtre suivante (*Next*) |
| **`Prefix` + `p`** | Fenêtre précédente (*Previous*) |
| **`Prefix` + `l`** | Revenir à la dernière fenêtre consultée (*Last*) |
| **`Prefix` + `f`** | Rechercher une fenêtre par mot-clé (*Find*) |
| **`Prefix` + `&`** | Tuer la fenêtre courante avec confirmation |

---

## 📐 Déplacement & Redimensionnement des Panneaux

| Raccourci | Action |
| :--- | :--- |
| **`Prefix` + `{`** | Intervertir le panneau courant avec le précédent |
| **`Prefix` + `}`** | Intervertir le panneau courant avec le suivant |
| **`Prefix` + `!`** | **Détacher le panneau** : transforme le panneau courant en une fenêtre dédiée ! |
| **`Prefix` + `H`** | Agrandir le panneau vers la **gauche** (5 colonnes) |
| **`Prefix` + `J`** | Agrandir le panneau vers le **bas** (5 lignes) |
| **`Prefix` + `K`** | Agrandir le panneau vers le **haut** (5 lignes) |
| **`Prefix` + `L`** | Agrandir le panneau vers la **droite** (5 colonnes) |
| **`Prefix` + `Espace`** | Alterner automatiquement entre les dispositions prédéfinies (colonnes égales, lignes égales, panneau principal + secondaires...) |

---

## 📜 Mode Copie, Défilement & Presse-Papier Universel (OSC 52)

Cette configuration inclut un historique géant de **100 000 lignes** et le protocole **OSC 52** : la copie fonctionne directement dans le presse-papier de votre machine hôte (Windows, Mac, etc.) même à travers **SSH, JetBrains Gateway ou JuiceSSH**, sans besoin de serveur X11.

### À la souris
* **Molette** : Défile instantanément dans l'historique sans raccourci.
* **Sélection à la souris** : Glissez pour surligner ; dès que vous relâchez le clic, le texte est copié dans le presse-papier système !

### Au clavier (Mode Vi)
| Raccourci | Action |
| :--- | :--- |
| **`Prefix` + `[`** | Entrer en mode copie / défilement |
| **`k` / `j`** ou **`↑` / `↓`** | Monter / Descendre d'une ligne |
| **`Ctrl` + `u` / `Ctrl` + `d`** | Défiler d'une demi-page vers le haut / bas |
| **`g` / `G`** | Aller tout en haut / tout en bas de l'historique |
| **`/`** | Rechercher vers le bas |
| **`?`** | Rechercher vers le haut |
| **`n` / `N`** | Occurrence suivante / précédente |
| **`v`** | Commencer la sélection de texte |
| **`Ctrl` + `v`** | Basculer en sélection de bloc rectangulaire |
| **`y`** | Copier la sélection dans le presse-papier système et quitter le mode |
| **`q`** ou **`Échap`** | Quitter le mode copie |
| **`Prefix` + `]`** | Coller le dernier buffer tmux interne |

---

## 📊 Indicateurs de la Barre de Statut

La barre de statut en bas d'écran affiche des indicateurs en temps réel :
* **`󰖯 #S`** : Nom de la session active (en cyan).
* **`#I: #W`** : Numéro et nom de chaque fenêtre.
* **`󰊓`** : S'affiche à côté de la fenêtre quand le panneau actif est **Zoomé** (`Prefix + z`).
* **`󰓦`** : S'affiche à côté de la fenêtre quand la **Synchronisation des panneaux** est active (`Prefix + S`).
* **`󰉋 <dossier>`** : Dossier de travail actuel du panneau actif.
* **`󱑍 HH:MM`** : Heure locale du serveur.
* **` #H`** : Nom d'hôte de la machine hôte (`uruk`, `jenko`, station Rocky).
