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

### Peupler la base de données

```postgresql

INSERT INTO public.restaurant
(id_restaurant, uri_name, "name", logo, "uuid")
VALUES(nextval('restaurant_id_restaurant_seq'::regclass), 'shake-shack', 'Shack Shack', 'https://upload.wikimedia.org/wikipedia/commons/thumb/9/96/Shake_Shack_logo.svg/2560px-Shake_Shack_logo.svg.png', '2f973077-158e-4337-8507-ff348e99bf03');

INSERT INTO public.terminal
(id_terminal, "uuid", "name", id_restaurant)
VALUES(nextval('terminal_id_terminal_seq'::regclass), 'cebbe9f9-637b-4220-aad4-7ab299c007f1', 'Borne 001', 1);

INSERT INTO public.terminal
(id_terminal, "uuid", "name", id_restaurant)
VALUES(nextval('terminal_id_terminal_seq'::regclass), '57ec4e4c-533a-4854-98cd-c00360805eed', 'Borne 002', 1);

INSERT INTO public."style"
(id_style, "uuid", "name", style_value, id_restaurant)
VALUES(nextval('style_id_style_seq'::regclass), '43b35977-bf79-4ca7-b046-017fe2871986', 'primary', 'oklch(0.553 0.158 136.559)', 1);

INSERT INTO public."style"
(id_style, "uuid", "name", style_value, id_restaurant)
VALUES(nextval('style_id_style_seq'::regclass), 'ae38585e-8e26-4341-9442-bea52bdafe97', 'primary-foreground', 'oklch(0.984 0.003 247.858)', 1);
```