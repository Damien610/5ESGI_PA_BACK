# 🔒 Tests de Sécurité - Borne Appétit API

## 🚀 Prérequis

Assurez-vous que l'API est démarrée :
```bash
# Démarrer l'environnement
docker compose -p app_dev -f docker-compose.yml --env-file .env.local up -d

# Vérifier que l'API répond
curl http://localhost:8000/health
```

## 1. 🛡️ Test des Headers de Sécurité

### Test des Headers HTTP
```bash
# Test complet des headers de sécurité
curl -I http://localhost:8000/health

# Vérification spécifique de chaque header
echo "=== HEADERS DE SÉCURITÉ ==="
curl -s -I http://localhost:8000/health | grep -i "x-content-type-options"
curl -s -I http://localhost:8000/health | grep -i "x-frame-options"
curl -s -I http://localhost:8000/health | grep -i "x-xss-protection"
curl -s -I http://localhost:8000/health | grep -i "strict-transport-security"
curl -s -I http://localhost:8000/health | grep -i "referrer-policy"
curl -s -I http://localhost:8000/health | grep -i "permissions-policy"
```

**✅ Résultat attendu :**
```
x-content-type-options: nosniff
x-frame-options: DENY
x-xss-protection: 1; mode=block
strict-transport-security: max-age=31536000; includeSubDomains
referrer-policy: strict-origin-when-cross-origin
permissions-policy: geolocation=(), microphone=(), camera=()
```

## 2. ⚡ Test du Rate Limiting

### Test Normal (sous la limite)
```bash
echo "=== TEST RATE LIMITING NORMAL ==="
for i in {1..5}; do
  echo "Requête $i:"
  curl -s -w "Status: %{http_code} - Time: %{time_total}s\n" http://localhost:8000/health -o /dev/null
done
```

### Test de Dépassement (simulation d'attaque)
```bash
echo "=== TEST RATE LIMITING - DÉPASSEMENT ==="
# Envoyer 20 requêtes rapidement pour tester la limite
for i in {1..20}; do
  curl -s -w "Req $i - Status: %{http_code}\n" http://localhost:8000/health -o /dev/null
done
```

**✅ Résultat attendu :**
- Premières requêtes : `Status: 200`
- Après dépassement : `Status: 429` (Too Many Requests)

## 3. 🌐 Test CORS

### Test Origin Autorisée
```bash
echo "=== TEST CORS - ORIGIN AUTORISÉE ==="
curl -H "Origin: http://localhost:4200" \
     -H "Access-Control-Request-Method: GET" \
     -H "Access-Control-Request-Headers: Content-Type" \
     -X OPTIONS \
     -v http://localhost:8000/health
```

### Test Origin Non Autorisée
```bash
echo "=== TEST CORS - ORIGIN NON AUTORISÉE ==="
curl -H "Origin: http://malicious-site.com" \
     -H "Access-Control-Request-Method: GET" \
     -X OPTIONS \
     -v http://localhost:8000/health
```

**✅ Résultat attendu :**
- Origin autorisée : Headers `Access-Control-Allow-*` présents
- Origin non autorisée : Pas de headers CORS ou rejet

## 4. 🔐 Test de Validation des Données

### Test Endpoint avec Données Valides
```bash
echo "=== TEST VALIDATION - DONNÉES VALIDES ==="
curl -X POST "http://localhost:8000/api/v1/clients/create" \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "John",
       "last_name": "Doe", 
       "email": "john.doe@example.com"
     }' \
     -w "Status: %{http_code}\n"
```

### Test Injection SQL (doit être bloquée)
```bash
echo "=== TEST VALIDATION - INJECTION SQL ==="
curl -X POST "http://localhost:8000/api/v1/clients/create" \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "Robert\"; DROP TABLE clients; --",
       "last_name": "Hacker",
       "email": "hacker@evil.com"
     }' \
     -w "Status: %{http_code}\n"
```

### Test XSS (doit être bloquée)
```bash
echo "=== TEST VALIDATION - XSS ==="
curl -X POST "http://localhost:8000/api/v1/clients/create" \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "<script>alert(\"XSS\")</script>",
       "last_name": "Attacker",
       "email": "xss@evil.com"
     }' \
     -w "Status: %{http_code}\n"
```

### Test Données Invalides
```bash
echo "=== TEST VALIDATION - DONNÉES INVALIDES ==="
# Email invalide
curl -X POST "http://localhost:8000/api/v1/clients/create" \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "Test",
       "last_name": "User",
       "email": "email-invalide"
     }' \
     -w "Status: %{http_code}\n"

# Champs manquants
curl -X POST "http://localhost:8000/api/v1/clients/create" \
     -H "Content-Type: application/json" \
     -d '{
       "first_name": "Test"
     }' \
     -w "Status: %{http_code}\n"
```

**✅ Résultat attendu :**
- Données valides : `Status: 200` ou `201`
- Injections/XSS : `Status: 422` (Validation Error)
- Données invalides : `Status: 422` (Validation Error)

## 5. 🚫 Test des Méthodes HTTP Non Autorisées

### Test Méthodes Autorisées
```bash
echo "=== TEST MÉTHODES AUTORISÉES ==="
curl -X GET http://localhost:8000/health -w "GET Status: %{http_code}\n" -o /dev/null
curl -X POST http://localhost:8000/api/v1/clients/create -w "POST Status: %{http_code}\n" -o /dev/null
```

### Test Méthodes Non Autorisées
```bash
echo "=== TEST MÉTHODES NON AUTORISÉES ==="
curl -X PATCH http://localhost:8000/health -w "PATCH Status: %{http_code}\n" -o /dev/null
curl -X TRACE http://localhost:8000/health -w "TRACE Status: %{http_code}\n" -o /dev/null
curl -X CONNECT http://localhost:8000/health -w "CONNECT Status: %{http_code}\n" -o /dev/null
```

**✅ Résultat attendu :**
- Méthodes autorisées : `Status: 200`, `405` (Method Not Allowed pour endpoint spécifique)
- Méthodes non autorisées : `Status: 405` (Method Not Allowed)

## 6. 📊 Test des Endpoints de Monitoring

### Test Health Check
```bash
echo "=== TEST HEALTH CHECK ==="
curl -s http://localhost:8000/health | jq '.'
```

### Test Status API
```bash
echo "=== TEST STATUS API ==="
curl -s http://localhost:8000/ | jq '.'
```

### Test Documentation (doit être accessible)
```bash
echo "=== TEST DOCUMENTATION ==="
curl -I http://localhost:8000/docs
curl -I http://localhost:8000/redoc
```

**✅ Résultat attendu :**
- Health : JSON avec `status: "healthy"`
- Status : JSON avec version et environnement
- Docs : `Status: 200`

## 7. 🔍 Test de Découverte d'Endpoints

### Test Endpoints Inexistants
```bash
echo "=== TEST ENDPOINTS INEXISTANTS ==="
curl -w "Status: %{http_code}\n" http://localhost:8000/admin -o /dev/null
curl -w "Status: %{http_code}\n" http://localhost:8000/.env -o /dev/null
curl -w "Status: %{http_code}\n" http://localhost:8000/config -o /dev/null
curl -w "Status: %{http_code}\n" http://localhost:8000/debug -o /dev/null
```

**✅ Résultat attendu :**
- Tous : `Status: 404` (Not Found)

## 8. 🕒 Test de Performance et DoS

### Test de Charge Basique
```bash
echo "=== TEST DE CHARGE BASIQUE ==="
# Test avec 50 requêtes simultanées
seq 1 50 | xargs -n1 -P10 -I{} curl -s -w "Req {}: %{http_code} - %{time_total}s\n" http://localhost:8000/health -o /dev/null
```

### Test Payload Volumineux
```bash
echo "=== TEST PAYLOAD VOLUMINEUX ==="
# Créer un payload de 1MB
python3 -c "print('a' * 1048576)" > large_payload.txt
curl -X POST "http://localhost:8000/api/v1/clients/create" \
     -H "Content-Type: application/json" \
     -d @large_payload.txt \
     -w "Status: %{http_code}\n" \
     -o /dev/null
rm large_payload.txt
```

**✅ Résultat attendu :**
- Charge normale : Temps de réponse < 1s
- Payload volumineux : `Status: 413` (Payload Too Large) ou `422`

## 9. 🔐 Test de Sécurité des Secrets

### Vérification Non-Exposition des Secrets
```bash
echo "=== TEST NON-EXPOSITION DES SECRETS ==="
# Ces endpoints ne doivent PAS exposer de secrets
curl -s http://localhost:8000/ | grep -i "secret\|password\|key" || echo "✅ Pas de secrets exposés"
curl -s http://localhost:8000/health | grep -i "secret\|password\|key" || echo "✅ Pas de secrets exposés"
```

## 10. 📝 Script de Test Complet

### Exécution de Tous les Tests
```bash
#!/bin/bash
# test_security_complete.sh

echo "🔒 DÉBUT DES TESTS DE SÉCURITÉ"
echo "================================"

# Test 1: Headers de sécurité
echo "1️⃣ Test des headers de sécurité..."
HEADERS=$(curl -s -I http://localhost:8000/health)
echo "$HEADERS" | grep -q "x-content-type-options" && echo "✅ X-Content-Type-Options" || echo "❌ X-Content-Type-Options manquant"
echo "$HEADERS" | grep -q "x-frame-options" && echo "✅ X-Frame-Options" || echo "❌ X-Frame-Options manquant"

# Test 2: Rate limiting
echo "2️⃣ Test du rate limiting..."
RATE_TEST=$(for i in {1..10}; do curl -s -w "%{http_code}" http://localhost:8000/health -o /dev/null; done)
echo "Codes de réponse: $RATE_TEST"

# Test 3: Validation
echo "3️⃣ Test de validation..."
VALIDATION=$(curl -s -w "%{http_code}" -X POST "http://localhost:8000/api/v1/clients/create" \
     -H "Content-Type: application/json" \
     -d '{"first_name":"<script>","email":"invalid"}' -o /dev/null)
[ "$VALIDATION" = "422" ] && echo "✅ Validation fonctionne" || echo "❌ Validation échoue"

echo "🎯 TESTS TERMINÉS"
```

## 🎯 Résultats Attendus - Résumé

| Test | Résultat Attendu | Signification |
|------|------------------|---------------|
| Headers de sécurité | 6 headers présents | Protection contre XSS, clickjacking, etc. |
| Rate limiting | 429 après limite | Protection contre DoS |
| CORS | Rejet origins non autorisées | Protection cross-origin |
| Validation | 422 pour données invalides | Protection injection/XSS |
| Méthodes HTTP | 405 pour non autorisées | Surface d'attaque réduite |
| Endpoints inexistants | 404 | Pas de fuite d'information |
| Secrets | Aucun exposé | Confidentialité préservée |

## 🚨 Actions si Tests Échouent

1. **Headers manquants** → Vérifier middleware de sécurité
2. **Rate limiting inactif** → Vérifier configuration middleware
3. **CORS permissif** → Vérifier allowed_origins
4. **Validation échoue** → Vérifier schémas Pydantic
5. **Secrets exposés** → Audit complet du code

Exécutez ces tests régulièrement pour maintenir la sécurité ! 🔒