# Documentation du Système de Gestion

## Table des Matières

1. [Présentation du Projet](#présentation-du-projet)
2. [Structure du Projet](#structure-du-projet)
3. [Modèles de Base de Données](#modèles-de-base-de-données)
4. [Rôles Utilisateurs](#rôles-utilisateurs)
5. [Panneau Administrateur](#panneau-administrateur)
6. [Panneau Client](#panneau-client)
7. [Panneau Superviseur](#panneau-superviseur)
8. [Implémentation Technique](#implémentation-technique)
9. [Diagrammes de Workflow](#diagrammes-de-workflow)

## Présentation du Projet

Le Système de Gestion est une application web complète développée avec Django qui facilite la gestion des stocks, le suivi des ventes et la gestion des rôles utilisateurs. Le système est conçu avec trois rôles utilisateurs distincts :

1. **Administrateurs** : Gèrent les produits, les fournisseurs, les superviseurs et consultent les données de ventes
2. **Clients** : Consultent les produits, effectuent des achats, et consultent leur historique d’achats
3. **Superviseurs** : Surveillent les niveaux de stock, génèrent des rapports, et supervisent les activités clients

Cette application fournit une solution complète pour les entreprises qui ont besoin de suivre leurs stocks, gérer les ventes et maintenir différents niveaux d’accès pour divers intervenants.

## Structure du Projet

Le projet suit une structure Django standard avec plusieurs applications, chacune responsable d’une fonctionnalité spécifique :

```
management/
├── admin_panel/         # Gère la fonctionnalité administrateur
├── client_panel/        # Gère la fonctionnalité client
├── supervisor_panel/    # Gère la fonctionnalité superviseur
├── stock/               # Paramètres et configuration principale du projet
├── static/              # Fichiers statiques (CSS, JavaScript, images)
├── media/               # Fichiers téléchargés par les utilisateurs (images produits)
├── templates/           # Templates partagés
└── manage.py            # Utilitaire en ligne de commande Django
```

### Composants Principaux

1. **stock** : Projet Django principal contenant les paramètres, la configuration des URL, et la configuration WSGI/ASGI.
2. **admin\_panel** : Gère les vues administrateurs, y compris la gestion des produits, fournisseurs, et superviseurs.
3. **client\_panel** : Gère l’inscription des clients, la navigation des produits, et la fonctionnalité d’achat.
4. **supervisor\_panel** : Fournit aux superviseurs des outils pour surveiller les stocks et générer des rapports.
5. **static** : Contient tous les fichiers statiques (CSS, JavaScript, images) utilisés dans l’application.
6. **media** : Stocke les fichiers téléchargés par les utilisateurs, principalement les images des produits.

## Modèles de Base de Données

L’application utilise plusieurs modèles interconnectés pour représenter ses données :

### Modèles du Panneau Administrateur

1. **Administrateur** : Lie le modèle User intégré de Django pour représenter les administrateurs.

   ```
   - user (OneToOneField vers User)
   ```
2. **Fournisseur** : Contient les informations sur les fournisseurs de produits.

   ```
   - nom  
   - téléphone  
   - email  
   - adresse
   ```
3. **Produit** : Représente les produits en stock.

   ```
   - designation  
   - prix_unitaire  
   - quantite  
   - alert_quantite  
   - fournisseur (clé étrangère vers Fournisseur)  
   - image
   ```
4. **Achat** : Enregistre les achats effectués par les clients.

   ```
   - quantite  
   - client (clé étrangère vers Client)  
   - produit (clé étrangère vers Produit)  
   - created_at (date d’achat)
   ```

### Modèles du Panneau Client

1. **Client** : Étend le modèle User avec des informations supplémentaires propres au client.

   ```
   - user (OneToOneField vers User)  
   - email  
   - téléphone  
   - adresse
   ```

### Modèles du Panneau Superviseur

1. **Superviseur** : Étend le modèle User avec des informations spécifiques au superviseur.

   ```
   - user (OneToOneField vers User)  
   - téléphone  
   - adresse  
   - date_ajout
   ```

## Rôles Utilisateurs

Le système implémente trois rôles utilisateurs distincts, chacun avec des permissions et interfaces spécifiques :

### Administrateur

Les administrateurs disposent du plus haut niveau d’accès et peuvent :

* Gérer les produits (ajouter, modifier, supprimer)
* Gérer les fournisseurs (ajouter, modifier, supprimer)
* Gérer les superviseurs (ajouter, modifier, supprimer)
* Voir les enregistrements d’achats
* Surveiller les niveaux de stock

### Client

Les clients sont les utilisateurs finaux qui peuvent :

* Consulter les produits disponibles
* Effectuer des achats
* Voir leur historique d’achats
* Gérer leurs informations de profil

### Superviseur

Les superviseurs ont des capacités de supervision et peuvent :

* Surveiller les niveaux de stock
* Générer des rapports sur les ventes et les stocks
* Voir les activités d’achat des clients
* Suivre la performance des produits

## Panneau Administrateur

Le Panneau Administrateur fournit une interface complète aux administrateurs pour gérer tous les aspects du système.

### Fonctionnalités Clés

1. **Tableau de bord**

   * Vue d’ensemble de l’état du système
   * Alertes de faible stock
   * Activités récentes d’achats
   * Accès rapide aux principales fonctions

2. **Gestion des Produits**

   * Ajouter de nouveaux produits avec détails et images
   * Modifier les informations des produits existants
   * Supprimer des produits
   * Voir les détails des produits y compris les niveaux de stock

3. **Gestion des Fournisseurs**

   * Ajouter de nouveaux fournisseurs
   * Modifier les informations des fournisseurs
   * Voir les détails des fournisseurs et produits associés

4. **Gestion des Superviseurs**

   * Créer des comptes superviseurs
   * Modifier les informations des superviseurs
   * Supprimer des comptes superviseurs
   * Voir les détails des superviseurs

5. **Enregistrements d’Achats**

   * Voir tous les achats effectués par les clients
   * Filtrer les achats par date, produit ou client
   * Voir les informations détaillées des achats

### Workflow Administrateur

1. L’administrateur se connecte via la page de connexion admin
2. Après authentification réussie, il est redirigé vers le tableau de bord
3. Depuis le tableau de bord, il peut naviguer dans les différentes sections via le menu latéral
4. Il peut effectuer des opérations CRUD sur les produits, fournisseurs, et superviseurs
5. Il peut consulter les enregistrements d’achats et surveiller les niveaux de stock

## Panneau Client

Le Panneau Client offre une interface conviviale pour que les clients consultent les produits et effectuent des achats.

### Fonctionnalités Clés

1. **Inscription et Authentification**

   * Création d’un nouveau compte
   * Connexion à un compte existant
   * Mise à jour des informations du profil

2. **Navigation des Produits**

   * Voir tous les produits disponibles
   * Filtrer les produits selon différents critères
   * Voir les informations détaillées des produits

3. **Fonctionnalité d’Achat**

   * Ajouter des produits au panier
   * Finaliser le processus d’achat
   * Voir la confirmation d’achat

4. **Historique des Achats**

   * Voir l’historique complet des achats
   * Consulter les détails des achats passés

### Workflow Client

1. Le client s’inscrit ou se connecte à un compte existant
2. Il navigue dans les produits disponibles sur la page dédiée
3. Il sélectionne les produits à acheter
4. Il finalise le processus d’achat
5. Il peut consulter son historique d’achats et ses informations de compte

## Panneau Superviseur

Le Panneau Superviseur fournit des outils pour surveiller les stocks et générer des rapports.

### Fonctionnalités Clés

1. **Tableau de bord**

   * Vue d’ensemble de l’état du système
   * Alertes de faible stock
   * Activités récentes d’achats

2. **Surveillance des Stocks**

   * Voir les niveaux actuels des stocks
   * Identifier les produits en dessous du seuil d’alerte
   * Suivre l’évolution des stocks dans le temps

3. **Outils de Reporting**

   * Générer des rapports de ventes
   * Exporter les données dans différents formats
   * Analyser les tendances des ventes

### Workflow Superviseur

1. Le superviseur se connecte via la page de connexion superviseur
2. Après authentification réussie, il est redirigé vers le tableau de bord
3. Depuis le tableau de bord, il peut surveiller les stocks et l’activité d’achats
4. Il peut générer des rapports sur les ventes et les stocks

## Implémentation Technique

Le Système de Gestion est construit avec le framework web Django, qui suit le modèle architectural Modèle-Vue-Template (MVT).

### Technologies Clés

1. **Backend**

   * Django (framework web Python)
   * Base de données SQLite (par défaut)

2. **Frontend**

   * HTML/CSS
   * JavaScript
   * Bootstrap pour un design responsive

3. **Authentification**

   * Système d’authentification intégré de Django
   * Rôles utilisateurs et permissions personnalisés

### Structure des URL

L’application utilise le système de routage URL de Django pour diriger les requêtes vers les vues appropriées :

* `/admin_panel/` - Accès aux vues administrateurs
* `/client_panel/` - Accès aux vues clients
* `/supervisor_panel/` - Accès aux vues superviseurs

### Templates

L’application utilise le système de templates Django pour générer les pages HTML :

1. **Templates du Panneau Administrateur**

   * Template maître pour la mise en page cohérente
   * Template du tableau de bord
   * Templates de gestion des produits
   * Templates de gestion des fournisseurs
   * Templates de gestion des superviseurs
   * Templates des enregistrements d’achats

2. **Templates du Panneau Client**

   * Template de base pour mise en page cohérente
   * Template du tableau de bord
   * Templates de navigation des produits
   * Templates d’achats
   * Templates de gestion du compte

3. **Templates du Panneau Superviseur**

   * Template de base pour mise en page cohérente
   * Template du tableau de bord
   * Templates de reporting

## Diagrammes de Workflow

### Flux d’Authentification Utilisateur

1. L’utilisateur accède à la page de connexion
2. L’utilisateur saisit ses identifiants
3. Le système valide les identifiants
4. Si valides, l’utilisateur est redirigé vers le tableau de bord approprié selon son rôle
5. Si invalides, un message d’erreur est affiché

### Flux de Gestion des Produits (Admin)

1. L’administrateur accède à la page de gestion des produits
2. Il peut voir la liste de tous les produits
3. Il peut ajouter un nouveau produit avec détails et image
4. Il peut modifier les informations d’un produit existant
5. Il peut supprimer des produits
6. Le système met à jour les stocks en conséquence

### Flux d’Achat (Client)

1. Le client parcourt les produits disponibles
2. Le client sélectionne les produits à acheter
3. Le client confirme l’achat
4. Le système enregistre l’achat et met à jour les stocks
5. Le client reçoit la confirmation d’achat

### Flux de Reporting (Superviseur)

1. Le superviseur accède à la section de reporting
2. Il sélectionne le type de rapport et les paramètres
3. Le système génère le rapport selon les critères choisis
4. Le superviseur peut consulter le rapport à l’écran ou l’exporter

## Conclusion

Le Système de Gestion offre une solution complète pour la gestion des stocks, le suivi des ventes, et la gestion des rôles utilisateurs. Avec ses trois interfaces distinctes (Administrateur, Client, Superviseur), il répond aux besoins de différents intervenants tout en garantissant l’intégrité et la sécurité des données.

La conception modulaire du système facilite la maintenance et l’évolution future, en faisant une solution évolutive adaptée aux entreprises de toutes tailles.