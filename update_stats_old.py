#!/usr/bin/env python3
"""
GitHub Stats Auto-Updater - Version complète
Automatically updates GitHub statistics in README.md and stats.json
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
        """Find all git repositories"""
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
    
    def analyze_skills_from_repos(self, repos):
        """Analyze skills based on repository content and projects"""
        skills_analysis = {
            'C Programming': {'files': 0, 'repos': [], 'weight': 0},
            'Data Structures': {'files': 0, 'repos': [], 'weight': 0},
            'Algorithms': {'files': 0, 'repos': [], 'weight': 0},
            'Python': {'files': 0, 'repos': [], 'weight': 0},
            'Shell Scripting': {'files': 0, 'repos': [], 'weight': 0},
            'Web Development': {'files': 0, 'repos': [], 'weight': 0}
        }
        
        # Keywords pour identifier les concepts
        data_structures_keywords = [
            'linked_list', 'binary_tree', 'hash_table', 'doubly_linked',
            'singly_linked', 'stack', 'queue', 'graph', 'tree'
        ]
        
        algorithms_keywords = [
            'sort', 'search', 'algorithm', 'recursion', 'sorting',
            'bubble_sort', 'merge_sort', 'quick_sort', 'binary_search'
        ]
        
        web_keywords = [
            'html', 'css', 'javascript', 'web', 'http', 'server', 'client'
        ]
        
        for repo in repos:
            repo_name = repo['name'].lower()
            repo_path = repo['path']
            
            try:
                # Analyser les fichiers dans le dépôt
                for root, dirs, files in os.walk(repo_path):
                    if '.git' in root:
                        continue
                        
                    for file in files:
                        file_path = os.path.join(root, file)
                        file_ext = os.path.splitext(file)[1].lower()
                        file_name = file.lower()
                        
                        # C Programming
                        if file_ext in ['.c', '.h']:
                            skills_analysis['C Programming']['files'] += 1
                            if repo['name'] not in skills_analysis['C Programming']['repos']:
                                skills_analysis['C Programming']['repos'].append(repo['name'])
                        
                        # Python
                        elif file_ext in ['.py']:
                            skills_analysis['Python']['files'] += 1
                            if repo['name'] not in skills_analysis['Python']['repos']:
                                skills_analysis['Python']['repos'].append(repo['name'])
                        
                        # Shell Scripting
                        elif file_ext in ['.sh']:
                            skills_analysis['Shell Scripting']['files'] += 1
                            if repo['name'] not in skills_analysis['Shell Scripting']['repos']:
                                skills_analysis['Shell Scripting']['repos'].append(repo['name'])
                        
                        # Web Development
                        elif file_ext in ['.html', '.css', '.js']:
                            skills_analysis['Web Development']['files'] += 1
                            if repo['name'] not in skills_analysis['Web Development']['repos']:
                                skills_analysis['Web Development']['repos'].append(repo['name'])
                
                # Analyser le nom du dépôt pour les concepts
                for keyword in data_structures_keywords:
                    if keyword in repo_name:
                        skills_analysis['Data Structures']['weight'] += 10
                        if repo['name'] not in skills_analysis['Data Structures']['repos']:
                            skills_analysis['Data Structures']['repos'].append(repo['name'])
                
                for keyword in algorithms_keywords:
                    if keyword in repo_name:
                        skills_analysis['Algorithms']['weight'] += 10
                        if repo['name'] not in skills_analysis['Algorithms']['repos']:
                            skills_analysis['Algorithms']['repos'].append(repo['name'])
                
                for keyword in web_keywords:
                    if keyword in repo_name:
                        skills_analysis['Web Development']['weight'] += 10
                        if repo['name'] not in skills_analysis['Web Development']['repos']:
                            skills_analysis['Web Development']['repos'].append(repo['name'])
                            
            except Exception as e:
                print(f"    ⚠️  Error analyzing {repo['name']}: {e}")
                continue
        
        return skills_analysis
    
    def calculate_skill_percentages(self, skills_analysis):
        """Calculate skill percentages based on analysis"""
        max_files = max([data['files'] for data in skills_analysis.values()]) or 1
        max_weight = max([data['weight'] for data in skills_analysis.values()]) or 1
        
        skill_percentages = {}
        
        for skill, data in skills_analysis.items():
            if skill in ['C Programming', 'Python', 'Shell Scripting', 'Web Development']:
                # Basé sur le nombre de fichiers (60%) + nombre de repos (40%)
                file_score = min(100, (data['files'] / max_files) * 100) if max_files > 0 else 0
                repo_score = min(100, len(data['repos']) * 15)  # 15% par repo
                percentage = int((file_score * 0.6) + (repo_score * 0.4))
            else:
                # Pour Data Structures et Algorithms, basé sur les mots-clés + repos
                weight_score = min(100, (data['weight'] / max_weight) * 100) if max_weight > 0 else 0
                repo_score = min(100, len(data['repos']) * 20)  # 20% par repo
                percentage = int((weight_score * 0.5) + (repo_score * 0.5))
            
            # Assurer un minimum pour les compétences identifiées
            if len(data['repos']) > 0 and percentage < 30:
                percentage = 30
            
            skill_percentages[skill] = max(0, min(100, percentage))
        
        return skill_percentages
    
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
        print("🔍 Collecting GitHub statistics...")
        
        repos = self.get_git_repos()
        total_commits_2025 = 0
        
        for repo in repos:
            print(f"  📂 Analyzing {repo['name']}...")
            commits_2025 = self.count_commits_2025(repo['path'])
            total_commits_2025 += commits_2025
        
        # Analyser les compétences
        print("🎯 Analyzing skills from repositories...")
        skills_analysis = self.analyze_skills_from_repos(repos)
        skill_percentages = self.calculate_skill_percentages(skills_analysis)
        
        self.stats = {
            "last_updated": datetime.now().strftime("%d/%m/%Y à %H:%M UTC"),
            "total_repos": len(repos),
            "commits_2025": total_commits_2025,
            "skills": skill_percentages,
            "skills_analysis": skills_analysis
        }
        
        print(f"✅ Stats collected: {total_commits_2025} commits in 2025, {len(repos)} repos")
        print("📊 Skills calculated:")
        for skill, percentage in skill_percentages.items():
            if percentage > 0:
                print(f"   • {skill}: {percentage}%")
        
        return self.stats
    
    def save_stats_json(self):
        """Save statistics to JSON file"""
        stats_file = os.path.join(self.profile_path, "stats.json")
        with open(stats_file, 'w') as f:
            json.dump(self.stats, f, indent=2)
        print(f"💾 Statistics saved to {stats_file}")
    
    def update_readme(self):
        """Update README.md with new statistics"""
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
        
        # Update Skills Progress badges
        if 'skills' in self.stats:
            skills = self.stats['skills']
            
            # C Programming
            if 'C Programming' in skills:
                percentage = skills['C Programming']
                color = self.get_skill_color(percentage)
                content = re.sub(
                    r'!\[C Programming\]\(https://img\.shields\.io/badge/C_Programming-\d+%25-\w+\?[^)]*\)',
                    f'![C Programming](https://img.shields.io/badge/C_Programming-{percentage}%25-{color}?style=flat-square&logo=c&logoColor=white)',
                    content
                )
            
            # Python
            if 'Python' in skills:
                percentage = skills['Python']
                color = self.get_skill_color(percentage)
                content = re.sub(
                    r'!\[Python\]\(https://img\.shields\.io/badge/Python-\d+%25-\w+\?[^)]*\)',
                    f'![Python](https://img.shields.io/badge/Python-{percentage}%25-{color}?style=flat-square&logo=python&logoColor=white)',
                    content
                )
            
            # Data Structures
            if 'Data Structures' in skills:
                percentage = skills['Data Structures']
                color = self.get_skill_color(percentage)
                content = re.sub(
                    r'!\[Data Structures\]\(https://img\.shields\.io/badge/Data_Structures-\d+%25-\w+\?[^)]*\)',
                    f'![Data Structures](https://img.shields.io/badge/Data_Structures-{percentage}%25-{color}?style=flat-square&logo=buffer&logoColor=white)',
                    content
                )
            
            # Algorithms
            if 'Algorithms' in skills:
                percentage = skills['Algorithms']
                color = self.get_skill_color(percentage)
                content = re.sub(
                    r'!\[Algorithms\]\(https://img\.shields\.io/badge/Algorithms-\d+%25-\w+\?[^)]*\)',
                    f'![Algorithms](https://img.shields.io/badge/Algorithms-{percentage}%25-{color}?style=flat-square&logo=codeigniter&logoColor=white)',
                    content
                )
        
        with open(readme_path, 'w') as f:
            f.write(content)
        
        print("📝 README.md updated successfully")
        if 'skills' in self.stats:
            print("🎯 Skills Progress badges updated automatically")
    
    def run(self):
        """Run the complete update process"""
        print("🚀 Starting GitHub Stats Auto-Update...")
        print("=" * 50)
        
        try:
            self.collect_stats()
            self.save_stats_json()
            self.update_readme()
            
            print("=" * 50)
            print("✅ Auto-update completed successfully!")
            print(f"📊 Summary:")
            print(f"   • Total repositories: {self.stats['total_repos']}")
            print(f"   • Commits in 2025: {self.stats['commits_2025']}")
            print(f"   • Last updated: {self.stats['last_updated']}")
            if 'skills' in self.stats:
                print(f"📈 Skills automatically calculated:")
                for skill, percentage in self.stats['skills'].items():
                    if percentage > 0:
                        print(f"   • {skill}: {percentage}%")
            
        except Exception as e:
            print(f"❌ Error during update: {e}")
            return False
        
        return True

if __name__ == "__main__":
    updater = GitHubStatsUpdater()
    updater.run()
