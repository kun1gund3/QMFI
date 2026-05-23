import json
import time
import subprocess
import requests
import collections

# Konfiguration
LOG_FILE = "/data/data/com.termux/files/home/qmfi_entropy.jsonl"
LLM_URL = "http://127.0.0.1:8080/v1/chat/completions" # Anpassung an lokales LLM
WINDOW_SIZE = 5  # Anzahl der Datenpunkte für die Gradientenberechnung
MEM_THRESHOLD = 50000  # kB Änderungsrate pro Sekunde als Schwelle

def send_to_llm(phase):
    """Informiert das lokale LLM über einen bevorstehenden Phasenwechsel."""
    payload = {
        "model": "LLM_NAME_MODEL",
        "messages": [{"role": "user", "content": f"QMFI_SIGNAL: PREPARE_PHASE_SH>
    }
    try:
        requests.post(LLM_URL, json=payload, timeout=0.5)
        print(f"Signal gesendet: {phase}")
    except Exception as e:
        print(f"Fehler beim Senden an LLM: {e}")

def calculate_velocity(data_points):
    """Berechnet die Änderungsrate des Speichers."""
    if len(data_points) < 2:
        return 0

    # Vereinfachte Berechnung der Velocity: (neuester - ältester) / Zeitdifferenz
    delta_mem = data_points[-1]['mem_available_kb'] - data_points[0]['mem_availa>
    delta_time = data_points[-1]['timestamp'] - data_points[0]['timestamp']

    if delta_time == 0:
        return 0

    return delta_mem / delta_time

def main():
    print("QMFI Antizipator gestartet...")
    data_buffer = collections.deque(maxlen=WINDOW_SIZE)

    # Verfolgen der Log-Datei
    process = subprocess.Popen(['tail', '-f', LOG_FILE], stdout=subprocess.PIPE,>

    for line in process.stdout:
        try:
            entry = json.loads(line)
            data_buffer.append(entry)

            if len(data_buffer) == WINDOW_SIZE:
                velocity = calculate_velocity(list(data_buffer))

                # Einfache Logik für Phasenwechsel
                if velocity < -MEM_THRESHOLD: # Speicher sinkt schnell
                    send_to_llm("CRITICAL_PRESSURE")
                elif velocity > MEM_THRESHOLD: # Speicher steigt schnell (Freiga>
                    send_to_llm("RECOVERY")

        except json.JSONDecodeError:
            continue

if __name__ == "__main__":
    main()
