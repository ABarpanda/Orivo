from PIL import Image
from transformers import pipeline
import io
import asyncio

class NSFWDetector:
    def __init__(self):
        print("🔍 Loading NSFW model...")
        self.classifier = pipeline("image-classification", model="Falconsai/nsfw_image_detection")
        print("✅ NSFW model loaded.")

    def classify_sync(self, img_bytes: bytes) -> bool:
        img = Image.open(io.BytesIO(img_bytes))
        result = list(self.classifier(img))
        for i in result:
            if i['label']=="nsfw":
                nsfw_score = i['score']
        if nsfw_score>=0.5:
            return True
        return False

    async def classify(self, img_bytes: bytes) -> bool:
        return await asyncio.to_thread(self.classify_sync, img_bytes)
