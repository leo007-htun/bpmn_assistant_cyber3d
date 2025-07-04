import xml.etree.ElementTree as ET

def set_all_false_to_true(xml_path, output_path):
    tree = ET.parse(xml_path)
    root = tree.getroot()

    def recursive_update(element):
        for attr in element.attrib:
            if element.attrib[attr].lower() == "false":
                element.attrib[attr] = "true"
        for child in element:
            recursive_update(child)

    recursive_update(root)
    tree.write(output_path, encoding="utf-8", xml_declaration=True)
    print(f"Updated XML saved to {output_path}")

# Example usage:
set_all_false_to_true("ontology_template.xml", "ontology_template_updated.xml")
