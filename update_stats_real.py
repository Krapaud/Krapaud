#!/usr/bin/env python3
"""
GitHub Stats Auto-Updater - Version API GitHub réelle
Utilise les vraies données de l'API GitHub pour des statistiques précises
"""

import os
import json
import subprocess
import requests
from datetime import datetime
import re

class GitHubStatsUpdater:
    def __init__(self, username="Krapaud"):
        self.username = username
        self.base_path = "/home/krapaud"
        self.profile_path = "/home/krapaud/Krapaud"
        self.stats = {}
        
    def get_git_repos(self):
        """Find all local git repositories"""
        repos = []
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
    
    def get_github_real_stats(self):
        """Get REAL comprehensive stats from GitHub API"""
        try:
            base_url = "https://api.github.com"
            
            print("🌐 Fetching real GitHub statistics...")
            
            # User info
            user_response = requests.get(f"{base_url}/users/{self.username}")
            user_data = user_response.json()
            
            # Repositories (including public and private if accessible)
            repos_response = requests.get(f"{base_url}/users/{self.username}/repos?per_page=100&type=all")
            repos_data = repos_response.json()
            
            # Calculate REAL language statistics from GitHub API
            languages_total = {}
            total_bytes = 0
            repo_count = 0
            
            print("📊 Analyzing language distribution from GitHub...")
            for repo in repos_data:
                if repo.get('fork'):  # Skip forked repos
                    continue
                    
                repo_count += 1
                try:
                    lang_response = requests.get(f"{base_url}/repos/{self.username}/{repo['name']}/languages")
                    if lang_response.status_code == 200:
                        lang_data = lang_response.json()
                        for lang, bytes_count in lang_data.items():
                            languages_total[lang] = languages_total.get(lang, 0) + bytes_count
                            total_bytes += bytes_count
                        print(f"  ✅ {repo['name']}: {list(lang_data.keys())}")
                    else:
                        print(f"  ⚠️  {repo['name']}: No access to languages")
                except Exception as e:
                    print(f"  ❌ {repo['name']}: Error - {e}")
                    continue
            
            # Convert to percentages (REAL GitHub percentages)
            language_percentages = {}
            if total_bytes > 0:
                for lang, bytes_count in languages_total.items():
                    percentage = round((bytes_count / total_bytes) * 100, 2)
                    language_percentages[lang] = percentage
            
            # Sort languages by percentage
            sorted_languages = dict(sorted(language_percentages.items(), key=lambda x: x[1], reverse=True))
            
            return {
                'public_repos': user_data.get('public_repos', 0),
                'followers': user_data.get('followers', 0),
                'following': user_data.get('following', 0),
                'total_stars': sum(repo.get('stargazers_count', 0) for repo in repos_data if not repo.get('fork')),
                'languages': sorted_languages,
                'repos_analyzed': repo_count,
                'user_data': user_data
            }
        except Exception as e:
            print(f"❌ Error fetching GitHub API stats: {e}")
            return {
                'public_repos': 0, 'followers': 0, 'following': 0, 
                'total_stars': 0, 'languages': {}, 'repos_analyzed': 0
            }
    
    def convert_github_languages_to_skills(self, github_languages):
        """Convert GitHub language percentages to skill badges"""
        
        # Map GitHub languages to skill categories
        skill_mapping = {
            'C': ['C Programming', 'Data Structures', 'Algorithms'],
            'Python': ['Python'],
            'JavaScript': ['Web Development', 'JavaScript'],
            'HTML': ['Web Development', 'Frontend'],
            'CSS': ['Web Development', 'Frontend'],
            'Shell': ['Shell Scripting', 'DevOps'],
            'TypeScript': ['Web Development', 'JavaScript'],
            'Java': ['Java Programming'],
            'C++': ['C++ Programming', 'Data Structures', 'Algorithms']
        }
        
        skills = {}
        
        # Initialize all skills
        all_skills = set()
        for lang_skills in skill_mapping.values():
            all_skills.update(lang_skills)
        
        for skill in all_skills:
            skills[skill] = 0
        
        # Calculate skill percentages based on GitHub languages
        for lang, percentage in github_languages.items():
            if lang in skill_mapping:
                for skill in skill_mapping[lang]:
                    # Distribute percentage among related skills
                    if skill in ['C Programming', 'Python', 'JavaScript']:
                        # Direct language skills get full percentage
                        skills[skill] = max(skills[skill], int(percentage))
                    elif skill in ['Data Structures', 'Algorithms']:
                        # These skills benefit from C programming
                        if lang == 'C':
                            skills[skill] = max(skills[skill], int(percentage * 0.8))
                    elif skill in ['Web Development', 'Frontend']:
                        # Web skills from HTML/CSS/JS
                        if lang in ['HTML', 'CSS', 'JavaScript', 'TypeScript']:
                            skills[skill] = max(skills[skill], int(percentage * 0.7))
                    elif skill in ['Shell Scripting', 'DevOps']:
                        # Shell skills
                        if lang == 'Shell':
                            skills[skill] = max(skills[skill], int(percentage * 2))  # Boost shell
        
        # Ensure minimum values for detected skills and reasonable maximums
        for skill, value in skills.items():
            if value > 0:
                skills[skill] = max(15, min(100, value))  # Min 15%, Max 100%
        
        return {k: v for k, v in skills.items() if v > 0}  # Only return skills with values > 0
    
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
        """Collect all statistics using REAL GitHub data"""
        print("🚀 Starting REAL GitHub stats collection...")
        print("=" * 60)
        
        # Local repos for commit counting
        local_repos = self.get_git_repos()
        total_commits_2025 = 0
        
        print("📂 Analyzing local repositories for commits...")
        for repo in local_repos:
            commits_2025 = self.count_commits_2025(repo['path'])
            total_commits_2025 += commits_2025
            print(f"  • {repo['name']}: {commits_2025} commits in 2025")
        
        # Real GitHub API stats
        github_stats = self.get_github_real_stats()
        
        # Convert GitHub languages to skills
        skills = self.convert_github_languages_to_skills(github_stats['languages'])
        
        self.stats = {
            "last_updated": datetime.now().strftime("%d/%m/%Y à %H:%M UTC"),
            "local_repos": len(local_repos),
            "commits_2025": total_commits_2025,
            "github_real": github_stats,
            "skills": skills
        }
        
        print("=" * 60)
        print("✅ REAL GitHub statistics collected!")
        print(f"📊 GitHub Summary:")
        print(f"   • Public repositories: {github_stats['public_repos']}")
        print(f"   • Followers: {github_stats['followers']}")
        print(f"   • Total stars: {github_stats['total_stars']}")
        print(f"   • Commits in 2025: {total_commits_2025}")
        
        print(f"🔥 REAL Language distribution:")
        for lang, percentage in list(github_stats['languages'].items())[:6]:
            print(f"   • {lang}: {percentage}%")
            
        print(f"🎯 Calculated skills:")
        for skill, percentage in skills.items():
            print(f"   • {skill}: {percentage}%")
        
        return self.stats
    
    def save_stats_json(self):
        """Save statistics to JSON file"""
        stats_file = os.path.join(self.profile_path, "stats.json")
        with open(stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
        print(f"💾 Statistics saved to {stats_file}")
    
    def update_readme(self):
        """Update README.md with REAL statistics"""
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
        
        # Update commit count
        content = re.sub(
            r'badge/Commits-\d+-brightgreen',
            f"badge/Commits-{self.stats['commits_2025']}-brightgreen",
            content
        )
        
        content = re.sub(
            r'badge/📊-\d+-blue',
            f"badge/📊-{self.stats['commits_2025']}-blue",
            content
        )
        
        # Update Skills Progress badges with REAL data
        if 'skills' in self.stats:
            skills = self.stats['skills']
            
            # Update each skill badge
            skill_badges = {
                'C Programming': ('C_Programming', 'c'),
                'Python': ('Python', 'python'),
                'Data Structures': ('Data_Structures', 'buffer'),
                'Algorithms': ('Algorithms', 'codeigniter'),
                'Web Development': ('Web_Development', 'html5'),
                'JavaScript': ('JavaScript', 'javascript')
            }
            
            for skill_name, (badge_name, logo) in skill_badges.items():
                if skill_name in skills:
                    percentage = skills[skill_name]
                    color = self.get_skill_color(percentage)
                    
                    # Update the specific badge
                    pattern = rf'!\[{skill_name.replace(" ", r"\s")}\]\(https://img\.shields\.io/badge/{badge_name}-\d+%25-\w+\?[^)]*\)'
                    replacement = f'![{skill_name}](https://img.shields.io/badge/{badge_name}-{percentage}%25-{color}?style=flat-square&logo={logo}&logoColor=white)'
                    
                    content = re.sub(pattern, replacement, content)
        
        with open(readme_path, 'w') as f:
            f.write(content)
        
        print("📝 README.md updated with REAL GitHub data!")
    
    def run(self):
        """Run the complete update process with REAL GitHub data"""
        print("🌟 GitHub Stats Auto-Updater - REAL DATA VERSION")
        print("=" * 60)
        
        try:
            self.collect_stats()
            self.save_stats_json()
            self.update_readme()
            
            print("=" * 60)
            print("🎉 SUCCESS! Your stats now reflect REAL GitHub data!")
            
        except Exception as e:
            print(f"❌ Error during update: {e}")
            return False
        
        return True

if __name__ == "__main__":
    updater = GitHubStatsUpdater()
    updater.run()
