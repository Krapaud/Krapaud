# 🔗 Commandes à exécuter dans votre terminal

## Une fois votre repository créé sur GitHub, exécutez ces commandes :

```bash
# Dans le dossier /home/krapaud/Krapaud/
cd /home/krapaud/Krapaud

# Connecter au repository GitHub (remplacez YOUR_USERNAME par votre vrai username GitHub)
git remote add origin https://github.com/YOUR_USERNAME/YOUR_USERNAME.git

# Renommer la branche en main (recommandé)
git branch -M main

# Pousser votre code vers GitHub
git push -u origin main
```

## 🎯 **Ce qui va se passer :**

1. ✅ Votre README.md sera automatiquement affiché sur votre profil GitHub
2. ✅ Tous les visiteurs verront votre belle page de présentation
3. ✅ Les statistiques et graphiques se mettront à jour automatiquement
4. ✅ Votre profil sera accessible via : `github.com/YOUR_USERNAME`

## 🔧 **Si vous avez des problèmes :**

### Authentification requise
Si Git vous demande un mot de passe, vous devrez utiliser un Personal Access Token :

1. Allez dans **Settings** > **Developer settings** > **Personal access tokens**
2. Créez un nouveau token avec les permissions **repo**
3. Utilisez ce token comme mot de passe

### Repository déjà existant
Si vous avez déjà un repository avec ce nom :
```bash
git remote set-url origin https://github.com/YOUR_USERNAME/YOUR_USERNAME.git
git push -f origin main
```

## 📱 **Vérification :**

1. Allez sur `github.com/YOUR_USERNAME`
2. Vous devriez voir votre belle page avec :
   - ✨ Animation de texte
   - 📊 Statistiques GitHub
   - 🎨 Badges colorés
   - 🚀 Projets mis en valeur

---

**🎉 Félicitations ! Votre profil GitHub sera maintenant professionnel et attractif !**
