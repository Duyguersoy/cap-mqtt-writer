from typing import Literal, Optional, Union

from pydantic import Field

from sdks.novavision.src.base.model import (
    Package,
    Input,
    Inputs,
    Config,
    Configs,
    Output,
    Outputs,
    Request,
    Response,
)


# ================================================================
# INPUT
# ================================================================


class MessageInput(Input):
    """
    Message content to be published to the MQTT broker.
    """

    name: Literal["message"] = "message"
    value: str
    type: Literal["string"] = "string"

    class Config:
        title = "Message"


class PackageInputs(Inputs):
    message: MessageInput


# ================================================================
# CONFIG PARAMETERS
# ================================================================


class Host(Config):
    """
    Specifies the hostname or IP address of the MQTT broker
    that the client connects to for publishing messages.
    """

    name: Literal["host"] = "host"
    value: str
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    placeHolder: Literal[
        "localhost"
    ] = "localhost"

    class Config:
        title = "Host"

        json_schema_extra = {
            "shortDescription": "MQTT Broker Host"
        }


class Port(Config):
    """
    Specifies the network port used to connect to the MQTT broker.
    """

    name: Literal["port"] = "port"

    value: int = Field(
        default=1883,
        ge=1,
        le=65535,
    )

    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    placeHolder: Literal[
        "1883"
    ] = "1883"

    class Config:
        title = "Port"

        json_schema_extra = {
            "shortDescription": "MQTT Broker Port"
        }


class Topic(Config):
    """
    Specifies the MQTT topic to which messages are published.
    """

    name: Literal["topic"] = "topic"
    value: str
    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    placeHolder: Literal[
        "novavision/test"
    ] = "novavision/test"

    class Config:
        title = "Topic"

        json_schema_extra = {
            "shortDescription": "Publish Topic"
        }


class QoS(Config):
    """
    Specifies the MQTT Quality of Service level used for message delivery.

    0 -> At most once
    1 -> At least once
    2 -> Exactly once
    """

    name: Literal["qos"] = "qos"

    value: int = Field(
        default=0,
        ge=0,
        le=2,
    )

    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    placeHolder: Literal[
        "0"
    ] = "0"

    class Config:
        title = "QoS"

        json_schema_extra = {
            "shortDescription": "Quality of Service Level"
        }


# ================================================================
# RETAIN DROPDOWN OPTIONS
# ================================================================


class RetainFalse(Config):
    """
    Represents the disabled retain option.
    """

    name: Literal["False"] = "False"
    value: Literal[False] = False
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Disable"


class RetainTrue(Config):
    """
    Represents the enabled retain option.
    """

    name: Literal["True"] = "True"
    value: Literal[True] = True
    type: Literal["bool"] = "bool"
    field: Literal["option"] = "option"

    class Config:
        title = "Enable"


class Retain(Config):
    """
    Determines whether the MQTT broker should retain
    the published message for future subscribers.
    """

    name: Literal["retain"] = "retain"

    value: Union[
        RetainFalse,
        RetainTrue,
    ]

    type: Literal["object"] = "object"
    field: Literal["dropdownlist"] = "dropdownlist"

    class Config:
        title = "Retain"

        json_schema_extra = {
            "shortDescription": "Retain Published Message"
        }


class Timeout(Config):
    """
    Specifies the timeout duration for MQTT connection
    and publish operations.
    """

    name: Literal["timeout"] = "timeout"

    value: float = Field(
        default=0.5,
        gt=0,
    )

    type: Literal["number"] = "number"
    field: Literal["textInput"] = "textInput"

    placeHolder: Literal[
        "0.5"
    ] = "0.5"

    class Config:
        title = "Timeout"

        json_schema_extra = {
            "shortDescription": "Connection Timeout"
        }


class Username(Config):
    """
    Optional username used to authenticate with the MQTT broker.

    This field may be left empty when authentication is not required.
    """

    name: Literal["username"] = "username"

    # An empty string is used instead of Optional[str] = None
    # so that the value field is always defined in the model.
    value: str = ""

    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Username"

        json_schema_extra = {
            "shortDescription": "Broker Username"
        }


class Password(Config):
    """
    Optional password used to authenticate with the MQTT broker.

    This field may be left empty when authentication is not required.
    """

    name: Literal["password"] = "password"

    value: str = ""

    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Password"

        json_schema_extra = {
            "shortDescription": "Broker Password"
        }


# ================================================================
# EXECUTOR CONFIGS
# ================================================================


class MQTTWriterConfigs(Configs):
    """
    Contains all MQTT connection and publishing configuration parameters.
    """

    host: Host
    port: Port
    topic: Topic
    qos: QoS
    retain: Retain
    timeout: Timeout
    username: Username
    password: Password


# ================================================================
# OUTPUTS
# ================================================================


class ErrorStatusOutput(Output):
    """
    Indicates whether the MQTT publish operation failed.

    Returns True when an error occurs and False when the message
    is published successfully.
    """

    name: Literal[
        "errorStatus"
    ] = "errorStatus"

    value: bool

    type: Literal[
        "bool"
    ] = "bool"

    class Config:
        title = "Error Status"


class MessageOutput(Output):
    """
    Provides the status message generated by the MQTT Writer operation.
    """

    name: Literal[
        "message"
    ] = "message"

    value: str

    type: Literal[
        "string"
    ] = "string"

    class Config:
        title = "Message"


class PackageOutputs(Outputs):
    """
    Contains the outputs returned by the MQTT Writer executor.
    """

    errorStatus: ErrorStatusOutput
    message: MessageOutput


# ================================================================
# REQUEST
# ================================================================


class PackageRequest(Request):
    """
    Defines the request model used by the MQTT Writer executor.
    """

    inputs: Optional[
        PackageInputs
    ] = None

    configs: MQTTWriterConfigs

    class Config:
        json_schema_extra = {
            "target": "configs",
        }


# ================================================================
# RESPONSE
# ================================================================


class PackageResponse(Response):
    """
    Defines the response model returned by the MQTT Writer executor.
    """

    outputs: PackageOutputs


# ================================================================
# EXECUTOR
# ================================================================


class MQTTWriterExecutor(Config):
    """
    Combines the MQTT Writer request and response models
    under a single executor definition.
    """

    name: Literal[
        "MQTTWriter"
    ] = "MQTTWriter"

    value: Union[
        PackageRequest,
        PackageResponse,
    ]

    type: Literal[
        "object"
    ] = "object"

    field: Literal[
        "option"
    ] = "option"

    class Config:
        title = "MQTT Writer"

        json_schema_extra = {
            "target": {
                "value": 0,
            }
        }


# ================================================================
# CONFIG EXECUTOR
# ================================================================


class ConfigExecutor(Config):
    """
    Defines the executor selection for the package.

    Since the package contains a single executor, the target
    is set to "value".
    """

    name: Literal[
        "ConfigExecutor"
    ] = "ConfigExecutor"

    value: Union[
        MQTTWriterExecutor
    ]

    type: Literal[
        "executor"
    ] = "executor"

    field: Literal[
        "dependentDropdownlist"
    ] = "dependentDropdownlist"

    class Config:
        title = "Task"

        json_schema_extra = {
            "target": "value",
        }


# ================================================================
# PACKAGE CONFIGS
# ================================================================


class PackageConfigs(Configs):
    """
    Contains the executor configuration for the package.
    """

    executor: ConfigExecutor


# ================================================================
# PACKAGE MODEL
# ================================================================


class PackageModel(Package):
    """
    Defines the NovaVision MQTT Writer component package model.

    The package publishes string messages to an MQTT broker using
    configurable connection, topic, QoS, retain, timeout, and
    authentication parameters.
    """

    configs: PackageConfigs

    type: Literal[
        "component"
    ] = "component"

    name: Literal[
        "MQTTWriter"
    ] = "MQTTWriter"