from PIL import Image
from transformers import pipeline

def is_nsfw(img_path:str)->bool:
    img = Image.open(img_path)
    classifier = pipeline("image-classification", model="Falconsai/nsfw_image_detection")
    classification = list(classifier(img))
    print(classification)
    for i in classification:
        if i['label']=="nsfw":
            nsfw_score = i['score']
    if nsfw_score>=0.5:
        return True
    return False

# file_bytes = await all_attachments[attachment_index].read()
# is_nsfw = await detector.classify(file_bytes)
# print(f"Checking the attachment {all_attachments[attachment_index]}")
# if is_nsfw==True:
#     print(f"{all_attachments[attachment_index]} is NSFW image")
# else:
#     print(f"{all_attachments[attachment_index]} is not NSFW")

if __name__=="__main__":
    print(is_nsfw("imagesFromUsers/nude-8255612_1280.jpg"))