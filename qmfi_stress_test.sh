#!/bin/bash
# qmfi_stress_test.sh - Simuliert Speicherlast für QMFI-Tests

echo "Starte Speicherlast-Simulation..."
# Erzeuge eine große temporäre Datei im RAM, um MemAvailable schnell zu se>
# Wir nutzen tmpfs, falls verfügbar, oder einfach eine große Datei
TMP_FILE="$HOME/qmfi_stress_test"

echo "Phase 1: Speicher belegen (1GB)..."
dd if=/dev/zero of=$TMP_FILE bs=1M count=1024
sleep 5

echo "Phase 2: Speicher freigeben..."
rm $TMP_FILE
echo "Simulation abgeschlossen."
