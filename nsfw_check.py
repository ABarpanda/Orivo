from PIL import Image
from transformers import pipeline

def is_nsfw(img_path:str)->bool:
    img = Image.open(img_path)
    classifier = pipeline("image-classification", model="Falconsai/nsfw_image_detection")
    classification = list(classifier(img))
    if classification[0]["score"]>classification[1]["score"]:
        return False
    return True

if __name__=="__main__":
    print(is_nsfw("imagesFromUsers/HN_Logo.png"))