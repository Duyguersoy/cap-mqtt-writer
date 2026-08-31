"""NovaVision executor for MQTT Writer."""

import math
import os
import sys
import time

import paho.mqtt.client as mqtt


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
    from components.MQTTWriter.src.models.PackageModel import PackageModel
    from components.MQTTWriter.src.utils.response import build_response


class MQTTWriter(Component):
    """
    NovaVision workflow üzerinden gelen string mesajı
    MQTT broker'a publish eder.
    """

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)

        self.request.model = PackageModel(**self.request.data)

        self.message = self.request.get_param("message")

        self.host = self.request.get_param("host")
        self.port = self.request.get_param("port")
        self.topic = self.request.get_param("topic")
        self.qos = self.request.get_param("qos")
        self.retain = self.request.get_param("retain")
        self.timeout = self.request.get_param("timeout")

        self.username = self.get_optional_param(
            "username",
            default="",
        )

        self.password = self.get_optional_param(
            "password",
            default="",
        )

        self.error_status = False
        self.response_message = ""

    @staticmethod
    def bootstrap(config: dict = None) -> dict:
        return {}

    def get_optional_param(self, name, default=""):
        """
        Opsiyonel config alanlarını güvenli biçimde okur.
        """

        try:
            value = self.request.get_param(name)
        except (KeyError, TypeError):
            return default

        if value is None:
            return default

        return value

    @staticmethod
    def unwrap_value(value):
        """
        NovaVision dropdown/config wrapper nesnelerinin
        içindeki gerçek value değerini çözer.
        """

        visited = set()

        while hasattr(value, "value"):
            object_id = id(value)

            if object_id in visited:
                break

            visited.add(object_id)
            value = value.value

        return value

    def normalize_retain(self):
        """
        Retain config değerini güvenli boolean
        değerine dönüştürür.
        """

        value = self.unwrap_value(self.retain)

        if isinstance(value, bool):
            return value

        if isinstance(value, str):
            normalized = value.strip().lower()

            if normalized in (
                "true",
                "1",
                "yes",
                "enable",
                "enabled",
            ):
                return True

            if normalized in (
                "false",
                "0",
                "no",
                "disable",
                "disabled",
                "",
            ):
                return False

        if isinstance(value, (int, float)):
            return bool(value)

        raise ValueError(
            "Retain must be a boolean value."
        )

    def validate_configs(self):
        """
        MQTT connection ve publish ayarlarını
        runtime'da doğrular.
        """

        host = str(self.host).strip()
        topic = str(self.topic).strip()

        port = int(
            self.unwrap_value(self.port)
        )

        qos = int(
            self.unwrap_value(self.qos)
        )

        timeout = float(
            self.unwrap_value(self.timeout)
        )

        if not host:
            raise ValueError(
                "Host cannot be empty."
            )

        if not 1 <= port <= 65535:
            raise ValueError(
                "Port must be between 1 and 65535."
            )

        if not topic:
            raise ValueError(
                "Topic cannot be empty."
            )

        if qos not in (0, 1, 2):
            raise ValueError(
                "QoS must be 0, 1, or 2."
            )

        if not math.isfinite(timeout) or timeout <= 0:
            raise ValueError(
                "Timeout must be a finite number greater than 0."
            )

        username = str(self.username).strip()
        password = str(self.password)

        if password and not username:
            raise ValueError(
                "Password cannot be used without username."
            )

        self.host = host
        self.topic = topic
        self.port = port
        self.qos = qos
        self.timeout = timeout
        self.username = username
        self.password = password

    def create_client(self):
        """
        Paho MQTT client oluşturur.
        """

        client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2
        )

        if self.username:
            client.username_pw_set(
                username=self.username,
                password=self.password,
            )

        return client

    def wait_for_connection(self, client):
        """
        Broker bağlantısının belirtilen timeout
        süresi içinde kurulmasını bekler.
        """

        deadline = (
            time.monotonic()
            + self.timeout
        )

        while not client.is_connected():
            if time.monotonic() >= deadline:
                raise TimeoutError(
                    "MQTT broker connection timed out."
                )

            time.sleep(0.01)

    def publish_message(self):
        """
        Gelen string mesajı MQTT broker'a publish eder.
        """

        client = None

        try:
            self.validate_configs()

            client = self.create_client()

            client.connect(
                host=self.host,
                port=self.port,
                keepalive=60,
            )

            client.loop_start()

            self.wait_for_connection(
                client
            )

            publish_info = client.publish(
                topic=self.topic,
                payload=self.message,
                qos=self.qos,
                retain=self.normalize_retain(),
            )

            if publish_info.rc != mqtt.MQTT_ERR_SUCCESS:
                raise RuntimeError(
                    "MQTT publish request failed "
                    f"with code {publish_info.rc}."
                )

            publish_info.wait_for_publish(
                timeout=self.timeout
            )

            if not publish_info.is_published():
                raise TimeoutError(
                    "MQTT publish operation timed out."
                )

            self.error_status = False
            self.response_message = (
                "Message published successfully."
            )

        except Exception as error:
            self.error_status = True
            self.response_message = str(error)

        finally:
            if client is not None:
                try:
                    client.disconnect()
                except Exception:
                    pass

                try:
                    client.loop_stop()
                except Exception:
                    pass

    def run(self):
        self.publish_message()

        return build_response(
            context=self
        )


if __name__ == "__main__":
    from sdks.novavision.src.helper.executor import Executor

    Executor(sys.argv[1]).run()