from typing import List

from collections.__init__ import namedtuple
from xml.etree.ElementTree import Element, SubElement

Tag = namedtuple('Tag', 'id name applicability')



def create_tag_xml(tags: List[Tag]) -> Element:
    root = Element('odoo')
    for tag in tags:
        record = SubElement(root, 'record', {'id': tag.id, 'model': 'account.account.tag'})
        SubElement(record, 'field', {'name': 'name'}).text = tag.name
        SubElement(record, 'field', {'name': 'applicability'}).text = tag.applicability
    return root