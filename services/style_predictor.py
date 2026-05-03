import torch
from torchvision import models, transforms
from PIL import Image

class StyleModel:

    def __init__(self):
        self.model = models.resnet18(pretrained=False)
        self.model.fc = torch.nn.Linear(self.model.fc.in_features, 5)

        self.model.load_state_dict(
            torch.load("models/style_model.pth", map_location="cpu")
        )

        self.model.eval()

        # 🔥 ORIGINAL MODEL CLASSES (DO NOT CHANGE ORDER)
        self.classes = ["boho", "industrial", "minimalist", "modern", "scandinavian"]

        # 🔥 NEW: MAPPING TO DB VALUES
        self.style_map = {
            "boho": "rustic",
            "industrial": "modern",
            "minimalist": "minimal",
            "modern": "modern",
            "scandinavian": "minimal"
        }

        self.transform = transforms.Compose([
            transforms.Resize((224,224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def predict(self, img):
        img = Image.fromarray(img)
        img = self.transform(img).unsqueeze(0)

        with torch.no_grad():
            output = self.model(img)

        # 🔥 STEP 1: GET MODEL PREDICTION
        pred_class = self.classes[output.argmax().item()]

        # 🔥 STEP 2: MAP TO DATABASE STYLE
        return self.style_map.get(pred_class, "modern")  # fallback safe


# 🔥 GLOBAL INSTANCE
style_model = StyleModel()

def detect_style(img):
    return style_model.predict(img)
