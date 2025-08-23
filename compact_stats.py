#!/usr/bin/env python3
"""
Script pour créer une version compacte de la section GitHub Statistics
"""

def create_compact_stats():
    compact_stats = '''## 📊 GitHub Statistics

<div align="center">

<!-- Header compact avec animation -->
<img src="https://readme-typing-svg.herokuapp.com?font=Fira+Code&size=24&duration=3000&pause=500&color=58A6FF&center=true&vCenter=true&width=500&lines=📊+GitHub+Analytics;🚀+Dev+Metrics;💻+Coding+Stats" alt="Stats Header" />

<!-- Badges de métriques en ligne compacte -->
<div style="margin: 15px 0;">
<img src="https://img.shields.io/github/followers/Krapaud?style=flat-square&logo=github&color=58A6FF&labelColor=0D1117" alt="Followers"/>
<img src="https://img.shields.io/github/stars/Krapaud?affiliations=OWNER&style=flat-square&logo=star&color=FFD700&labelColor=0D1117" alt="Stars"/>
<img src="https://img.shields.io/badge/dynamic/json?logo=github&style=flat-square&color=1F6FEB&labelColor=0D1117&label=Repos&query=%24.public_repos&url=https%3A%2F%2Fapi.github.com%2Fusers%2FKrapaud" alt="Repos"/>
<img src="https://komarev.com/ghpvc/?username=Krapaud&style=flat-square&color=58A6FF&labelColor=0D1117" alt="Views"/>
<img src="https://img.shields.io/github/last-commit/Krapaud/Krapaud?style=flat-square&logo=github&color=58A6FF&labelColor=0D1117" alt="Last Commit"/>
</div>

<!-- Dashboard principal en 3 colonnes -->
<table style="width: 100%; border-collapse: collapse;">
<tr>
<!-- Colonne 1: GitHub Stats -->
<td style="width: 33%; vertical-align: top; padding: 10px;">
<img src="https://github-readme-stats.vercel.app/api?username=Krapaud&show_icons=true&theme=tokyonight&hide_border=true&count_private=true&include_all_commits=true&line_height=20&card_width=300&title_color=58A6FF&icon_color=1F6FEB&text_color=C9D1D9&bg_color=0D1117&border_radius=8" alt="GitHub Stats"/>
</td>

<!-- Colonne 2: Top Languages -->
<td style="width: 33%; vertical-align: top; padding: 10px;">
<img src="https://github-readme-stats.vercel.app/api/top-langs/?username=Krapaud&layout=compact&theme=tokyonight&hide_border=true&langs_count=6&card_width=300&title_color=58A6FF&text_color=C9D1D9&bg_color=0D1117&border_radius=8" alt="Top Languages"/>
</td>

<!-- Colonne 3: Streak Stats -->
<td style="width: 33%; vertical-align: top; padding: 10px;">
<img src="https://github-readme-streak-stats.herokuapp.com/?user=Krapaud&theme=tokyonight&hide_border=true&stroke=58A6FF&ring=1F6FEB&fire=FF6B6B&currStreakLabel=58A6FF&background=0D1117&border_radius=8" alt="GitHub Streak"/>
</td>
</tr>
</table>

<!-- Activity Graph pleine largeur mais plus compact -->
<div style="margin: 15px 0;">
<img width="100%" src="https://github-readme-activity-graph.vercel.app/graph?username=Krapaud&bg_color=0D1117&color=C9D1D9&line=58A6FF&point=1F6FEB&area=true&hide_border=true&custom_title=📊%20Contribution%20Activity&radius=8&height=300" alt="Activity Graph"/>
</div>

<!-- Métriques détaillées compactes en tableau horizontal -->
<details>
<summary><strong>📈 Detailed Metrics</strong> (Click to expand)</summary>
<br>
<table style="width: 100%; margin: 10px 0;">
<tr style="background: rgba(88, 166, 255, 0.1);">
<td style="padding: 8px; text-align: center;"><strong>📚 Repos:</strong> 13</td>
<td style="padding: 8px; text-align: center;"><strong>⭐ Stars:</strong> 2</td>
<td style="padding: 8px; text-align: center;"><strong>👥 Followers:</strong> 4</td>
<td style="padding: 8px; text-align: center;"><strong>📅 Days:</strong> 2111</td>
</tr>
</table>

<!-- Badges de performance et langages en ligne -->
<div style="margin: 10px 0;">
<img src="https://img.shields.io/badge/dynamic/json?color=brightgreen&label=Commits%202025&query=%24.total_count&url=https%3A%2F%2Fapi.github.com%2Fsearch%2Fcommits%3Fq%3Dauthor%3AKrapaud%2Bauthor-date%3A2025-01-01..2025-12-31&style=flat-square&logo=git" alt="Commits 2025"/>
<img src="https://img.shields.io/badge/C-5%20repos-00599C?style=flat-square&logo=c" alt="C"/>
<img src="https://img.shields.io/badge/Shell-3%20repos-4EAA25?style=flat-square&logo=gnu-bash" alt="Shell"/>
<img src="https://img.shields.io/badge/Python-1%20repo-3776AB?style=flat-square&logo=python" alt="Python"/>
</div>
</details>

<!-- Footer compact -->
<div style="margin: 10px 0; padding: 8px; background: rgba(88, 166, 255, 0.05); border-radius: 8px;">
<sub>🔄 <em>Auto-updated • Last sync: <!--STATS_UPDATE_TIME-->23/08/2025 à 14:13 UTC<!--/STATS_UPDATE_TIME--></em></sub>
</div>

</div>

'''
    return compact_stats

def replace_github_stats_section():
    """Remplace la section GitHub Statistics par une version compacte"""
    
    try:
        # Lire le fichier README actuel
        with open('README.md', 'r', encoding='utf-8') as f:
            content = f.read()
        
        # Trouver le début et la fin de la section GitHub Statistics
        start_marker = "## 📊 GitHub Statistics"
        end_marker = "## 🏆 Developer Achievements & Milestones"
        
        start_pos = content.find(start_marker)
        end_pos = content.find(end_marker)
        
        if start_pos == -1 or end_pos == -1:
            print("❌ Impossible de trouver les marqueurs de début/fin de section")
            return False
        
        # Remplacer la section
        new_stats = create_compact_stats()
        new_content = content[:start_pos] + new_stats + "\n" + content[end_pos:]
        
        # Écrire le nouveau contenu
        with open('README.md', 'w', encoding='utf-8') as f:
            f.write(new_content)
        
        print("✅ Section GitHub Statistics remplacée par une version compacte!")
        print("📊 Nouvelle disposition:")
        print("   - Header compact avec animation simplifiée")
        print("   - 5 badges en ligne horizontale")
        print("   - Dashboard 3 colonnes (Stats | Languages | Streak)")
        print("   - Activity Graph compact")
        print("   - Métriques détaillées dans un accordéon")
        print("   - Footer simplifié")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors du remplacement: {e}")
        return False

if __name__ == "__main__":
    print("🔄 Remplacement de la section GitHub Statistics par une version compacte...")
    if replace_github_stats_section():
        print("🎉 Refonte compacte terminée avec succès!")
    else:
        print("❌ Échec de la refonte")
