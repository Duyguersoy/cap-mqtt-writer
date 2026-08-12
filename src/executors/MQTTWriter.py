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
    from components.MQTTWriter.src.models.PackageModel import (
        PackageModel,
    )
    from components.MQTTWriter.src.utils.response import (
        build_response,
    )


class MQTTWriter(Component):
    """
    NovaVision workflow mesajlarını
    MQTT broker'a publish eden component.
    """

    def __init__(self, request, bootstrap):
        super().__init__(request, bootstrap)

        # ----------------------------------------------------------
        # REQUEST VALIDATION
        # ----------------------------------------------------------

        self.request.model = PackageModel(
            **self.request.data
        )

        # ----------------------------------------------------------
        # INPUT
        # ----------------------------------------------------------

        self.message = self.request.get_param(
            "message"
        )

        # ----------------------------------------------------------
        # REQUIRED CONFIGS
        # ----------------------------------------------------------

        self.host = self.request.get_param(
            "host"
        )

        self.port = self.request.get_param(
            "port"
        )

        self.topic = self.request.get_param(
            "topic"
        )

        self.qos = self.request.get_param(
            "qos"
        )

        self.retain = self.request.get_param(
            "retain"
        )

        self.timeout = self.request.get_param(
            "timeout"
        )

        # ----------------------------------------------------------
        # OPTIONAL CONFIGS
        # ----------------------------------------------------------

        self.username = self.get_optional_param(
            "username",
            default="",
        )

        self.password = self.get_optional_param(
            "password",
            default="",
        )

        # ----------------------------------------------------------
        # RESPONSE STATE
        # ----------------------------------------------------------

        self.error_status = False
        self.response_message = ""

    def get_optional_param(
        self,
        name,
        default="",
    ):
        """
        NovaVision boş textInput alanlarında bazen
        'value' key'ini request JSON'una eklemiyor.

        request.get_param() bu durumda KeyError/None
        üretebildiği için optional parametreler güvenli
        biçimde okunur.
        """

        try:
            value = self.request.get_param(
                name
            )

        except (KeyError, TypeError):
            return default

        if value is None:
            return default

        return value

    @staticmethod
    def bootstrap(
        config: dict = None,
    ) -> dict:
        """
        MQTT Writer başlangıçta model,
        weight veya başka kaynak yüklemez.
        """

        return {}

    def create_client(self):
        """
        Paho MQTT client oluşturur.
        """

        client = mqtt.Client(
            mqtt.CallbackAPIVersion.VERSION2
        )

        client.connect_timeout = float(
            self.timeout
        )

        if self.username:
            client.username_pw_set(
                username=self.username,
                password=self.password,
            )

        return client

    def publish_message(self):
        """
        Workflow mesajını MQTT broker'a publish eder.
        """

        client = None

        try:
            client = self.create_client()

            # ------------------------------------------------------
            # CONNECT
            # ------------------------------------------------------

            client.connect(
                host=self.host,
                port=int(self.port),
                keepalive=60,
            )

            client.loop_start()

            connection_deadline = (
                time.monotonic()
                + float(self.timeout)
            )

            while not client.is_connected():

                if (
                    time.monotonic()
                    >= connection_deadline
                ):
                    raise TimeoutError(
                        "MQTT broker connection timed out."
                    )

                time.sleep(0.01)

            # ------------------------------------------------------
            # PUBLISH
            # ------------------------------------------------------

            publish_info = client.publish(
                topic=self.topic,
                payload=self.message,
                qos=int(self.qos),
                retain=bool(self.retain),
            )

            if (
                publish_info.rc
                != mqtt.MQTT_ERR_SUCCESS
            ):
                raise RuntimeError(
                    "MQTT publish request failed "
                    f"with code {publish_info.rc}."
                )

            publish_info.wait_for_publish(
                timeout=float(self.timeout)
            )

            if not publish_info.is_published():
                raise TimeoutError(
                    "MQTT publish operation timed out."
                )

            # ------------------------------------------------------
            # SUCCESS
            # ------------------------------------------------------

            self.error_status = False

            self.response_message = (
                "Message published successfully."
            )

        except Exception as exc:
            self.error_status = True
            self.response_message = str(exc)

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
        """
        MQTT publish işlemini çalıştırır ve
        NovaVision response modelini döndürür.
        """

        self.publish_message()

        return build_response(
            context=self
        )


if __name__ == "__main__":
    from sdks.novavision.src.helper.executor import Executor

    Executor(
        sys.argv[1]
    ).run()