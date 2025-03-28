# Once upon a Dream

Le jeu ne comporte que 3 types de classes principales :

## Cutscenes (/Cutscenes)

Elles représentent les cinématiques de discussion.

Elles sont simples et s'utilisent ainsi :

```PYTHON
from Cutscenes.scene_0 import Scene0  # Exemple

scene = Scene0(core: Core)  # Initialise la scène
scene.setup()  # Lance la scène
```

## Transitions (/Transitions)

Fonctionnant de manière similaire aux cutscenes, elles sont uniques à chaque mini-jeu mais, principalement, elles s'utilisent ainsi :

```PYTHON
from Transitions.dream_2 import Dream2  # Exemple

Dream2(core: Core)  # Initialise et lance la transition
```

Contrairement aux cutscenes, elles se lancent directement.

Des arguments supplémentaires peuvent être nécessaires selon les transitions, comme l'action à effectuer après la transition dans **you_won.py**.

## MiniGames (/MiniGames)

Ils représentent les mini-jeux qui constituent la majeure partie du jeu.

Ils sont au nombre de 4, comprenant une version corrompue de PacMan et un jeu "Maze" abandonné.

Ils sont rarement initialisés directement, le plus souvent par une transition.

Exemple de code :

```PYTHON
from MiniGames.road import Road  # Exemple

game = Road(core: Core)  # Initialise le mini-jeu
game.setup()  # Lance la scène
```

Le fonctionnement est identique à celui des cutscenes.

## __main__.py

Ce fichier représente le fichier principal contenant le menu du jeu.

Il se lance au démarrage du jeu et initialise le **Core**.

Il possède une classe **Game**, qui représente ici le menu principal.

Deux fonctions principales :

```PYTHON
game = Game(core: Core)  # Initialise le menu
game.update()  # Met à jour la scène, principalement avec la détection des appuis sur les boutons.
```