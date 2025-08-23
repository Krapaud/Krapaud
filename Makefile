# Makefile pour automatiser les tâches du profil GitHub

.PHONY: help stats update commit push all clean test

# Couleurs pour l'affichage
BLUE=\033[0;34m
GREEN=\033[0;32m
YELLOW=\033[1;33m
RED=\033[0;31m
NC=\033[0m # No Color

help: ## Afficher l'aide
	@echo "$(BLUE)🚀 Commandes disponibles pour le profil GitHub :$(NC)"
	@echo ""
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "$(GREEN)%-15s$(NC) %s\n", $$1, $$2}'
	@echo ""
	@echo "$(YELLOW)📝 Exemples d'utilisation :$(NC)"
	@echo "  make stats     # Met à jour les statistiques"
	@echo "  make commit    # Commit et push automatique"
	@echo "  make all       # Stats + commit + push"

stats: ## Mettre à jour les statistiques GitHub
	@echo "$(BLUE)📊 Mise à jour des statistiques GitHub...$(NC)"
	@python3 update_stats.py
	@echo "$(GREEN)✅ Statistiques mises à jour !$(NC)"

update: stats ## Alias pour stats
	@echo "$(GREEN)✅ Mise à jour terminée !$(NC)"

test: ## Tester les connexions et APIs
	@echo "$(BLUE)🔍 Test des connexions...$(NC)"
	@python3 -c "import requests; r = requests.get('https://api.github.com/users/Krapaud'); print('✅ API GitHub OK' if r.status_code == 200 else '❌ API GitHub KO')"
	@python3 -c "import requests; r = requests.get('https://github-readme-stats.vercel.app/api?username=Krapaud'); print('✅ GitHub Stats Widget OK' if r.status_code == 200 else '❌ GitHub Stats Widget KO')"
	@echo "$(GREEN)✅ Tests terminés !$(NC)"

commit: ## Committer les changements avec un message automatique
	@echo "$(BLUE)📝 Commit des changements...$(NC)"
	@git add .
	@git commit -m "🤖 Mise à jour automatique des statistiques - $(shell date '+%d/%m/%Y %H:%M')" || echo "$(YELLOW)⚠️  Aucun changement à committer$(NC)"
	@echo "$(GREEN)✅ Commit effectué !$(NC)"

push: ## Pousser les changements vers GitHub
	@echo "$(BLUE)🚀 Push vers GitHub...$(NC)"
	@git push origin main
	@echo "$(GREEN)✅ Push effectué !$(NC)"

all: stats commit push ## Mettre à jour stats, committer et pousser
	@echo "$(GREEN)🎉 Toutes les opérations terminées avec succès !$(NC)"

clean: ## Nettoyer les fichiers temporaires
	@echo "$(BLUE)🧹 Nettoyage des fichiers temporaires...$(NC)"
	@rm -f *.log *.tmp stats_update.md *.backup
	@find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
	@find . -name "*.pyc" -delete 2>/dev/null || true
	@echo "$(GREEN)✅ Nettoyage terminé !$(NC)"

status: ## Afficher le statut Git
	@echo "$(BLUE)📋 Statut Git :$(NC)"
	@git status --short || echo "$(RED)❌ Pas un repository Git$(NC)"

info: ## Afficher les informations du profil
	@echo "$(BLUE)ℹ️  Informations du profil GitHub :$(NC)"
	@echo "$(GREEN)👤 Utilisateur :$(NC) Krapaud"
	@echo "$(GREEN)📁 Repository :$(NC) $(shell basename `git rev-parse --show-toplevel` 2>/dev/null || echo 'Non-Git')"
	@echo "$(GREEN)🌿 Branche :$(NC) $(shell git branch --show-current 2>/dev/null || echo 'N/A')"
	@echo "$(GREEN)📊 Dernière mise à jour :$(NC) $(shell git log -1 --format=%cd --date=format:'%d/%m/%Y %H:%M' 2>/dev/null || echo 'N/A')"

setup: ## Configuration initiale du repository
	@echo "$(BLUE)⚙️  Configuration initiale...$(NC)"
	@chmod +x update_stats.py
	@echo "$(GREEN)✅ Script Python exécutable$(NC)"
	@python3 -c "import requests" && echo "$(GREEN)✅ Module requests disponible$(NC)" || echo "$(RED)❌ Module requests manquant - Installer avec: pip3 install requests$(NC)"
	@echo "$(GREEN)✅ Configuration terminée !$(NC)"

# Tâche par défaut
default: help
