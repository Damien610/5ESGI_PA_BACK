@echo off
echo 🔒 DÉBUT DES TESTS DE SÉCURITÉ
echo ================================
echo.

REM Test 1: Headers de sécurité
echo 1️⃣ Test des headers de sécurité...
curl -s -I http://localhost:8000/health > headers_temp.txt
findstr /i "x-content-type-options" headers_temp.txt >nul && echo ✅ X-Content-Type-Options || echo ❌ X-Content-Type-Options manquant
findstr /i "x-frame-options" headers_temp.txt >nul && echo ✅ X-Frame-Options || echo ❌ X-Frame-Options manquant
findstr /i "x-xss-protection" headers_temp.txt >nul && echo ✅ X-XSS-Protection || echo ❌ X-XSS-Protection manquant
findstr /i "strict-transport-security" headers_temp.txt >nul && echo ✅ Strict-Transport-Security || echo ❌ Strict-Transport-Security manquant
del headers_temp.txt
echo.

REM Test 2: Rate limiting
echo 2️⃣ Test du rate limiting...
for /L %%i in (1,1,5) do (
    curl -s -w "Req %%i: Status %%{http_code}" http://localhost:8000/health -o nul
    echo.
)
echo.

REM Test 3: Validation des données
echo 3️⃣ Test de validation...
echo Test injection SQL:
curl -X POST "http://localhost:8000/api/v1/clients/create" ^
     -H "Content-Type: application/json" ^
     -d "{\"first_name\":\"Robert'; DROP TABLE clients; --\",\"last_name\":\"Hacker\",\"email\":\"hack@evil.com\"}" ^
     -w "Status: %%{http_code}" -o nul
echo.

echo Test XSS:
curl -X POST "http://localhost:8000/api/v1/clients/create" ^
     -H "Content-Type: application/json" ^
     -d "{\"first_name\":\"^<script^>alert('XSS')^</script^>\",\"last_name\":\"Attacker\",\"email\":\"xss@evil.com\"}" ^
     -w "Status: %%{http_code}" -o nul
echo.

REM Test 4: Endpoints inexistants
echo 4️⃣ Test endpoints inexistants...
curl -w "Admin: %%{http_code}" http://localhost:8000/admin -o nul
echo.
curl -w ".env: %%{http_code}" http://localhost:8000/.env -o nul
echo.
curl -w "Config: %%{http_code}" http://localhost:8000/config -o nul
echo.

REM Test 5: Health check
echo 5️⃣ Test health check...
curl -s http://localhost:8000/health
echo.

REM Test 6: Documentation
echo 6️⃣ Test documentation...
curl -I http://localhost:8000/docs | findstr "HTTP"
echo.

echo 🎯 TESTS TERMINÉS
echo ================================
pause