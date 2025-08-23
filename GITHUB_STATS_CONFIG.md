# Configuration des Statistiques GitHub Automatiques

Ce document explique comment fonctionnent les statistiques automatiques de votre profil GitHub.

## 🤖 Mises à jour automatiques

### 1. Workflows GitHub Actions

Deux workflows ont été configurés dans `.github/workflows/` :

- **`update-readme.yml`** : Met à jour les statistiques personnalisées tous les jours à 6h UTC
- **`metrics.yml`** : Génère des métriques avancées tous les jours à 2h UTC

### 2. Badges dynamiques

Les badges suivants se mettent à jour automatiquement :

```markdown
![GitHub followers](https://img.shields.io/github/followers/Krapaud?style=for-the-badge&logo=github&color=58A6FF&labelColor=0D1117)
![GitHub repositories](https://img.shields.io/badge/dynamic/json?logo=github&style=for-the-badge&color=1F6FEB&labelColor=0D1117&label=Repositories&query=%24.public_repos&url=https%3A%2F%2Fapi.github.com%2Fusers%2FKrapaud)
![Profile views](https://komarev.com/ghpvc/?username=Krapaud&style=for-the-badge&color=58A6FF&labelColor=0D1117)
```

### 3. Widgets en temps réel

Ces widgets se mettent à jour automatiquement à chaque chargement de page :

- **GitHub Stats** : `github-readme-stats.vercel.app`
- **Streak Stats** : `github-readme-streak-stats.herokuapp.com`
- **Activity Graph** : `github-readme-activity-graph.vercel.app`
- **Language Stats** : `github-readme-stats.vercel.app/api/top-langs`

## 🔧 Configuration

### Personnalisation des couleurs

Vous pouvez modifier les couleurs des widgets en changeant les paramètres `theme` :

- `tokyonight` : Thème sombre bleu/violet
- `radical` : Thème sombre rouge/rose
- `merko` : Thème sombre vert
- `gruvbox` : Thème sombre orange/marron
- `dark` : Thème sombre classique
- `vue` : Thème clair vert/bleu

### Modification des métriques

Pour ajouter ou modifier les métriques affichées, éditez le fichier `update-readme.yml` dans la section `Get GitHub Stats`.

### Mise à jour manuelle

Utilisez le script Python pour une mise à jour locale :

```bash
python3 update_stats.py
```

## 📊 Métriques disponibles

### Automatiques (API GitHub)
- Nombre de repositories
- Nombre de followers/following
- Étoiles totales
- Forks totales
- Langages utilisés
- Commits par année
- Date de création du compte

### En temps réel (Widgets)
- Statistiques de contribution
- Streak de commits
- Graphique d'activité
- Distribution des langages
- Heatmap des contributions

## 🔄 Fréquence de mise à jour

- **Badges dynamiques** : En temps réel
- **Widgets externes** : Cache de ~5-15 minutes
- **Workflow Actions** : Quotidien (6h UTC)
- **Métriques avancées** : Quotidien (2h UTC)

## 🛠️ Dépannage

### Si les badges ne s'affichent pas :
1. Vérifiez que votre profil GitHub est public
2. Assurez-vous que l'API GitHub est accessible
3. Vérifiez les permissions du token GITHUB_TOKEN

### Si les workflows ne s'exécutent pas :
1. Vérifiez que les Actions GitHub sont activées
2. Assurez-vous que les workflows ont les permissions nécessaires
3. Consultez l'onglet "Actions" pour voir les erreurs

## 📝 Personnalisation avancée

Pour personnaliser davantage vos statistiques, vous pouvez :

1. Modifier les requêtes API dans `update-readme.yml`
2. Ajouter de nouveaux services de badges
3. Créer vos propres widgets personnalisés
4. Intégrer d'autres métriques (Wakatime, etc.)

---

*Dernière mise à jour de cette documentation : 23/08/2025*
