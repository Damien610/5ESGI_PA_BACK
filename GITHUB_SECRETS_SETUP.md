# 🔐 Configuration des Secrets GitHub

## Étapes à suivre dans GitHub

1. **Aller dans votre repository GitHub**
2. **Cliquer sur `Settings`**
3. **Aller dans `Secrets and variables` → `Actions`**
4. **Cliquer sur `New repository secret`**

## 🔑 Secrets à Ajouter

### **Secrets de Test**
```
Nom: SECRET_KEY_TEST
Valeur: test_$(python -c "import secrets; print(secrets.token_urlsafe(32))")

Nom: POSTGRES_PASSWORD_TEST
Valeur: test_$(python -c "import secrets; print(secrets.token_urlsafe(16))")

Nom: SMTP_PASSWORD_TEST
Valeur: test_password

Nom: MINIO_ACCESS_KEY_TEST
Valeur: test_$(python -c "import secrets; print(secrets.token_hex(8))")

Nom: MINIO_SECRET_KEY_TEST
Valeur: test_$(python -c "import secrets; print(secrets.token_hex(16))")
```

### **Secrets de Staging**
```
Nom: SECRET_KEY_STAGING
Valeur: staging_$(python -c "import secrets; print(secrets.token_urlsafe(32))")

Nom: POSTGRES_PASSWORD_STAGING
Valeur: staging_$(python -c "import secrets; print(secrets.token_urlsafe(24))")

Nom: SMTP_PASSWORD_STAGING
Valeur: votre-mot-de-passe-smtp-staging

Nom: MINIO_ACCESS_KEY_STAGING
Valeur: staging_$(python -c "import secrets; print(secrets.token_hex(16))")

Nom: MINIO_SECRET_KEY_STAGING
Valeur: staging_$(python -c "import secrets; print(secrets.token_hex(32))")
```

### **Secrets de Production**
```
Nom: SECRET_KEY_PROD
Valeur: prod_$(python -c "import secrets; print(secrets.token_urlsafe(32))")

Nom: POSTGRES_PASSWORD_PROD
Valeur: $(openssl rand -base64 32)

Nom: SMTP_PASSWORD_PROD
Valeur: votre-mot-de-passe-smtp-production

Nom: MINIO_ACCESS_KEY_PROD
Valeur: $(openssl rand -hex 16)

Nom: MINIO_SECRET_KEY_PROD
Valeur: $(openssl rand -hex 32)
```

### **Secrets Docker**
```
Nom: DOCKER_USERNAME
Valeur: votre-nom-utilisateur-docker-hub

Nom: DOCKER_PASSWORD
Valeur: votre-mot-de-passe-docker-hub
```

## 🎯 Génération des Valeurs Sécurisées

Utilisez ces commandes pour générer des valeurs sécurisées :

```bash
# SECRET_KEY (à faire 2 fois : une pour TEST, une pour PROD)
python -c "import secrets; print('SECRET_KEY:', secrets.token_urlsafe(32))"

# POSTGRES_PASSWORD_PROD
python -c "import secrets; print('POSTGRES_PASSWORD:', secrets.token_urlsafe(24))"

# MINIO_ACCESS_KEY_PROD
python -c "import secrets; print('MINIO_ACCESS_KEY:', secrets.token_hex(16))"

# MINIO_SECRET_KEY_PROD
python -c "import secrets; print('MINIO_SECRET_KEY:', secrets.token_hex(32))"
```

## ✅ Vérification

Une fois configurés, vos secrets devraient ressembler à :
- ✅ SECRET_KEY_TEST
- ✅ SECRET_KEY_PROD
- ✅ POSTGRES_PASSWORD_PROD
- ✅ SMTP_PASSWORD_PROD
- ✅ MINIO_ACCESS_KEY_PROD
- ✅ MINIO_SECRET_KEY_PROD
- ✅ DOCKER_USERNAME
- ✅ DOCKER_PASSWORD

## 🚨 IMPORTANT

- **JAMAIS** copier-coller ces valeurs dans le code
- **TOUJOURS** utiliser des valeurs différentes pour test/prod
- **CHANGER** les secrets tous les 90 jours
- **RÉVOQUER** immédiatement en cas de compromission