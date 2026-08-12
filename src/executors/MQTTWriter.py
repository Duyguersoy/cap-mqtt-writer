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

from components.MQTTWriter.src.utils.response import build_response
from components.MQTTWriter.src.models.PackageModel import PackageModel


class MQTTWriter(Component):

    def __init__(self, request, bootstrap):

        super().__init__(request, bootstrap)

        self.request.model = PackageModel(
            **self.request.data
        )

        # ==========================================================
        # INPUT
        # ==========================================================

        self.message = self.request.get_param(
            "message"
        )

        # ==========================================================
        # CONFIGS
        # ==========================================================

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

        self.username = self.request.get_param(
            "username"
        )

        self.password = self.request.get_param(
            "password"
        )

        # ==========================================================
        # OUTPUT STATE
        # ==========================================================

        self.error_status = False
        self.response_message = ""


    @staticmethod
    def bootstrap(config: dict) -> dict:
        """
        MQTT Writer does not require model weights
        or startup resources.
        """

        return {}


    def create_client(self):

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

        client = None

        try:

            client = self.create_client()

            # ======================================================
            # CONNECT
            # ======================================================

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

                if time.monotonic() >= connection_deadline:

                    raise TimeoutError(
                        "MQTT broker connection timed out."
                    )

                time.sleep(0.01)

            # ======================================================
            # PUBLISH
            # ======================================================

            publish_info = client.publish(
                topic=self.topic,
                payload=self.message,
                qos=int(self.qos),
                retain=bool(self.retain),
            )

            if publish_info.rc != mqtt.MQTT_ERR_SUCCESS:

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

            # ======================================================
            # SUCCESS
            # ======================================================

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

        self.publish_message()

        return build_response(
            context=self
        )


if __name__ == "__main__":

    from sdks.novavision.src.helper.executor import Executor

    Executor(
        sys.argv[1]
    ).run()