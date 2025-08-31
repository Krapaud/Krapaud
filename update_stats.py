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
    
    def collect_stats(self):
        """Collect all statistics"""
        print("🔍 Collecting GitHub statistics...")
        
        repos = self.get_git_repos()
        total_commits_2025 = 0
        
        for repo in repos:
            print(f"  📂 Analyzing {repo['name']}...")
            commits_2025 = self.count_commits_2025(repo['path'])
            total_commits_2025 += commits_2025
        
        self.stats = {
            "last_updated": datetime.now().strftime("%d/%m/%Y à %H:%M UTC"),
            "total_repos": len(repos),
            "commits_2025": total_commits_2025
        }
        
        print(f"✅ Stats collected: {total_commits_2025} commits in 2025, {len(repos)} repos")
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
        
        with open(readme_path, 'w') as f:
            f.write(content)
        
        print("📝 README.md updated successfully")
    
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
            
        except Exception as e:
            print(f"❌ Error during update: {e}")
            return False
        
        return True

if __name__ == "__main__":
    updater = GitHubStatsUpdater()
    updater.run()
