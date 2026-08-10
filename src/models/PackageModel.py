from pydantic import Field
from typing import Optional, Union, Literal

from sdks.novavision.src.base.model import (
    Package,
    Inputs,
    Configs,
    Outputs,
    Response,
    Request,
    Output,
    Input,
    Config,
)


# ------------------------------------------------------------------
# INPUTS
# ------------------------------------------------------------------

class MessageInput(Input):
    """
    Message that will be published to the MQTT broker.
    """

    name: Literal["message"] = "message"
    value: str
    type: Literal["string"] = "string"

    class Config:
        title = "Message"


class PackageInputs(Inputs):
    message: MessageInput


# ------------------------------------------------------------------
# CONFIGS
# ------------------------------------------------------------------

class Host(Config):
    """
    MQTT broker host address.
    """

    name: Literal["host"] = "host"
    value: str
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["localhost"] = "localhost"

    class Config:
        title = "Host"


class Port(Config):
    """
    MQTT broker port.
    """

    name: Literal["port"] = "port"
    value: int = Field(default=1883, ge=1, le=65535)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["1883"] = "1883"

    class Config:
        title = "Port"


class Topic(Config):
    """
    MQTT topic that the message will be published to.
    """

    name: Literal["topic"] = "topic"
    value: str
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["novavision/test"] = "novavision/test"

    class Config:
        title = "Topic"


class QoS(Config):
    """
    MQTT Quality of Service level.

    0: At most once
    1: At least once
    2: Exactly once
    """

    name: Literal["qos"] = "qos"
    value: int = Field(default=0, ge=0, le=2)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["0"] = "0"

    class Config:
        title = "QoS"


class RetainFalse(Config):
    name: Literal["False"] = "False"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Disable"


class RetainTrue(Config):
    name: Literal["True"] = "True"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable"


class Retain(Config):
    """
    Determines whether the broker should retain the published message.
    """

    name: Literal["retain"] = "retain"
    value: Union[RetainFalse, RetainTrue]
    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Retain"


class Timeout(Config):
    """
    Timeout for MQTT connect and publish operations.
    """

    name: Literal["timeout"] = "timeout"
    value: float = Field(default=0.5, gt=0)
    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"
    placeHolder: Literal["0.5"] = "0.5"

    class Config:
        title = "Timeout"


class Username(Config):
    """
    Optional MQTT broker username.
    """

    name: Literal["username"] = "username"
    value: Optional[str] = None
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Username"


class Password(Config):
    """
    Optional MQTT broker password.
    """

    name: Literal["password"] = "password"
    value: Optional[str] = None
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Password"


class MQTTWriterConfigs(Configs):
    host: Host
    port: Port
    topic: Topic
    qos: QoS
    retain: Retain
    timeout: Timeout
    username: Username
    password: Password


# ------------------------------------------------------------------
# OUTPUTS
# ------------------------------------------------------------------

class ErrorStatusOutput(Output):
    """
    True when the MQTT publish operation fails.
    False when the operation succeeds.
    """

    name: Literal["error_status"] = "error_status"
    value: bool
    type: Literal["bool"] = "bool"

    class Config:
        title = "Error Status"


class MessageOutput(Output):
    """
    Status message returned after the MQTT publish operation.
    """

    name: Literal["message"] = "message"
    value: str
    type: Literal["string"] = "string"

    class Config:
        title = "Message"


class PackageOutputs(Outputs):
    error_status: ErrorStatusOutput
    message: MessageOutput


# ------------------------------------------------------------------
# REQUEST / RESPONSE
# ------------------------------------------------------------------

class PackageRequest(Request):
    inputs: PackageInputs
    configs: MQTTWriterConfigs

    class Config:
        json_schema_extra = {
            "target": "configs"
        }


class PackageResponse(Response):
    outputs: PackageOutputs


# ------------------------------------------------------------------
# EXECUTOR
# ------------------------------------------------------------------

class MQTTWriterExecutor(Config):
    name: Literal["MQTTWriter"] = "MQTTWriter"
    value: Union[PackageRequest, PackageResponse]
    type: Literal["object"] = "object"
    field: Literal["option"] = "option"

    class Config:
        title = "MQTT Writer"
        json_schema_extra = {
            "target": {
                "value": 0
            }
        }


class ConfigExecutor(Config):
    name: Literal["ConfigExecutor"] = "ConfigExecutor"
    value: Union[MQTTWriterExecutor]
    type: Literal["executor"] = "executor"
    field: Literal["dependentDropdownlist"] = "dependentDropdownlist"

    class Config:
        title = "Task"
        json_schema_extra = {
            "target": "value"
        }


# ------------------------------------------------------------------
# PACKAGE MODEL
# ------------------------------------------------------------------

class PackageConfigs(Configs):
    executor: ConfigExecutor


class PackageModel(Package):
    configs: PackageConfigs
    type: Literal["component"] = "component"
    name: Literal["MQTTWriter"] = "MQTTWriter"
