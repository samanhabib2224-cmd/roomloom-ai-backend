import torch
from torchvision import models, transforms
from PIL import Image

MODEL_PATH = "models/resnet18_places365.pth.tar"
LABEL_PATH = "models/categories_places365.txt"

class SceneDetector:
    def __init__(self):
        self.model = models.resnet18(num_classes=365)

        checkpoint = torch.load(MODEL_PATH, map_location="cpu", weights_only=False)
        state_dict = {k.replace("module.", ""): v for k, v in checkpoint["state_dict"].items()}
        self.model.load_state_dict(state_dict)

        self.model.eval()

        with open(LABEL_PATH) as f:
            self.classes = [line.strip().split(' ')[0][3:] for line in f]

        self.transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(
                mean=[0.485, 0.456, 0.406],
                std=[0.229, 0.224, 0.225]
            )
        ])

    def detect_scene(self, img):
        img = Image.fromarray(img)
        input_img = self.transform(img).unsqueeze(0)

        with torch.no_grad():
            output = self.model(input_img)

        _, pred = torch.max(output, 1)
        scene = self.classes[pred.item()]

        # 🔥 SMART MAPPING
        if "bedroom" in scene:
            return "bedroom"
        elif "living" in scene:
            return "living_room"
        elif "office" in scene:
            return "office"
        elif "dining" in scene:
            return "guest_room"
        else:
            return "living_room"


detector = SceneDetector()

def detect_scene(img):
    return detector.detect_scene(img)