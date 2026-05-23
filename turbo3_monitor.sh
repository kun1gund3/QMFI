#!/bin/bash
# turbo3_monitor.sh - ERA-basiertes Quirk-Monitoring für S20 FE

LOG_FILE="$HOME/turbo3_metrics.json"
STATE_FILE="$HOME/turbo3_state.json"
# S20 FE Limit: Wir wollen unter 4.5GB für den llama-Prozess bleiben
RAM_LIMIT_MB=4500
CHECK_INTERVAL=2

update_state() {
    local mem=$1
    local quirk="none"
    local dfts_mode="standard"

    # Quirk-Logik: Identifikation von Speicher-Anomalien
    if [ "$mem" -gt "$RAM_LIMIT_MB" ]; then
        quirk="critical_ram_spike"
        dfts_mode="molecular_compression" # Signal für DFTS-Skalierung
    elif [ "$mem" -gt 3500 ]; then
        quirk="high_pressure"
        dfts_mode="optimized"
    fi

    # Erstelle Status-Datei für Agent-Zero
    echo "{\"timestamp\":\"$(date -u +%Y-%m-%dT%H:%M:%SZ)\", \"mem_usage_mb\":$mem, \"quirk\":\"$quirk\", \"dfts_mode\":\"$dfts_mode\"}" > "$STATE_FIL>
}

echo "Turbo3 ERA Monitor gestartet. RAM-Limit: ${RAM_LIMIT_MB}MB"

while true; do
    # Speicherverbrauch von llama-server ermitteln (in MB)
    # Nutzt 'ps' um den RSS (Resident Set Size) Wert zu lesen
    MEM_USAGE=$(ps -o rss= -C llama-server 2>/dev/null | awk '{sum+=$1} END {print int(sum/1024)}')

    if [ -z "$MEM_USAGE" ] || [ "$MEM_USAGE" -eq 0 ]; then
        MEM_USAGE=0
        STATUS="llama_offline"
    else
        STATUS="active"
    fi

    update_state "$MEM_USAGE"

    # Loggen für spätere empirische Analyse
    echo "{\"time\":\"$(date)\", \"mem\":$MEM_USAGE, \"status\":\"$STATUS\"}" >> "$LOG_FILE"

    # Konsolen-Output für Debugging
    if [ "$MEM_USAGE" -gt "$RAM_LIMIT_MB" ]; then
        echo "!!! QUIRK DETEKTIERT: Speicher bei ${MEM_USAGE}MB. DFTS molekulare Kompression angefordert."
    fi

    sleep "$CHECK_INTERVAL"
done
