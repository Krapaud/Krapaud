#!/bin/bash

# 🚀 Script automatique pour publier votre profil GitHub
# Usage: ./publish_profile.sh VOTRE_USERNAME_GITHUB

if [ $# -eq 0 ]; then
    echo "❌ Erreur: Veuillez fournir votre username GitHub"
    echo "📋 Usage: ./publish_profile.sh VOTRE_USERNAME"
    echo "📝 Exemple: ./publish_profile.sh Krapaud"
    exit 1
fi

USERNAME=$1
REPO_URL="https://github.com/$USERNAME/$USERNAME.git"

echo "🚀 Publication de votre profil GitHub..."
echo "👤 Username: $USERNAME"
echo "🔗 Repository: $REPO_URL"
echo ""

# Vérifier si on est dans le bon dossier
if [ ! -f "README.md" ]; then
    echo "❌ Erreur: README.md non trouvé. Êtes-vous dans le bon dossier ?"
    exit 1
fi

# Configurer le remote
echo "🔗 Configuration du remote origin..."
git remote remove origin 2>/dev/null || true
git remote add origin "$REPO_URL"

# Renommer la branche en main
echo "🌿 Renommage de la branche en main..."
git branch -M main

# Pousser vers GitHub
echo "⬆️  Push vers GitHub..."
if git push -u origin main; then
    echo ""
    echo "🎉 ✅ SUCCÈS ! Votre profil est maintenant en ligne !"
    echo "🌐 Visitez: https://github.com/$USERNAME"
    echo "👀 Votre profil sera visible dans quelques minutes"
    echo ""
    echo "📊 Vos statistiques GitHub se mettront à jour automatiquement"
    echo "🎨 Tous les badges et animations fonctionneront"
else
    echo ""
    echo "❌ Erreur lors du push. Vérifiez :"
    echo "1. 📝 Le repository existe sur GitHub"
    echo "2. 🔑 Vos droits d'accès (token si nécessaire)"
    echo "3. 🌐 Votre connexion internet"
fi
