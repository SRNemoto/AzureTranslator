import requests
# If you are using a Jupyter notebook, uncomment the following line.
# %matplotlib inline
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
from io import BytesIO
import numpy as np

# Add your Computer Vision subscription key and endpoint to your environment variables.
# if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
#     subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
# else:
#     print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable.\n**Restart your shell or IDE for changes to take effect.**")
#     sys.exit()

# if 'COMPUTER_VISION_ENDPOINT' in os.environ:
#     endpoint = os.environ['COMPUTER_VISION_ENDPOINT']

filename = "api_key.txt"
api_file = open(filename, "r")
api_lines = api_file.readlines()
api_key = [line for line in map((lambda line: line.rstrip()), api_lines)]

subscription_key = api_key[0]
endpoint = api_key[2]

# Set image_url to the URL of an image that you want to analyze.
image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/a/af/" + \
    "Atomist_quote_from_Democritus.png/338px-Atomist_quote_from_Democritus.png"

""" for images from local storage"""
# image_path = "<path-to-local-image-file>"
# # Read the image into a byte array
# image_data = open(image_path, "rb").read()
# # Set Content-Type to octet-stream
# headers = {'Ocp-Apim-Subscription-Key': subscription_key, 'Content-Type': 'application/octet-stream'}
# # put the byte array into your post request
# response = requests.post(ocr_url, headers=headers, params=params, data = image_data)

class OCRTranslate:
    def __init__(self, api_key, endpoint):
        self.key = api_key
        self.endpoint = endpoint
    
    def TransImg(self, language='unk', image_url=None, image_path=None):
        ocr_url = self.endpoint + "vision/v2.1/ocr"
        headers = {'Ocp-Apim-Subscription-Key': self.key}
        params = {'language': language, 'detectOrientation': 'true'}
        data = {'url': image_url}
        response = requests.post(ocr_url, headers=headers, params=params, json=data)
        response.raise_for_status()

        analysis = response.json()

        # Extract the word bounding boxes and text.
        line_infos = [region["lines"] for region in analysis["regions"]]
        word_infos = []
        for line in line_infos:
            for word_metadata in line:
                for word_info in word_metadata["words"]:
                    word_infos.append(word_info)
                    print(word_info)

        # Display the image and overlay it with the extracted text.
        plt.figure(figsize=(5, 5))
        image = Image.open(BytesIO(requests.get(image_url).content))
        np_image = np.array(image)
        print("image length: {}".format(np_image.shape))
        print("image[0] length: {}".format(len(np_image[0])))
        print("image type: {}".format(type(np_image)))
        ax = plt.imshow(image)
        for word in word_infos:
            bbox = [int(num) for num in word["boundingBox"].split(",")]
            avg_color = self.getAvgColor(np_image, bbox)
            print("bbox: {}".format(avg_color))
            text = word["text"]
            origin = (bbox[0], bbox[1])
            patch = Rectangle(origin, bbox[2], bbox[3],
                            fill=False, linewidth=2, color=avg_color[0:3])
            ax.axes.add_patch(patch)
            plt.text(origin[0], origin[1], text, fontsize=20, weight="bold", va="top", color='w')
        plt.axis("off")
        plt.show()

    def getAvgColor(self, np_image, bbox):
        # top_left_x = bbox[0]
        # top_left_y = bbox[1]
        # bot_right_x = bbox[2]
        # bot_right_y = bbox[3]

        avg_list = []

        for index in range(0, np_image.shape[2]):
            print("top_left[{}]: {}".format(index, np_image[bbox[1], bbox[0], index]))
            avg = \
                np_image[bbox[1], bbox[0], index] + \
                np_image[bbox[3], bbox[0], index] + \
                np_image[bbox[1], bbox[2], index] + \
                np_image[bbox[3], bbox[2], index]
            avg /= 4 * 255
            avg_list.append(avg)

        return avg_list
            

if __name__ == "__main__":
    module = OCRTranslate(subscription_key, endpoint)
    module.TransImg('unk', image_url)