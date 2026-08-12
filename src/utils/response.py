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

    error_status = ErrorStatusOutput(
        value=context.error_status
    )

    message = MessageOutput(
        value=context.response_message
    )

    outputs = PackageOutputs(
        errorStatus=error_status,
        message=message,
    )

    package_response = PackageResponse(
        outputs=outputs
    )

    mqtt_writer_executor = MQTTWriterExecutor(
        value=package_response
    )

    executor = ConfigExecutor(
        value=mqtt_writer_executor
    )

    package_configs = PackageConfigs(
        executor=executor
    )

    package = PackageHelper(
        packageModel=PackageModel,
        packageConfigs=package_configs,
    )

    return package.build_model(context)