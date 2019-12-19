from PIL import Image
import pytesseract
import difflib


class ImageWord:

    def __init__(self):
        self.words = ""
        self.top_left_position = None
        self.height = None
        self.width = None

    def match(self, input_string):
        rate = difflib.SequenceMatcher(None, self.words, input_string).quick_ratio()
        return rate

    def get_center_position(self):
        return self.top_left_position[0] + int(self.width / 2), self.top_left_position[1] + int(self.height / 2)


class RawImageProcessor:

    @staticmethod
    def load_image(image_path):
        # imageObject = Image.open("./ForOCRTest.png")
        image_object = Image.open(image_path)
        box = pytesseract.image_to_data(image_object, lang='chi_sim', output_type=pytesseract.Output.DICT)
        return box

    @staticmethod
    def drill_down(raw_data):
        image_object_list = []
        index = 0
        sentence = ""
        for idx, block_idx in enumerate(raw_data["block_num"]):
            if block_idx == index:
                sentence = sentence + raw_data["text"][idx]
            if idx + 1 == raw_data["block_num"].__len__() or raw_data["block_num"][idx + 1] != block_idx:
                try:
                    index = raw_data["block_num"][idx + 1]
                except Exception as e:
                    print(str(e))
                image_word = ImageWord()
                image_word.words = sentence
                image_word.top_left_position = (raw_data["left"][idx], raw_data["top"][idx])
                image_word.height = raw_data["height"][idx]
                image_word.width = raw_data["width"][idx]
                image_object_list.append(image_word)
                sentence = ""
        return image_object_list

    @staticmethod
    def get_highest_word_position(image_list, input_string):
        highest_rate_word = (0, "")
        for word in image_list:
            word_rate = word.match(input_string)
            if word_rate > highest_rate_word[0]:
                highest_rate_word = (word_rate, word)
        return highest_rate_word[1].get_center_position()



