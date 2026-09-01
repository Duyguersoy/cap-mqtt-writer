from sdks.novavision.src.helper.package import PackageHelper

from components.MQTTWriter.src.models.PackageModel import (
    PackageModel,
    PackageConfigs,
    ConfigExecutor,
    PackageOutputs,
    PackageResponse,
    MQTTWriterExecutor,
    ErrorStatusOutput,
    MessageOutput,
)


def build_response(context):
    """
    Converts the MQTT Writer execution result
    into the NovaVision PackageModel response structure.
    """

    error_status_output = ErrorStatusOutput(
        value=context.error_status
    )

    message_output = MessageOutput(
        value=context.response_message
    )

    package_outputs = PackageOutputs(
        errorStatus=error_status_output,
        message=message_output,
    )

    package_response = PackageResponse(
        outputs=package_outputs
    )

    mqtt_writer_executor = MQTTWriterExecutor(
        value=package_response
    )

    config_executor = ConfigExecutor(
        value=mqtt_writer_executor
    )

    package_configs = PackageConfigs(
        executor=config_executor
    )

    package_helper = PackageHelper(
        packageModel=PackageModel,
        packageConfigs=package_configs,
    )

    return package_helper.build_model(
        context
    )