@echo off
REM Script de configuration pour l'environnement de développement Windows
REM Usage: scripts\setup-dev.bat

echo 🚀 Configuration de l'environnement de développement...

REM Vérifier si .env.example existe
if not exist ".env.example" (
    echo ❌ Fichier .env.example introuvable
    exit /b 1
)

REM Créer .env.local s'il n'existe pas
if not exist ".env.local" (
    echo 📝 Création du fichier .env.local...
    copy .env.example .env.local
    
    REM Générer une clé secrète sécurisée
    for /f %%i in ('python -c "import secrets; print(secrets.token_urlsafe(32))"') do set SECRET_KEY=%%i
    
    REM Remplacer la clé secrète et les credentials SMTP dans le fichier
    powershell -Command "(gc .env.local) -replace 'your-very-secure-secret-key-here', '%SECRET_KEY%' | Out-File -encoding ASCII .env.local"
    powershell -Command "(gc .env.local) -replace 'your-email@gmail.com', 'borneappetit0@gmail.com' | Out-File -encoding ASCII .env.local"
    powershell -Command "(gc .env.local) -replace 'your-app-password', 'garr egub sndo qpxl' | Out-File -encoding ASCII .env.local"
    
    echo ✅ Fichier .env.local créé avec:
    echo   - Clé secrète générée automatiquement
    echo   - Credentials SMTP partagés configurés
) else (
    echo ℹ️  Le fichier .env.local existe déjà
)

echo ✅ Configuration terminée!
echo 💡 Vous pouvez maintenant lancer: make dev-up