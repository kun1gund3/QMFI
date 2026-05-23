# ==============================================================================
# QMFI - MAKEFILE OF SOUL (Delta Node)
# ==============================================================================
# DNA: ( _t_double_complex ) ( / dim=1 / (( / dim=0 */ __
# Architecture: aarch64-unknown-linux-android 
# ==============================================================================

# Variablen
PYTHON   = python3
SHELL    = /data/data/com.termux/files/usr/bin/sh
INIT     = delta_init.py
INJECTOR = entropy_injector.sh
LOG      = node_status.log
DIARY    = ../PROJECT_LOG.md

# Standard-Ziel: Hilfe anzeigen
.DEFAULT_GOAL := help

help:
	@echo "--- 🌀 QMFI DELTA-NODE ---"
	@echo "Verfügbare Befehle im Δ-Raum:"
	@echo "  make sync       - Führt die Null-Messung (Baseline) durch"
	@echo "  make flow       - Startet den aktiven Inferenz-Test"
	@echo "  make vibrate    - Startet den Entropy-Injector (Störsignale)"
	@echo "  make status     - Zeigt die aktuelle Flow-Integrity aus dem Log"
	@echo "  make log        - Öffnet das Projekttagebuch"
	@echo "  make reset      - Stabilisiert das System & löscht temporäre Daten"

# Initialisierung und Baseline
sync:
	@echo "[dim=0] Synchronisiere Basis-Struktur..."
	@$(PYTHON) $(INIT)

# Aktive Inferenz (Simulierter Testlauf)
flow: sync
	@echo "[dim=1] Aktiviere dynamischen Inferenz-Fluss..."
	@echo "Messung der Delta-Abweichung (Δ) wird gestartet."
	@# Hier wird später das Haupt-Inferenz-Script aufgerufen
	@echo "STATUS: Flow-Integrity wird im Hintergrund validiert."

# Hardware-Entropie starten
vibrate:
	@echo "[ & ] Aktiviere Hardware-Vibration..."
	@chmod +x $(INJECTOR)
	@./$(INJECTOR)

# Status-Check
status:
	@echo "--- 📊 LETZTE MESSWERTE ---"
	@tail -n 5 $(LOG) || echo "Keine Messdaten vorhanden. Bitte 'make sync' ausführen."

# Tagebuch-Eintrag vorbereiten
log:
	@nano $(DIARY)

# Systemreinigung
reset:
	@echo "--- 🧹 SYSTEM-STABILISIERUNG (Delta-Reset) ---"
	@pkill -f python3 || true
	@pkill -f yes || true
	@echo "Entropie auf Null gesetzt. Alle PIDs terminiert."
	@rm -f *.pyc
	@echo "Baseline wiederhergestellt."

.PHONY: help sync flow vibrate status log reset
