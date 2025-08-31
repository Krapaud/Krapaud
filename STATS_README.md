# 🔄 GitHub Stats Auto-Updater

Ce système automatise la mise à jour de vos statistiques GitHub dans votre profil README.

## 📁 Fichiers

- `update_stats.py` - Script principal de mise à jour
- `auto_update.sh` - Script bash pour automatisation
- `stats.json` - Fichier de données JSON
- `.github/workflows/update-stats.yml` - GitHub Actions

## 🚀 Utilisation

### 1. Manual Update
```bash
cd /home/krapaud/Krapaud
python3 update_stats.py
```

### 2. Via script bash
```bash
./auto_update.sh
```

### 3. Automatisation avec crontab
Pour une mise à jour quotidienne à 6h00 :
```bash
# Éditer crontab
crontab -e

# Ajouter cette ligne :
0 6 * * * /home/krapaud/Krapaud/auto_update.sh
```

### 4. GitHub Actions (recommandé)
Le workflow `.github/workflows/update-stats.yml` se déclenche :
- Automatiquement chaque jour à 6h00 UTC
- Manuellement via l'interface GitHub
- À chaque push sur le script

## 📊 Badges dynamiques

Vos badges utilisent maintenant :

### Badges statiques mis à jour automatiquement :
```markdown
![Commits](https://img.shields.io/badge/Commits-802-brightgreen)
```

### Badges dynamiques (recommandé) :
```markdown
![Commits 2025](https://img.shields.io/badge/dynamic/json?color=brightgreen&label=Commits%202025&query=commits_2025&url=https://raw.githubusercontent.com/Krapaud/Krapaud/main/stats.json)
```

## 🛠️ Configuration

### Variables d'environnement (optionnel)
```bash
export GITHUB_USERNAME="Krapaud"
export GITHUB_TOKEN="your_token_here"  # Pour éviter les limites de l'API
```

### Personnalisation
Modifiez les variables dans `update_stats.py` :
- `username` - Votre nom d'utilisateur GitHub
- `base_path` - Chemin vers vos dépôts
- `profile_path` - Chemin vers votre dépôt de profil

## 📈 Fonctionnalités

✅ **Statistiques locales :**
- Compte automatique des commits 2025
- Analyse de tous vos dépôts Git locaux
- Détection des langages de programmation

✅ **Statistiques GitHub API :**
- Followers, stars, repositories publics
- Mise à jour automatique des badges

✅ **Mise à jour automatique :**
- README.md mis à jour
- Fichier stats.json généré
- Timestamp automatique

✅ **Intégration Git :**
- Commit et push automatiques
- Support GitHub Actions

## 🔧 Dépannage

### Script ne fonctionne pas
```bash
# Vérifier les permissions
chmod +x update_stats.py auto_update.sh

# Tester manuellement
python3 update_stats.py
```

### Erreur API GitHub
- Vérifiez votre connexion internet
- Ajoutez un token GitHub pour éviter les limites

### Crontab ne fonctionne pas
```bash
# Vérifier le service cron
sudo systemctl status cron

# Voir les logs
tail -f /home/krapaud/Krapaud/update_stats.log
```

## 📅 Planification recommandée

- **GitHub Actions** : Quotidien à 6h00 UTC
- **Crontab local** : Backup quotidien à 7h00
- **Manuel** : Avant commits importants

## 🎯 Prochaines améliorations

- [ ] Intégration Wakatime
- [ ] Statistiques de contributions détaillées
- [ ] Support multi-comptes GitHub
- [ ] Dashboard web interactif
- [ ] Notifications par email
