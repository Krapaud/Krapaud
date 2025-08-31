#!/bin/bash
# GitHub Stats Auto-Update Script
# À exécuter via crontab pour mise à jour automatique

cd /home/krapaud/Krapaud

# Log file
LOG_FILE="/home/krapaud/Krapaud/update_stats.log"

echo "$(date): Starting GitHub stats update..." >> "$LOG_FILE"

# Exécuter le script Python
python3 update_stats.py >> "$LOG_FILE" 2>&1

# Si on est dans un dépôt git, commit et push
if [ -d ".git" ]; then
    git add . >> "$LOG_FILE" 2>&1
    git commit -m "🔄 Auto-update GitHub stats - $(date +'%Y-%m-%d %H:%M UTC')" >> "$LOG_FILE" 2>&1
    git push >> "$LOG_FILE" 2>&1
fi

echo "$(date): GitHub stats update completed." >> "$LOG_FILE"
