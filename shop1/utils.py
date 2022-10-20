import re


def cleaner(text):
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'https*\S+', '', text)
    text = re.sub(r'[^A-zА-я0-9., ]', '', text)
    return text