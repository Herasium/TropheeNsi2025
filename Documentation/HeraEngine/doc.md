# HeraEngine

## Core

La classe **Core** est le point central du game engine, permettant la mise en place de la fenêtre, du clavier, de la souris et du rendu.

Il peut être initialisé ainsi : 

```PYTHON
from HeraEngine import Core

core = Core(start_func: Fonction, update_fonction: Fonction, asset_path: Str)
```

Il utilise deux fonctions : 

```PYTHON
core.start = func()
core.update = func(core: Core)
```

La fonction **start** est appelée à l'initialisation du projet, et **update** à chaque tick.

L'**asset_path** représente le dossier des textures pour les charger à l'avance.

L'application peut être fermée avec la fonction :

```PYTHON
core.quit()
```

---

## Types

Voici les différents types de données du projet, utilisés par l'ensemble des modules :

```PYTHON
from HeraEngine.types import ...
```

### Vec2 

L'unité initiale du projet, permettant la représentation de deux valeurs, une valeur **x** et une valeur **y**.

```PYTHON
data = Vec2(x=12, y=3.1)
print(data.x)  # 12
print(data.y)  # 3.1
```

Ils peuvent être additionnés, soustraits, multipliés et divisés, avec un autre **Vec2**, ou un **int** ou un **float**.

### Collection

Une collection d'entités, facilitant la création et la destruction d'entités ou de textes.

```PYTHON
collection = Collection(core: Core)
collection.Entity(...) 
# Paramètres identiques à l'entité classique, plus un "name" : name = entity_name
collection.Text(...)  # Idem

collection.entity_name.position = Vec2(1, 1)

collection.quit()  # Supprime toutes les entités.
```

### Texture

Représente une texture.

```PYTHON
texture = Texture(path, core: Core) 
# Le core est optionnel mais permet d'utiliser les textures préchargées ; sans lui, la texture va être rechargée depuis le fichier.

texture.size = Vec2(1, 2) 
# Redimensionne la texture, garder le même ratio que l'original est idéal.
```

### BoxCollision

Utilisé par les entités pour représenter une collision. À ne pas manipuler.

### Color

Représente une couleur, utilisée par les entités quand il n'y a pas de texture.

```PYTHON
color = Color(r=0, g=0, b=0)  # Format RGB, de 0 à 255, ici noir.
```

### Font

Représente une police d'écriture, utilisée par les entités de type **Text**.

```PYTHON
font = Font(nom, corrupted=False) 
# Le nom est celui de la police mais doit aussi être celui du dossier présent dans {asset_path}/Textures/Fonts.
# Utilise les fichiers en .raw si corrupted == False, sinon en .raw.corrupted.
font.size = Vec2(x=13, y=28) 
# Représente la taille d'une lettre. Normalement prise sur la lettre "o" automatiquement.
font.offset = Vec2(-2, 0) 
# Représente un décalage entre les lettres. Ici, -2 rapproche les lettres.
```

### Vec3

Inutile.

---

## Cursor

Cette classe représente la souris de l'utilisateur. Initialisée automatiquement par le **Core**, elle peut être accédée ainsi :

```PYTHON
mouse = core.cursor

print(mouse.x, mouse.y)  # Position de la souris, ex : 0, 0
print(mouse.position)    # Vec2(0, 0)
```

La classe possède deux listes permettant d'interagir avec la souris sous forme de fonctions à exécuter :

```PYTHON
print(mouse.on_right_click) 
print(mouse.on_left_click)  # Listes de fonctions à exécuter quand un bouton est pressé.

mouse.on_right_click.append(func(cursor: Cursor))
```

---

## Keyboard

Cette classe représente le clavier de l'utilisateur, initialisée automatiquement par le **Core**.

```PYTHON
keyboard = core.keyboard

print(keyboard.last_pressed)  # Liste contenant les appuis récents, se réinitialise à chaque tick.
```

---

## Layers

Information requise lors de la création d'une entité ou d'un texte :

```PYTHON
from HeraEngine import * 

layer = layers.background
```

---

## Window

Classe interne au game engine, gérant la relation avec la fenêtre Windows, faisant office de pont entre le game engine et l'écran, la souris, ou le clavier réel de l'utilisateur.  
À ne pas manipuler.

---

## Popup

Classe permettant la création de fenêtres "popup", comme des messages d'information ou d'erreur.

```PYTHON
from HeraEngine import Popup

Popup(text: str, titre: str, icon: int)  # Icon de 0 à 4 compris.
# Crée et affiche le popup directement sans retourner de valeurs.
```

---

## Pipeline (/render)

### pipeline.py
Fichier prenant en charge le "pipeline" graphique, transformant une liste d'entités en une liste de valeurs 32 bits prêtes à être affichées à l'écran.

### flat.py
Moteur de rendu 2D, affichant les entités simples, les textures et les textes.

Les deux modules sont internes. Il est déconseillé de les manipuler.

---

## Files (/files)

### raw_reader.py
Module permettant de lire les fichiers .raw et de charger les images.

### csv_reader.py
Module permettant de lire les fichiers .txt ou .csv pour extraire des données (séparateur : ;)

### TextureLoader

Classe s'occupant de charger l'ensemble des textures avant le lancement du jeu.  
Elle scanne le fichier indiqué par **asset_path** lors de la création du **Core** pour tous les fichiers en .raw et .raw.corrupted afin de les charger en mémoire, évitant ainsi de les relire systématiquement.

Les trois modules sont internes. Il est déconseillé de les manipuler.

---

## Childs (/childs)

### Entity

Classe majeure du game engine, représentant une entité basique, sa couleur, sa taille, ainsi que sa position ou encore sa texture.

```PYTHON
from HeraEngine import Entity

# Paramètres obligatoires
sprite = Entity(position: Vec2(), size: Vec2(), layer = layers.background)

# Paramètres optionnels :
sprite.color = Color(0, 0, 0)
sprite.texture = "Assets/Textures/exemple.raw"
sprite.texture = Texture("Assets/Textures/exemple.raw") 
# Accepte un str ou une texture.
```

Les paramètres d'entrée sont identiques à ceux d'une collection, avec un nom unique à rajouter.

Sans collection, l'entité doit être ajoutée au **Core** :

```PYTHON
core.add_entity(sprite)
core.remove_entity(sprite)
```

### Text

Similaire aux entités, avec deux paramètres obligatoires supplémentaires :

```PYTHON
sprite = Text(position: Vec2(), size: Vec2(), text: Str, font: Font, layer = layers.background)
```
