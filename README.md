# Projet : Corporate AI Privacy Proxy (Middleware Conforme RGPD)

## 1. Objectif Commercial (Problème & Solution)
* **Problème :** La crainte des fuites de données et les strictes amendes du RGPD empêchent les entreprises européennes d'envoyer des documents internes (contrats, fiches de paie) vers des LLM publics (Claude, ChatGPT).
* **Solution :** Développement d'un proxy IA hybride (Middleware). Un réseau de neurones local détecte et chiffre (anonymise) les données personnelles en interne, puis le prompt sécurisé est envoyé à un modèle cloud puissant. Au retour de la réponse, les données sont déchiffrées localement.
* **Environnement Technique :** Laboratoire totalement isolé du réseau d'entreprise. Serveur local sur Dell Precision (32 Go RAM), réseau indépendant via routeur 5G.

## 2. Architecture et Fonctionnement (Approche Hybride)
Le cycle technique fonctionne comme un système de "Vestiaire" avec des tags :
1. **Création du "Dictionnaire Secret" (Local) :** Le LLM local remplace les entités sensibles (ex: "Maria Rossi") par des tags (ex: `[PERSON_1]`) et crée une table de correspondance en mémoire vive, strictement confinée au réseau d'entreprise.
2. **Envoi de la tâche anonymisée (Cloud) :** Le texte chiffré est envoyé à une IA cloud puissante (ChatGPT, Claude, Mistral) pour une analyse complexe.
3. **Traitement Intelligent (Cloud) :** Le modèle cloud analyse la logique du document sans jamais connaître les vraies données (il traite `[PERSON_1]`), et renvoie son analyse détaillée.
4. **Déchiffrement (Local) :** Le script local récupère la réponse, consulte son "dictionnaire secret", et remplace automatiquement les tags par les mots d'origine.
5. **Résultat :** L'utilisateur obtient une analyse parfaite avec les vraies données, sans qu'elles n'aient jamais transité sur internet.

## 3. Choix Techniques et Sécurité
* **Contrôle total du trafic (Zero Telemetry) :** Utilisation de la bibliothèque standard `urllib.request` en Python pour les requêtes HTTP (REST API), évitant les bibliothèques tierces (comme le package officiel ollama) pour empêcher toute collecte de données cachée.
* **Périmètre compatible RGPD :** Le modèle local (Llama 3.1) s'exécute exclusivement dans la RAM du poste local, agissant comme un filtre-censeur et un "cordon sanitaire" infranchissable.
* **Division du travail :** L'IA locale gère la tâche routinière de détection/censure, tandis que les supercalculateurs cloud gèrent l'analyse lourde, alliant 100% de sécurité locale à 100% de puissance cloud.

## 4. Journal de Développement (Logbook)
**Phase 1 : Infrastructure et Routage Réseau**
* Déploiement de l'environnement de développement : VS Code, Git, Python 3.15.
* Déploiement du noyau IA : Installation d'Ollama et test réussi du modèle Llama 3.1 en local.
* Configuration réseau : Modification des variables d'environnement (`OLLAMA_HOST=0.0.0.0:11434`) et création de règles de pare-feu (Port TCP 11434) pour transformer le PC en serveur capable de recevoir des requêtes.

**Phase 2 : Développement du Proxy (Middleware)**
* Rejet stratégique des connexions réseau non sécurisées (Wi-Fi publics/partagés) au profit d'une communication interne stricte.
* Écriture du script Python d'anonymisation via requêtes HTTP natives.
* Connexion réussie à l'API locale (`http://localhost:11434/api/generate`) et validation du censeur IA : remplacement effectif des entités sensibles par les tags `[PERSON]`, `[COMPANY]` et `[AMOUNT]`.
