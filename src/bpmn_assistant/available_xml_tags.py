import xml.etree.ElementTree as ET

def print_tag_hierarchy(element, indent=0):
    print("  " * indent + f"- {element.tag}")
    for child in element:
        print_tag_hierarchy(child, indent + 1)

def list_tag_structure(xml_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()
    print("Tag Structure:\n")
    print_tag_hierarchy(root)

# Example usage
list_tag_structure("ontology_template.xml")
