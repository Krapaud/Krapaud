#!/usr/bin/env python3
"""
GitHub Stats Auto-Updater - Version robuste avec données de fallback
"""

import os
import json
import subprocess
from datetime import datetime
import re

class GitHubStatsUpdater:
    def __init__(self, username="Krapaud"):
        self.username = username
        # Détection automatique de l'environnement
        if os.getenv('GITHUB_ACTIONS') == 'true':
            # Dans GitHub Actions
            self.base_path = os.getenv('GITHUB_WORKSPACE', os.getcwd())
            self.profile_path = self.base_path
        else:
            # En local
            self.base_path = "/home/krapaud"
            self.profile_path = "/home/krapaud/perso/Krapaud"
        self.stats = {}

    def get_git_repos(self):
        """Find all local git repositories"""
        repos = []
        # Dans GitHub Actions, on analyse juste le repo courant
        if os.getenv('GITHUB_ACTIONS') == 'true':
            if os.path.exists(os.path.join(self.base_path, ".git")):
                repos.append({"name": "Krapaud", "path": self.base_path})
            return repos
        
        # En local, on cherche tous les repos
        for item in os.listdir(self.base_path):
            repo_path = os.path.join(self.base_path, item)
            if os.path.isdir(repo_path) and os.path.exists(os.path.join(repo_path, ".git")):
                repos.append({"name": item, "path": repo_path})
        return repos

    def count_commits_2025(self, repo_path):
        """Count commits in 2025 for a repository"""
        try:
            result = subprocess.run(
                ["git", "-C", repo_path, "log", "--oneline", "--since=2025-01-01"],
                capture_output=True, text=True
            )
            return len(result.stdout.strip().split('\n')) if result.stdout.strip() else 0
        except:
            return 0

    def get_current_github_stats(self):
        """Get current GitHub stats from GitHub API"""
        try:
            # Récupérer les stats utilisateur depuis l'API GitHub
            import urllib.request
            import urllib.error

            # Stats utilisateur de base
            user_url = f"https://api.github.com/users/{self.username}"
            with urllib.request.urlopen(user_url) as response:
                user_data = json.loads(response.read().decode())

            # Récupérer tous les repos pour calculer les étoiles et langages
            repos_url = f"https://api.github.com/users/{self.username}/repos?per_page=100"
            total_stars = 0
            repos_analyzed = 0
            all_languages = {}

            try:
                with urllib.request.urlopen(repos_url) as response:
                    repos_data = json.loads(response.read().decode())
                    repos_analyzed = len(repos_data)
                    total_stars = sum(repo.get('stargazers_count', 0) for repo in repos_data)

                    # Analyser les langages de chaque repository
                    for repo in repos_data:
                        languages_url = repo.get('languages_url')
                        if languages_url:
                            try:
                                with urllib.request.urlopen(languages_url) as lang_response:
                                    repo_languages = json.loads(lang_response.read().decode())
                                    for lang, bytes_count in repo_languages.items():
                                        all_languages[lang] = all_languages.get(lang, 0) + bytes_count
                            except (urllib.error.URLError, json.JSONDecodeError):
                                continue

            except (urllib.error.URLError, json.JSONDecodeError):
                total_stars = 5  # Fallback
                repos_analyzed = user_data.get('public_repos', 13)
                all_languages = {
                    'C': 45.0,
                    'Python': 25.0,
                    'JavaScript': 15.0,
                    'Shell': 10.0,
                    'HTML': 3.0,
                    'CSS': 2.0
                }

            # Convertir les bytes en pourcentages
            if all_languages:
                total_bytes = sum(all_languages.values())
                languages_percent = {}
                for lang, bytes_count in all_languages.items():
                    percentage = round((bytes_count / total_bytes) * 100, 1)
                    languages_percent[lang] = percentage
            else:
                languages_percent = {
                    'C': 45.0,
                    'Python': 25.0,
                    'JavaScript': 15.0,
                    'Shell': 10.0,
                    'HTML': 3.0,
                    'CSS': 2.0
                }

            return {
                'public_repos': user_data.get('public_repos', 13),
                'followers': user_data.get('followers', 5),
                'following': user_data.get('following', 7),
                'total_stars': total_stars,
                'languages': languages_percent,
                'repos_analyzed': repos_analyzed
            }
        except (urllib.error.URLError, json.JSONDecodeError, KeyError) as e:
            print(f"⚠️ Erreur lors de la récupération des stats GitHub: {e}")
            # Fallback avec des données par défaut mises à jour
            return {
                'public_repos': 13,
                'followers': 5,
                'following': 7,
                'total_stars': 5,
                'languages': {
                    'C': 45.0,
                    'Python': 25.0,
                    'JavaScript': 15.0,
                    'Shell': 10.0,
                    'HTML': 3.0,
                    'CSS': 2.0
                },
                'repos_analyzed': 13
            }

    def evaluate_expertise_skills(self):
        """Evaluate skills based on your actual expertise"""

        # Vos compétences basées sur vos projets réels et expertise
        skills = {
            'C Programming': 100,        # Expert: Shell, Printf, Low-level
            'System Programming': 100,   # Expert: Shell implementation, système
            'Data Structures': 85,       # Avancé: Binary trees, listes
            'Algorithms': 80,           # Avancé: Sorting, recherche
            'Shell Scripting': 85,      # Avancé: Multiples projets shell
            'Python': 75,               # Solide: Projets d'apprentissage
            'Web Development': 70,      # Bon: Portfolio, jeux
            'JavaScript': 65,           # Bon: Frontend, interactivité
            'Problem Solving': 90,      # Expert: Holberton challenges
            'Git & Version Control': 85 # Avancé: Workflow développement
        }

        return skills

    def get_skill_color(self, percentage):
        """Get color based on skill percentage"""
        if percentage >= 90:
            return "brightgreen"
        elif percentage >= 80:
            return "green"
        elif percentage >= 70:
            return "yellowgreen"
        elif percentage >= 60:
            return "yellow"
        elif percentage >= 50:
            return "orange"
        else:
            return "red"

    def collect_stats(self):
        """Collect all statistics"""
        print("🚀 Collecting comprehensive GitHub statistics...")
        print("=" * 60)

        # Local repos for commit counting
        local_repos = self.get_git_repos()
        total_commits_2025 = 0

        print("📂 Analyzing local repositories for commits...")
        for repo in local_repos:
            commits_2025 = self.count_commits_2025(repo['path'])
            total_commits_2025 += commits_2025
            print(f"  • {repo['name']}: {commits_2025} commits in 2025")

        # Current GitHub stats
        github_stats = self.get_current_github_stats()

        # Expertise-based skills
        skills = self.evaluate_expertise_skills()

        self.stats = {
            "last_updated": datetime.now().strftime("%d/%m/%Y à %H:%M UTC"),
            "local_repos": len(local_repos),
            "commits_2025": total_commits_2025,
            "github_real": github_stats,
            "skills": skills
        }

        print("=" * 60)
        print("✅ Statistics collection completed!")
        print(f"📊 Summary:")
        print(f"   • Local repositories: {len(local_repos)}")
        print(f"   • Public repositories: {github_stats['public_repos']}")
        print(f"   • Followers: {github_stats['followers']}")
        print(f"   • Total stars: {github_stats['total_stars']}")
        print(f"   • Commits in 2025: {total_commits_2025}")

        print(f"🎯 Your expertise-based skills:")
        for skill, percentage in skills.items():
            color_indicator = "🔥" if percentage >= 90 else "💪" if percentage >= 80 else "⭐"
            print(f"   {color_indicator} {skill}: {percentage}%")

        return self.stats

    def save_stats_json(self):
        """Save statistics to JSON file"""
        stats_file = os.path.join(self.profile_path, "stats.json")
        with open(stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
        print(f"💾 Statistics saved to {stats_file}")

    def update_readme(self):
        """Update README.md with complete automation"""
        readme_path = os.path.join(self.profile_path, "README.md")

        with open(readme_path, 'r') as f:
            content = f.read()

        # Update timestamp
        new_timestamp = self.stats['last_updated']
        content = re.sub(
            r'<!--STATS_UPDATE_TIME-->.*?<!--/STATS_UPDATE_TIME-->',
            f'<!--STATS_UPDATE_TIME-->{new_timestamp}<!--/STATS_UPDATE_TIME-->',
            content
        )

        # Update GitHub statistics
        github_data = self.stats.get('github_real', {})

        # Repository count
        repo_count = github_data.get('public_repos', 0)
        content = re.sub(r'<strong>📚 Repos:</strong> \d+', f'<strong>📚 Repos:</strong> {repo_count}', content)
        content = re.sub(r'badge/Repos-\d+-', f'badge/Repos-{repo_count}-', content)

        # Stars count
        star_count = github_data.get('total_stars', 0)
        content = re.sub(r'<strong>⭐ Stars:</strong> \d+', f'<strong>⭐ Stars:</strong> {star_count}', content)

        # Followers count
        followers_count = github_data.get('followers', 0)
        content = re.sub(r'<strong>👥 Followers:</strong> \d+', f'<strong>👥 Followers:</strong> {followers_count}', content)

        # Commits count
        commits_2025 = self.stats.get('commits_2025', 0)
        content = re.sub(r'badge/Commits-\d+-brightgreen', f'badge/Commits-{commits_2025}-brightgreen', content)
        content = re.sub(r'badge/📊-\d+-blue', f'badge/📊-{commits_2025}-blue', content)
        content = re.sub(r'- 📈 \*\*Contributions:\*\* \d+ commits this year', f'- 📈 **Contributions:** {commits_2025} commits this year', content)

        # Update skills badges
        if 'skills' in self.stats:
            skills = self.stats['skills']

            skill_mappings = {
                'C Programming': ('C_Programming', 'c'),
                'Python': ('Python', 'python'),
                'Data Structures': ('Data_Structures', 'buffer'),
                'Algorithms': ('Algorithms', 'codeigniter'),
                'System Programming': ('System_Programming', 'linux'),
                'Web Development': ('Web_Development', 'html5'),
                'JavaScript': ('JavaScript', 'javascript'),
                'Shell Scripting': ('Shell_Scripting', 'gnu-bash')
            }

            for skill_name, (badge_name, logo) in skill_mappings.items():
                if skill_name in skills:
                    percentage = skills[skill_name]
                    color = self.get_skill_color(percentage)

                    # Update existing badge
                    pattern = rf'!\[{re.escape(skill_name)}\]\([^)]+\)'
                    replacement = f'![{skill_name}](https://img.shields.io/badge/{badge_name}-{percentage}%25-{color}?style=flat-square&logo={logo}&logoColor=white)'
                    content = re.sub(pattern, replacement, content)

        # Update programming languages badges avec les vrais pourcentages
        if 'github_real' in self.stats and 'languages' in self.stats['github_real']:
            languages = self.stats['github_real']['languages']

            # Mapping des langages vers leurs badges et logos
            language_mappings = {
                'C': ('C', '00599C', 'c'),
                'Python': ('Python', '3776AB', 'python'),
                'Shell': ('Shell', '4EAA25', 'gnu-bash'),
                'JavaScript': ('JavaScript', 'F7DF1E', 'javascript'),
                'HTML': ('HTML', 'E34F26', 'html5'),
                'CSS': ('CSS', '1572B6', 'css3'),
                'Makefile': ('Makefile', 'FF6600', 'gnu'),
                'Java': ('Java', 'ED8B00', 'java'),
                'TypeScript': ('TypeScript', '3178C6', 'typescript'),
                'Go': ('Go', '00ADD8', 'go'),
                'Rust': ('Rust', '000000', 'rust'),
                'SQL': ('SQL', '336791', 'mysql')
            }

            # Trier les langages par pourcentage pour avoir les plus importants en premier
            sorted_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)

            # Mettre à jour chaque badge de langage
            for lang, percentage in sorted_languages:
                if lang in language_mappings:
                    badge_name, color, logo = language_mappings[lang]

                    # Pattern plus flexible pour trouver les badges existants
                    patterns = [
                        # Badge standard avec le nom du langage
                        rf'<img src="[^"]*badge/{re.escape(lang)}-[^"]*"[^>]*alt="{re.escape(lang)}"[^>]*/>',
                        # Badge markdown
                        rf'!\[{re.escape(lang)}\]\([^)]+\)',
                        # Badge avec label=
                        rf'<img[^>]*label={re.escape(lang)}[^>]*/>',
                        # Badge avec alt contenant le langage
                        rf'<img[^>]*alt="{re.escape(lang)}"[^>]*badge[^>]*/>',
                        # Badge GitHub search (format spécial pour C, Shell, etc.) - pattern amélioré
                        rf'<img src="https://img\.shields\.io/github/search/[^"]*language%3A{re.escape(lang)}[^"]*"[^>]*alt="{re.escape(lang)}"[^>]*/>',
                        # Badge search avec label C - pattern plus précis
                        rf'<img src="[^"]*github/search/[^"]*language%3A{re.escape(lang)}\?[^"]*label={re.escape(lang)}[^"]*" alt="{re.escape(lang)}"[^>]*/>',
                        # Pattern spécifique pour le format exact trouvé
                        rf'<img src="https://img\.shields\.io/github/search/[^"]*language%3A{re.escape(lang)}\?[^"]*" alt="{re.escape(lang)}"[^>]*/>',
                    ]

                    # Nouveau badge avec le vrai pourcentage
                    new_badge = f'<img src="https://img.shields.io/badge/{badge_name}-{percentage}%25-{color}?style=flat-square&logo={logo}&logoColor=white" alt="{lang}"/>'

                    # Essayer chaque pattern pour remplacer
                    replaced = False
                    for pattern in patterns:
                        if re.search(pattern, content):
                            content = re.sub(pattern, new_badge, content)
                            replaced = True
                            break

                    # Si aucun badge existant trouvé pour ce langage, l'ajouter à la section des badges
                    if not replaced and percentage >= 5.0:  # Seulement pour les langages significatifs
                        # Chercher la section des badges de langages et ajouter le nouveau
                        badge_section_pattern = r'(<img src="[^"]*badge/dynamic/json[^"]*Commits%202025[^>]*/>)'
                        if re.search(badge_section_pattern, content):
                            content = re.sub(
                                badge_section_pattern,
                                f'\\1\n{new_badge}',
                                content
                            )

        with open(readme_path, 'w') as f:
            f.write(content)

        print("📝 README.md updated with comprehensive automation!")
        print("✅ All categories now auto-update:")
        print(f"   • Repository count: {repo_count}")
        print(f"   • Stars: {star_count}")
        print(f"   • Followers: {followers_count}")
        print(f"   • Commits 2025: {commits_2025}")
        print("   • All skill badges updated with real expertise levels")

    def run(self):
        """Run the complete update process"""
        print("🌟 GitHub Profile Auto-Updater - Complete Automation")
        print("=" * 60)

        try:
            self.collect_stats()
            self.save_stats_json()
            self.update_readme()

            print("=" * 60)
            print("🎉 SUCCESS! Your profile is now fully automated!")
            print("📊 Next update will run automatically via GitHub Actions")

        except Exception as e:
            print(f"❌ Error during update: {e}")
            import traceback
            traceback.print_exc()
            return False

        return True

if __name__ == "__main__":
    updater = GitHubStatsUpdater()
    updater.run()
