#!/bin/bash
LOG_FILE="$HOME/qmfi_entropy.jsonl"
INTERVAL=0.5
while true; do
    MEM_AVAILABLE=$(grep MemAvailable /proc/meminfo | awk '{print $2}')
    TIMESTAMP=$(date -u +%s.%3N)
    printf '{"timestamp": %s, "mem_available_kb": %s}
' "$TIMESTAMP" "$MEM_AVAILABLE" >> "$LOG_FILE"
    sleep $INTERVAL
done
