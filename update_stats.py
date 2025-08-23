#!/usr/bin/env python3
"""
Script pour mettre à jour automatiquement les statistiques GitHub dans le README.md
Usage: python3 update_stats.py
"""

import json
import re
import requests
from datetime import datetime
import os
import sys

def get_github_stats(username):
    """Récupère les statistiques GitHub pour un utilisateur donné"""
    
    base_url = "https://api.github.com"
    
    try:
        # Informations utilisateur
        user_response = requests.get(f"{base_url}/users/{username}")
        user_data = user_response.json()
        
        # Repositories
        repos_response = requests.get(f"{base_url}/users/{username}/repos?per_page=100")
        repos_data = repos_response.json()
        
        # Calcul des statistiques
        stats = {
            'username': username,
            'public_repos': user_data.get('public_repos', 0),
            'followers': user_data.get('followers', 0),
            'following': user_data.get('following', 0),
            'created_at': user_data.get('created_at', ''),
            'total_stars': sum(repo.get('stargazers_count', 0) for repo in repos_data if isinstance(repos_data, list)),
            'total_forks': sum(repo.get('forks_count', 0) for repo in repos_data if isinstance(repos_data, list)),
            'languages': {}
        }
        
        # Calcul du nombre de jours depuis la création
        if stats['created_at']:
            from datetime import datetime
            created_date = datetime.strptime(stats['created_at'][:10], '%Y-%m-%d')
            days_since_creation = (datetime.now() - created_date).days
            stats['days_on_github'] = days_since_creation
        
        # Langages les plus utilisés
        if isinstance(repos_data, list):
            for repo in repos_data:
                if repo.get('language'):
                    lang = repo['language']
                    stats['languages'][lang] = stats['languages'].get(lang, 0) + 1
        
        return stats
        
    except Exception as e:
        print(f"Erreur lors de la récupération des statistiques: {e}")
        return None

def update_readme_stats(stats):
    """Met à jour le README.md avec les nouvelles statistiques"""
    
    try:
        # Lire le fichier README actuel
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Générer le timestamp de mise à jour
        update_time = datetime.now().strftime('%d/%m/%Y à %H:%M UTC')
        
        # Mettre à jour le timestamp dans le README
        content = re.sub(
            r'<!--STATS_UPDATE_TIME-->.*?<!--/STATS_UPDATE_TIME-->',
            f'<!--STATS_UPDATE_TIME-->{update_time}<!--/STATS_UPDATE_TIME-->',
            content
        )
        
        # Créer une section de statistiques enrichies
        enhanced_stats = f"""
### 📊 **Statistiques GitHub Détaillées**

<div align="center">

| 📈 **Métrique** | 📊 **Valeur** | 🎯 **Détails** |
|:---|:---:|:---|
| 📚 **Repositories publics** | **{stats['public_repos']}** | Projets open source |
| ⭐ **Total des étoiles** | **{stats['total_stars']}** | Reconnaissance communauté |
| 🍴 **Total des forks** | **{stats['total_forks']}** | Projets dupliqués |
| 👥 **Followers** | **{stats['followers']}** | Communauté GitHub |
| 👤 **Following** | **{stats['following']}** | Développeurs suivis |
| 📅 **Jours sur GitHub** | **{stats['days_on_github']}** | Ancienneté du compte |

#### 🌐 **Langages Principaux**
"""
        
        # Ajouter les langages les plus utilisés
        if stats['languages']:
            sorted_languages = sorted(stats['languages'].items(), key=lambda x: x[1], reverse=True)[:5]
            for lang, count in sorted_languages:
                enhanced_stats += f"![{lang}](https://img.shields.io/badge/{lang}-{count}%20repos-blue?style=flat-square) "
            enhanced_stats += "\n"
        
        enhanced_stats += f"""
<br>

<sub>🤖 <em>Statistiques générées automatiquement • Dernière mise à jour: {update_time}</em></sub>

</div>

---
"""
        
        # Chercher où insérer les statistiques détaillées
        # Les insérer après la section "Métriques en Temps Réel"
        pattern = r'(#### 🎯 \*\*Badges de Performance\*\*.*?<sub>🔄.*?</div>\s*</div>)'
        
        if re.search(pattern, content, re.DOTALL):
            content = re.sub(
                pattern,
                r'\1\n\n' + enhanced_stats,
                content,
                flags=re.DOTALL
            )
        
        # Écrire le nouveau contenu
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"✅ README.md mis à jour avec succès!")
        print(f"📊 Statistiques pour @{stats['username']}:")
        print(f"   📚 {stats['public_repos']} repositories")
        print(f"   ⭐ {stats['total_stars']} étoiles")
        print(f"   👥 {stats['followers']} followers")
        print(f"   📅 {stats['days_on_github']} jours sur GitHub")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de la mise à jour du README: {e}")
        return False

def main():
    """Fonction principale"""
    
    username = "Krapaud"  # Remplacez par votre nom d'utilisateur GitHub
    
    print(f"🔄 Récupération des statistiques GitHub pour @{username}...")
    
    # Récupérer les statistiques
    stats = get_github_stats(username)
    
    if not stats:
        print("❌ Impossible de récupérer les statistiques GitHub")
        sys.exit(1)
    
    # Mettre à jour le README
    if update_readme_stats(stats):
        print("🎉 Mise à jour terminée avec succès!")
    else:
        print("❌ Échec de la mise à jour")
        sys.exit(1)

if __name__ == "__main__":
    main()
