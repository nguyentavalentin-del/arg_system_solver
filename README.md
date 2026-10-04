# Solveur de Systèmes d'Argumentation Abstraite

## Projet RCR 2025-2026

Ce projet implémente un solveur de systèmes d'argumentation abstraite basé sur les travaux fondateurs de Dung. Il permet de résoudre différents problèmes de décision et de vérification dans le cadre des sémantiques préférées et stables.

---

## Membres du Binôme

- **Nom et Prénom 1** : [NGUYEN Valentin-Even]
- **Nom et Prénom 2** : [KHADIR Abdessamed]

---

## Installation

### Prérequis

Le projet nécessite uniquement **Python 3** et n'utilise **aucune bibliothèque externe**. 

### Installation

Aucune installation particulière n'est requise. Il suffit de cloner ou télécharger le projet et de s'assurer que Python 3 est installé sur votre système.

```bash
python3 --version
```

---

## Usage

### Syntaxe Générale

Le programme s'exécute via la ligne de commande avec la syntaxe suivante :

```bash
python3 my_solver.py -p XX-YY -f <file.apx> -a <arg>
```

### Distinction Stricte des Drapeaux

⚠️ **Important** : Le sujet impose une distinction stricte entre les drapeaux selon le type de problème :

#### Drapeau `-P` (majuscule) : Problèmes de Vérification

Utilisez `-P` pour les problèmes de **vérification** suivants :

- **VE-PR** : Vérification crédule sous sémantique préférée
- **VE-ST** : Vérification crédule sous sémantique stable

**Exemple** :
```bash
python3 my_solver.py -P VE-PR -f exemple.apx -a arg1
```

#### Drapeau `-p` (minuscule) : Problèmes de Décision

Utilisez `-p` pour les problèmes de **décision** suivants :

- **DC-PR** : Acceptation crédule sous sémantique préférée
- **DS-PR** : Acceptation sceptique sous sémantique préférée
- **DC-ST** : Acceptation crédule sous sémantique stable
- **DS-ST** : Acceptation sceptique sous sémantique stable

**Exemple** :
```bash
python3 my_solver.py -p DC-PR -f exemple.apx -a arg1
```

### Paramètres

- `-p XX-YY` ou `-P XX-YY` : Type de problème à résoudre (voir ci-dessus)
- `-f <file.apx>` : Fichier d'entrée au format APX contenant le système d'argumentation
- `-a <arg>` : Argument à évaluer

### Exemples d'Utilisation

```bash
# Vérification crédule sous sémantique préférée
python3 my_solver.py -P VE-PR -f test_files/example1.apx -a a

# Acceptation crédule sous sémantique préférée
python3 my_solver.py -p DC-PR -f test_files/example2.apx -a b

# Acceptation sceptique sous sémantique stable
python3 my_solver.py -p DS-ST -f test_files/example3.apx -a c
```

---

## Algorithme

### Approche par Étiquetage

Le solveur implémente la **sémantique de Labelling (étiquetage)** de **Caminada (2006)**, une approche formelle et efficace pour le calcul des extensions d'argumentation. Cette méthode, basée sur l'attribution d'étiquettes (IN, OUT, UNDEC) aux arguments, offre une alternative élégante à l'approche naïve par énumération exhaustive.

### Avantages de l'Approche

- **Formalisme rigoureux** : Basé sur des fondations théoriques solides
- **Efficacité** : Évite l'énumération exhaustive de toutes les extensions possibles
- **Clarté conceptuelle** : Représentation intuitive de l'état d'acceptabilité des arguments

---

## Sortie

Le programme affiche uniquement :

- **`YES`** : Si la propriété testée est vérifiée
- **`NO`** : Si la propriété testée n'est pas vérifiée

**Exemple** :
```bash
$ python3 my_solver.py -p DC-PR -f test.apx -a a
YES
```

---

## Structure du Projet

```
projet/
├── src/
│   ├── my_solver.py           # Point d'entrée principal
│   ├── ArgumentationSystem.py # Implémentation du système d'argumentation
│   └── tests.py               # Tests unitaires
├── test_files/                # Fichiers de test au format APX
└── README.md                  # Cette documentation
```

---

## Références

- **Dung, P. M.** (1995). *On the acceptability of arguments and its fundamental role in nonmonotonic reasoning, logic programming and n-person games*. Artificial Intelligence, 77(2), 321-357.
- **Caminada, M.** (2006). *On the Issue of Reinstatement in Argumentation*. In Logics in Artificial Intelligence (pp. 111-123).

---

## Licence

Projet académique réalisé dans le cadre du cours de Représentation des Connaissances et Raisonnement (RCR) 2025-2026.
