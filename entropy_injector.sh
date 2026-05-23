#!/bin/bash
# 🌊 QMFI Entropy-Injector V1.0 - "The Vibration"
# Zweck: Erzeugung kontrollierter Hardware-Entropie auf dem S20 FE.

echo "--- 🧠 QMFI ENTROPY INJECTOR GESTARTET ---"
echo "Ziel: Messung der Flow-Integrity unter Ressourcen-Druck."

# Speicher für die PIDs der RAM-Fresser
PIDS=""

cleanup() {
    echo -e "\n\n--- 🧹 Bereinige Entropie (System-Stabilisierung) ---"
    kill $PIDS 2>/dev/null
    echo "Alle Störsignale gestoppt. Fluss kehrt zur Baseline zurück."
    exit
}

# Sicherstellen, dass bei Abbruch alles gelöscht wird
trap cleanup SIGINT

while true; do
    echo ""
    echo "1) [+] Entropie erhöhen (256MB RAM Chunk)"
    echo "2) [!] CPU-Vibration (5s Pulse)"
    echo "3) [0] System stabilisieren (Reset)"
    echo "4) [x] Cleanup"
    read -p "Aktion wählen: " choice

    case $choice in
        1)
            # Nutzt Python, um sauber Speicher zu belegen
            echo "Injektiere 256MB RAM-Entropie..."
            python3 -c "import time; x = ' ' * (1024 * 1024 * 256); time.sleep(3>
            PID=$!
            PIDS="$PIDS $PID"
            echo "Aktiver Druck: $(echo $PIDS | wc -w) Einheiten."
            ;;
        2)
            echo "Erzeuge CPU-Vibration (Load Spike)..."
            timeout 5s yes > /dev/null &
            ;;
        3)
            kill $PIDS 2>/dev/null
            PIDS=""
            echo "Entropie-Reset durchgeführt."
            ;;
        4)
            cleanup
            ;;
        *)
            echo "Ungültige Eingabe."
            ;;
    esac
done
