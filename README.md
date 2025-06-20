# miniagent-lab

Miniagent-lab est une petite application FastAPI démontrant l'utilisation d'un agent capable d'appeler des outils externes.

## But du projet

Ce dépôt illustre la mise en place d'un "agent" simple utilisant des outils pour rechercher des informations ou obtenir la météo. L'API expose un seul endpoint `/ask` qui fait appel à cet agent pour générer une réponse à partir d'une question utilisateur.

## Prérequis

- Python 3.10 ou supérieur.
- Les dépendances listées dans `requirements.txt`.
- Trois variables d'environnement doivent être définies :
  - `GOOGLE_CSE_ID`
  - `GOOGLE_API_KEY`
  - `OPENWEATHER_API_KEY`

Ces variables sont chargées par `config.py` et sont nécessaires au démarrage de l'application.

Un fichier `.env.example` est fourni à la racine du projet et peut être copié en `.env` pour servir de modèle.

## Installation et lancement

1. Installer les dépendances :
   ```bash
   pip install -r requirements.txt
   ```
2. Copiez le fichier `.env.example` en `.env` puis renseignez vos clés (ou exportez les variables manuellement).
3. Lancer l'application FastAPI avec Uvicorn :
   ```bash
   uvicorn main:app --reload
   ```

L'API sera alors disponible sur `http://localhost:8000`.

## Exemple de requête

Pour poser une question à l'agent :

```bash
curl "http://localhost:8000/ask?prompt=Quelle+est+la+meteo+a+Paris%3F"
```

Cette requête renverra la réponse générée par l'agent.

## Licence

Ce projet est distribue sous licence MIT. Voir le fichier [LICENSE](LICENSE) pour plus d'informations.
