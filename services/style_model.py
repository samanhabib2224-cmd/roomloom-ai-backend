import torch
import torch.nn as nn
from torchvision import models, datasets, transforms
from torch.utils.data import DataLoader, random_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import os
import json

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

DATASET_PATH = "dataset/style_dataset"

# =========================
# TRANSFORMS
# =========================
transform = transforms.Compose([
    transforms.Resize((224, 224)),
    transforms.RandomHorizontalFlip(),
    transforms.RandomRotation(15),
    transforms.ColorJitter(0.2, 0.2, 0.2, 0.1),
    transforms.ToTensor(),
    transforms.Normalize([0.485, 0.456, 0.406],
                         [0.229, 0.224, 0.225])
])

# =========================
# DATASET
# =========================
dataset = datasets.ImageFolder(DATASET_PATH, transform=transform)

train_size = int(0.8 * len(dataset))
val_size = len(dataset) - train_size

train_data, val_data = random_split(dataset, [train_size, val_size])

train_loader = DataLoader(train_data, batch_size=32, shuffle=True)
val_loader = DataLoader(val_data, batch_size=32)

# =========================
# MODEL
# =========================
model = models.resnet18(weights=models.ResNet18_Weights.DEFAULT)

# partial freezing
for name, param in model.named_parameters():
    if "layer4" in name or "fc" in name:
        param.requires_grad = True
    else:
        param.requires_grad = False

model.fc = nn.Linear(model.fc.in_features, 5)
model = model.to(DEVICE)

criterion = nn.CrossEntropyLoss()
optimizer = torch.optim.Adam(
    filter(lambda p: p.requires_grad, model.parameters()),
    lr=0.0005
)

# =========================
# TRAINING
# =========================
best_acc = 0

print("🔥 Training Style Model...")

for epoch in range(22):

    model.train()

    for images, labels in train_loader:
        images, labels = images.to(DEVICE), labels.to(DEVICE)

        outputs = model(images)
        loss = criterion(outputs, labels)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    # =========================
    # VALIDATION
    # =========================
    model.eval()
    preds, labels_list = [], []

    with torch.no_grad():
        for images, labels in val_loader:
            images = images.to(DEVICE)

            outputs = model(images)
            pred = torch.argmax(outputs, 1).cpu().numpy()

            preds.extend(pred)
            labels_list.extend(labels.numpy())

    acc = accuracy_score(labels_list, preds)

    print(f"Epoch {epoch+1} Accuracy: {acc:.2f}")

    if acc > best_acc:
        best_acc = acc
        torch.save(model.state_dict(), "models/style_model.pth")

print("✅ Best Model Saved")

# =========================
# METRICS
# =========================
precision = precision_score(labels_list, preds, average='weighted', zero_division=0)
recall = recall_score(labels_list, preds, average='weighted', zero_division=0)
f1 = f1_score(labels_list, preds, average='weighted', zero_division=0)

os.makedirs("analytics", exist_ok=True)

with open("analytics/style_metrics.json", "w") as f:
    json.dump({
        "accuracy": float(best_acc),
        "precision": float(precision),
        "recall": float(recall),
        "f1_score": float(f1)
    }, f)

print("🎯 METRICS SAVED")
