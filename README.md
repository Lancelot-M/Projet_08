# Projet 8
Pur Beurre, l'application pour les amateurs de bons produits. Consultation de produit avec liste de substitution, création de compte utilisateur 
et fiche de présentation du restaurant propriétaire.  
L'application est accessible depuis l'adresse https://floating-retreat-72525.herokuapp.com/. 

## 1) Prérequis.
Pour la consultation un navigateur suffit.   
Pour l'hébergement de l'application il est nécessaire d'accéder à un terminal et d'installer les prérequis:  
    - git  
    - python 3.8  
    - pipenv  
Une base de données Postgresql doit être créée avant d'aller plus loin dans l'installation.

## 2) Installation.
Pour installer l'application:  
    - Clonez le dépôt du projet.  
    - Activez un environnement virtuel dans le dossier téléchargé.  
    - Installez les requirements.  
    - Créez un fichier ".env" contenant l'accès à votre bdd (nom bdd, hôte, identifiant psql, mot de passe), 
ainsi que la clé secrète pour ce projet, en suivant le modèle contenu dans le fichier "env_exemple.txt".  
    - Vous pouvez activer les commandes django. (ex: python manage.py migrate)  
    
## 3) Paramétrage.
Il est possible de modifier les diverses images des applications en accédant aux dossiers '/"nom_application"/assets/'.
Attention toutefois à appliquer le nom de l'ancienne image à la nouvelle.

## 4) Contrôles.
L'application "swap_food" offre 3 commandes permettant l'interaction entre les données d'openfoodfact et la base de 
données de l'application. Elles sont activées par, leur nom précédé de "python manage.py". (ex: python manage.py delete_all)

dumps_category : Permet la création d'un fichier recensant les catégories alimentaires existantes sur le site openfoodfact.   
import_data XX XX : Permet le remplissage de la base de donnée de l'application de la ligne XX à la ligne XX du fichier créé par la commande "dumps_categories".  
delete_all : Supprime tous les aliments de la base de donnée.  

