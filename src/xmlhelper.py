import os
from xml.dom import minidom
from xml.etree.ElementTree import (Element, tostring)


def write(filepath: str, string: str):
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'w') as file:
        file.write(string)


def prettify(elem: Element) -> str:
    "Return a pretty-printed XML string for the Element."
    rough_string = tostring(elem, encoding='unicode')
    reparsed = minidom.parseString(rough_string)
    encoded = reparsed.toprettyxml(indent=' '*2, encoding='utf-8')
    return encoded.decode('utf-8')