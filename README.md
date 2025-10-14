# Borne Appétit - API Backend

API d'authentification OTP pour système de fidélité client.

## Prérequis

- Docker & Docker Compose
- Make
- Git

## Installation

```bash
# Cloner le projet
git clone <repo-url>
cd 5ESGI_PA_BACK

# Démarrer l'environnement
make dev-up

# Appliquer les migrations
make upgrade
```

## Développement

### Commandes utiles

```bash
# Démarrer les services
make dev-up

# Voir les logs
make dev-logs

# Accéder au container API
make dev-bash-api

# Accéder à la base de données
make dev-bash-db

# Arrêter les services
make dev-down
```

### Migrations

```bash
# Créer une migration
make migrate msg="description"

# Appliquer les migrations
make upgrade

# Revenir en arrière
make downgrade
```

### Tests

```bash
# Lancer les tests
make test

# Linting
make lint

# Formatage du code
make format
```

## Architecture

```
app/
├── models/          # Modèles SQLAlchemy
├── schemas/         # Schémas Pydantic
├── repositories/    # Accès base de données
├── services/        # Logique métier
├── api/routers/     # Endpoints FastAPI
├── core/           # Configuration
├── utils/          # Utilitaires
└── exceptions/     # Gestion erreurs
```

## Configuration

## Workflow de développement

1. **Créer une branche**
   ```bash
   git checkout -b feature/nom-feature
   ```

2. **Développer**
   - Ajouter/modifier le code
   - Écrire les tests
   - Tester localement

3. **Valider**
   ```bash
   make test
   make lint
   ```

4. **Commit et push**
   ```bash
   git add .
   git commit -m "feat: description"
   git push origin feature/nom-feature
   ```

5. **Pull Request**
   - Créer une PR vers `develop`
   - Attendre la review
   - Merger après validation

## Conventions

### Commits
- `feat:` nouvelle fonctionnalité
- `fix:` correction de bug
- `refactor:` refactoring
- `test:` ajout de tests
- `docs:` documentation


## Endpoints disponibles

- `POST /clients/create` - Créer un client
- `POST /clients/send-otp` - Envoyer un OTP
- `POST /clients/verify-otp` - Vérifier un OTP
- `GET /clients/{email}` - Récupérer un client

## Test rapide

```bash
# Créer un client
curl -X POST "http://localhost:8000/clients/create" \
     -H "Content-Type: application/json" \
     -d '{"first_name": "Test", "last_name": "User", "email": "test@example.com"}'

# Vérifier l'OTP
curl -X POST "http://localhost:8000/clients/verify-otp" \
     -H "Content-Type: application/json" \
     -d '{"email": "test@example.com", "otp_code": "123456"}'
```

### Logs

```bash
# Logs de l'API
docker logs fastapi_projet_dev

# Logs de la DB
docker logs postgres_dev
```
