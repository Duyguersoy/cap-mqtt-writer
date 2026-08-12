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
    MQTT broker'a publish edilecek mesaj.
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
    MQTT broker host adresi.
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


class Port(Config):
    """
    MQTT broker portu.
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


class Topic(Config):
    """
    Mesajın yayınlanacağı MQTT topic.
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


class QoS(Config):
    """
    MQTT Quality of Service seviyesi.

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


# ================================================================
# RETAIN DROPDOWN OPTIONS
# ================================================================


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
    Broker'ın mesajı retain edip etmeyeceğini belirler.
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


class Timeout(Config):
    """
    MQTT bağlantı ve publish timeout süresi.
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


class Username(Config):
    """
    Opsiyonel MQTT kullanıcı adı.

    Boş bırakılabilir.
    """

    name: Literal["username"] = "username"

    # Optional[str] = None yerine boş string default kullanıyoruz.
    # Böylece model tarafında value alanı her zaman tanımlıdır.
    value: str = ""

    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Username"


class Password(Config):
    """
    Opsiyonel MQTT şifresi.

    Boş bırakılabilir.
    """

    name: Literal["password"] = "password"

    value: str = ""

    type: Literal["string"] = "string"
    field: Literal["textInput"] = "textInput"

    class Config:
        title = "Password"


# ================================================================
# EXECUTOR CONFIGS
# ================================================================


class MQTTWriterConfigs(Configs):
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
    Publish işlemi başarısızsa True,
    başarılıysa False.
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
    MQTT Writer durum mesajı.
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
    errorStatus: ErrorStatusOutput
    message: MessageOutput


# ================================================================
# REQUEST
# ================================================================


class PackageRequest(Request):
    """
    MQTTWriter executor request modeli.
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
    outputs: PackageOutputs


# ================================================================
# EXECUTOR
# ================================================================


class MQTTWriterExecutor(Config):
    """
    MQTTWriter Request ve Response modellerini
    tek executor altında toplar.
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
    Package'ın executor seçimini tanımlar.

    Package tek executor içerdiği için
    target değeri "value" olmalıdır.
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
    executor: ConfigExecutor


# ================================================================
# PACKAGE MODEL
# ================================================================


class PackageModel(Package):
    """
    NovaVision MQTT Writer component modeli.
    """

    configs: PackageConfigs

    type: Literal[
        "component"
    ] = "component"

    name: Literal[
        "MQTTWriter"
    ] = "MQTTWriter"