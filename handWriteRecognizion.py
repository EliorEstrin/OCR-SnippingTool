import os, io
from google.cloud import vision



def get_text_from_image():
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = r'venv/ServiceAccountToken.json'
    client = vision.ImageAnnotatorClient()
    #change it to your directory when Trying
    FOLDER_PATH = r'C:\Users\elior\Desktop\Python\v3_snippingTool'
    IMAGE_FILE = 'some_image.jpeg'
    FILE_PATH = os.path.join(FOLDER_PATH, IMAGE_FILE)
    print('---------------')
    with io.open(FILE_PATH, 'rb') as image_file:
        content = image_file.read()

    image = vision.Image(content=content)
    response = client.document_text_detection(image=image)

    print(type(response))
    print(f"Respons is {response}")
    docText = response.full_text_annotation.text
    print(f"The Result is: {docText}")
    return docText

# get_text_from_image()