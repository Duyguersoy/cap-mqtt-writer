from typing import List, Literal, Union

from pydantic import validator

from sdks.novavision.src.base.model import (
    Config,
    Configs,
    Detection,
    Input,
    Inputs,
    Output,
    Outputs,
    Package,
    Request,
    Response,
)


class InputDetections(Input):
    """
    DetectionToJSON tarafından JSON string'e
    dönüştürülecek detection verisi.
    """

    name: Literal["inputDetections"] = "inputDetections"
    value: Union[List[Detection], Detection]
    type: str = "object"

    @validator("type", pre=True, always=True)
    def set_type_based_on_value(cls, value, values):
        detection_value = values.get("value")

        if isinstance(detection_value, list):
            return "list"

        return "object"

    class Config:
        title = "Input Detections"


class OutputMessage(Output):
    """
    MQTT Writer'a gönderilecek JSON string çıktısı.
    """

    name: Literal["outputMessage"] = "outputMessage"
    value: str
    type: Literal["string"] = "string"

    class Config:
        title = "Output Message"


class PackageInputs(Inputs):
    inputDetections: InputDetections


class PackageOutputs(Outputs):
    outputMessage: OutputMessage


class PackageRequest(Request):
    inputs: PackageInputs

    class Config:
        json_schema_extra = {
            "target": "inputs",
        }


class PackageResponse(Response):
    outputs: PackageOutputs


class DetectionToJSONExecutor(Config):
    name: Literal["DetectionToJSON"] = "DetectionToJSON"

    value: Union[
        PackageRequest,
        PackageResponse,
    ]

    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "Detection To JSON"
        json_schema_extra = {
            "target": {
                "value": 0,
            }
        }


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"

    value: DetectionToJSONExecutor

    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"
        json_schema_extra = {
            "target": "value",
        }


class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs

    type: Literal["component"] = "component"
    name: Literal["DetectionToJSON"] = "DetectionToJSON"