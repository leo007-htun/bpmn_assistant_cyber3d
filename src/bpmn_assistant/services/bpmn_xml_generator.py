import json
import xml.etree.ElementTree as ET

from bpmn_assistant.config import logger
from bpmn_assistant.services import BpmnProcessTransformer


class BpmnXmlGenerator:
    """
    Generates custom BPMN layout XML in <root> format for Unity or frontend diagram rendering.
    """

    def __init__(self):
        self.transformer = BpmnProcessTransformer()

    def create_bpmn_xml(self, process: list[dict]) -> str:
        """
        Create BPMN layout XML in <root> format with <BPMNShape> and <BPMNEdge>.

        Args:
            process: List of BPMN elements from LLM.

        Returns:
            str: XML string for Unity or frontend rendering.
        """
        transformed_process = self.transformer.transform(process)
        logger.debug(f"Transformed process:\n{json.dumps(transformed_process, indent=2)}")

        layout_root = ET.Element("root")

        # Layout configuration
        x_start = 100
        y = -100
        spacing = 200
        width = 966.2021
        height = 506.1058

        id_pos = {}

        # Create BPMNShape elements
        for i, element in enumerate(transformed_process["elements"]):
            elem_id = element.get("id")
            label = element.get("label") or ""
            elem_type = element.get("type") or "task"

            shape = ET.SubElement(layout_root, "BPMNShape")
            shape.set("bpmnElement", str(elem_id))
            shape.set("id", str(elem_id))
            shape.set("text", str(label))
            shape.set("type", str(elem_type))  # Added for prefab matching

            x = x_start + i * spacing
            bounds = ET.SubElement(shape, "Bounds")
            bounds.set("x", str(x))
            bounds.set("y", str(y))
            bounds.set("width", str(width))
            bounds.set("height", str(height))

            id_pos[elem_id] = (x + width / 2, y + height / 2)

        # Create BPMNEdge elements
        for i, flow in enumerate(transformed_process["flows"]):
            source = flow.get("sourceRef")
            target = flow.get("targetRef")
            edge_id = f"{source}-{target}_connector{i}"

            edge = ET.SubElement(layout_root, "BPMNEdge")
            edge.set("id", edge_id)
            edge.set("startElement", str(source))
            edge.set("startPosition", "locationRight")
            edge.set("targetElement", str(target))
            edge.set("targetPosition", "locationLeft")

            if source in id_pos and target in id_pos:
                sx, sy = id_pos[source]
                tx, ty = id_pos[target]
                ET.SubElement(edge, "waypoint", x=str(sx), y=str(sy))
                ET.SubElement(edge, "waypoint", x=str(tx), y=str(ty))

        # Convert XML tree to string
        layout_xml_string = ET.tostring(layout_root, encoding="unicode")
        return layout_xml_string
