# QMFI - Die Topologie des Safetensors-Formats

Dieses Format ist das "Gefäß" für unsere Majorana-Inferenz. Es trennt 
strikt zwischen STRUKTUR (Geist) und MASSE (Daten).

STRUKTURELLER FLUSS (Byte-Strom):
================================================================================
| DESCRIPTOR |     TOPOLOGISCHES MANIFEST (JSON)     |    BINÄRER KORPUS       |
|------------|---------------------------------------|-------------------------|
|  8 Bytes   |           N Bytes (UTF-8)             |    Payload-Horizont     |
================================================================================
      |                        |                            |
      | [DIMENSIONIERUNG]      | [MAPPING-LOGIK]            | [REINER STROM]
      └─ Definiert die         └─ Enthält Vektoren-         └─ Die tatsächlichen
         Manifest-Größe           Adressräume (Offsets)        Gewichte (Tensors)

LOGISCHE VERKNÜPFUNG (The "Zero-Copy" Bridge):
--------------------------------------------------------------------------------
Das Manifest fungiert als Schablone. Dank der OFFSETS muss die Hardware die 
Daten nicht "lesen" und "verschieben", sondern kann direkt auf den BINÄREN 
KORPUS zugreifen (Memory Mapping).

SCHEMA-BEISPIEL:
{
    "TENSOR_WEIGHTS": {
        "dtype": "TQ4_ALPHA",         // Quantisierungs-Auflösung
        "shape": [4096, 4096],         // Matrix-Geometrie
        "offsets": [1024, 10248576]    // Vektor-Anker im Payload-Horizont
    },
    "__metadata__": {
        "integrity_mode": "QMFI-V1",   // Validierungsklasse
        "entropy_source": "S20FE-HW"   // Herkunftsnachweis der Entropie
    }
}
--------------------------------------------------------------------------------
ORDNUNGSPRINZIP: "Separation of Concerns"
1. Sicherheit: Keine ausführbaren Header (Malware-Resistenz).
2. Effizienz: Direktes Streaming vom Flash in den RAM (Flow-Integrity).
3. Transparenz: Metadaten sind im Klartext lesbar.
