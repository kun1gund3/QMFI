import os
import cv2
import torch
import numpy as np
import albumentations as A
from albumentations.pytorch import ToTensorV2
from torch.utils.data import Dataset, DataLoader
from transformers import AutoTokenizer

# 1. Hardware optimal auslasten
NUM_WORKERS = os.cpu_count()  # Nutzt alle verfügbaren CPU-Kerne für das Laden

# 2. Blitzschnelle Bild-Transformationen (Albumentations ist ca. 2x schneller als Torchvision PIL)
train_transforms = A.Compose([
    A.Resize(224, 224),
    A.HorizontalFlip(p=0.5),
    A.RandomBrightnessContrast(p=0.2),
    A.Normalize(mean=(0.485, 0.456, 0.406), std=(0.229, 0.224, 0.225)),
    ToTensorV2(),  # Konvertiert direkt in PyTorch Tensors
])

# 3. Den in Rust geschriebenen FAST Tokenizer laden
TOKENIZER_NAME = "bert-base-uncased"
tokenizer = AutoTokenizer.from_pretrained(TOKENIZER_NAME, use_fast=True)

class KaggleMultimodalDataset(Dataset):
    def __init__(self, image_paths, texts, labels, transforms):
        self.image_paths = image_paths
        self.texts = texts
        self.labels = torch.tensor(labels, dtype=torch.float32)
        self.transforms = transforms

    def __len__(self):
        return len(self.image_paths)

    def __getitem__(self, idx):
        # BILD-LADEN: cv2.imread ist massiv schneller als PIL.Image.open!
        img_path = self.image_paths[idx]
        image = cv2.imread(img_path)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        
        if self.transforms:
            image = self.transforms(image=image)["image"]
            
        # TEXT-LADEN: KEIN Padding hier! Wir übergeben nur den rohen Text.
        # Das Tokenisieren passiert parallel und dynamisch im Smart Collator.
        text = self.texts[idx]
        label = self.labels[idx]
        
        return {"image": image, "text": text, "label": label}

# 4. Der "Smart Collator" für Dynamic Padding
def multimodal_smart_collator(batch):
    """
    Diese Funktion sammelt ein Batch auf den CPU-Workers ein, 
    tokenisiert alle Texte gleichzeitig und füllt sie NUR bis zur 
    maximalen Länge DIESES Batches auf (spart bis zu 50% Rechenzeit).
    """
    images = torch.stack([item["image"] for item in batch])
    labels = torch.stack([item["label"] for item in batch])
    texts = [item["text"] for item in batch]
    
    # Batch-Tokenisierung nutzt Multithreading der HuggingFace Rust-Engine
    tokenized_text = tokenizer(
        texts,
        padding=True,          # Dynamic Padding: füllt nur bis zur längsten Sequenz im aktuellen Batch auf
        truncation=True,       # Schneidet ab, falls ein Text das Limit (z.B. 512) überschreitet
        max_length=128,        # Maximal erlaubte Obergrenze
        return_tensors="pt"    # Direkt als PyTorch Tensors ausgeben
    )
    
    return {
        "images": images,
        "input_ids": tokenized_text["input_ids"],
        "attention_mask": tokenized_text["attention_mask"],
        "labels": labels
    }

# --- BEISPIEL FÜR DIE INITIALISIERUNG ---
# Erstelle Dummy-Daten (Ersetze dies mit deinen echten Pfaden und Texten)
dummy_img_paths = ["sample_img.jpg"] * 1000  # Stelle sicher, dass die Bilder existieren
dummy_texts = ["Dies ist ein sehr kurzer Beispieltext für Kaggle."] * 1000
dummy_labels = np.random.rand(1000, 1)

# Dataset & DataLoader instanziieren
train_dataset = KaggleMultimodalDataset(dummy_img_paths, dummy_texts, dummy_labels, train_transforms)

train_loader = DataLoader(
    dataset=train_dataset,
    batch_size=64,                      # T4-GPUs lieben Zweierpotenzen (32, 64, 128)
    shuffle=True,
    num_workers=NUM_WORKERS,            # Lädt Bilder parallel
    collate_fn=multimodal_smart_collator, # Aktiviert die ultraschnelle Textverarbeitung
    pin_memory=True,                    # Ermöglicht asynchronen GPU-Transfer
    persistent_workers=True,            # Verhindert Lags zwischen den Epochen
    drop_last=True                      # Wichtig für reibungsloses Multi-GPU Training
)
