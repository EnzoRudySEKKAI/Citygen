# CityGen

## **Pré-requis**

- numpy 1.22.3
- pygame 2.1.2
- pytest 7.1.1
- scipy 1.8.0
- Shapely 1.8.1.post1


## **Installation**

Avant toutes choses, executez le fichier requirements.txt:

**python -m pip install -r requirements.txt**

## **Utilisation**

Lancer le logiciel : 

_**python main.py**_ en étant placé dans le dossier src.

![menuopt](docs/requirements/menuprin.png)

Ensuite lancer GENERATE pour generer une ville.

Lancer les tests : 

_**python -m pytest**_ en étant placé dans le dossier src.

## **Sauvegarde PNG**

Une fois cliqué sur le bouton **save** il faut retourner sur le terminal et écrire le nom du fichier dans lequel on veut sauvegarder l'image.

## **Personnalisation**

Depuis le menu option:

![menuopt](docs/requirements/menuopt.png)
![menuopt](docs/requirements/menuopt2.png)
**Number of buildings** : le nombre de bâtiments que vous voulez générer.

**Number of districts** : le nombre de quartiers que vous voulez générer.

**City width** : la largeur de la ville.

**City height** : la hauteur de la ville.

Ces options peuvent rester vides, dans ce cas là, les valeurs par défaut seront utilisées. 

*Nota Bene: Toutes les valeurs ci-dessus doivent être des chiffres, sinon une erreur sera renvoyée.*

## **Bâtiments**

- **Bleu Foncé** : HOUSE
- **Marron** : LIBRARY
- **Noir** : MERCHANT
- **Bleu ciel** : INN

## **Auteurs**
* **Marouane OURICHE** 
* **Dimitrios PERIPHANOS** 
* **Wissam BOUSSELLA** 
* **Philéas BALLON** 
* **Enzo Rudy SEKKAÏ** 



