"""NovaVision executor for Detection To JSON."""

import json
import os
import sys


sys.path.append(
    os.path.join(
        os.path.dirname(__file__),
        "../../../../",
    )
)


from sdks.novavision.src.base.component import Component


if __package__:
    from ..models.PackageModel import PackageModel
    from ..utils.response import build_response
else:
    from components.DetectionToJSON.src.models.PackageModel import PackageModel
    from components.DetectionToJSON.src.utils.response import build_response


class DetectionToJSON(Component):
    """
    NovaVision Detection veya List[Detection]
    verisini MQTT Writer tarafından kullanılabilecek
    JSON string formatına dönüştürür.
    """

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)

        self.request.model = PackageModel(**self.request.data)

        self.input_detections = self.request.get_param(
            "inputDetections"
        )

        self.output_message = ""

    @staticmethod
    def bootstrap(config: dict = None) -> dict:
        """
        Model veya harici kaynak yüklenmediği için
        boş bootstrap context döndürülür.
        """

        return {}

    @staticmethod
    def normalize_detections(detections):
        """
        Tek Detection girdisini liste haline getirir.
        Liste zaten geldiyse değiştirmeden döndürür.
        """

        if detections is None:
            return []

        if isinstance(detections, list):
            return detections

        return [detections]

    @staticmethod
    def bounding_box_to_dict(bounding_box):
        """
        NovaVision BoundingBox modelini
        JSON serializable dictionary yapısına dönüştürür.
        """

        if bounding_box is None:
            return None

        return {
            "left": float(bounding_box.left),
            "top": float(bounding_box.top),
            "width": float(bounding_box.width),
            "height": float(bounding_box.height),
        }

    @classmethod
    def detection_to_dict(cls, detection):
        """
        NovaVision Detection modelinden yalnızca
        dış sisteme gönderilmesi gereken alanları çıkarır.
        """

        return {
            "classLabel": detection.classLabel,
            "classId": int(detection.classId),
            "confidence": float(detection.confidence),
            "boundingBox": cls.bounding_box_to_dict(
                detection.boundingBox
            ),
        }

    def serialize_detections(self):
        """
        Detection listesini JSON string'e dönüştürür.
        """

        detections = self.normalize_detections(
            self.input_detections
        )

        payload = {
            "detections": [
                self.detection_to_dict(detection)
                for detection in detections
            ]
        }

        self.output_message = json.dumps(
            payload,
            ensure_ascii=False,
            separators=(",", ":"),
        )

    def run(self):
        """
        Detection verisini serialize eder ve
        NovaVision string output üretir.
        """

        self.serialize_detections()

        return build_response(context=self)


if __name__ == "__main__":
    from sdks.novavision.src.helper.executor import Executor

    Executor(sys.argv[1]).run()