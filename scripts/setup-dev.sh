#!/bin/bash

# Script de configuration pour l'environnement de développement
# Usage: ./scripts/setup-dev.sh

echo "🚀 Configuration de l'environnement de développement..."

# Vérifier si .env.example existe
if [ ! -f ".env.example" ]; then
    echo "❌ Fichier .env.example introuvable"
    exit 1
fi

# Créer .env.local s'il n'existe pas
if [ ! -f ".env.local" ]; then
    echo "📝 Création du fichier .env.local..."
    cp .env.example .env.local
    
    # Générer une clé secrète sécurisée
    SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))")
    
    # Remplacer les valeurs par défaut
    sed -i "s/your-very-secure-secret-key-here/$SECRET_KEY/" .env.local
    sed -i "s/your-email@gmail.com/borne.appetit.projet@gmail.com/" .env.local
    sed -i "s/your-app-password/abcd efgh ijkl mnop/" .env.local
    
    echo "✅ Fichier .env.local créé avec:"
    echo "  - Clé secrète générée automatiquement"
    echo "  - Credentials SMTP partagés configurés"
else
    echo "ℹ️  Le fichier .env.local existe déjà"
fi

# Exporter les variables pour Docker Compose
echo "📦 Chargement des variables d'environnement..."
export $(cat .env.local | grep -v '^#' | xargs)

echo "✅ Configuration terminée!"
echo "💡 Vous pouvez maintenant lancer: make dev-up"