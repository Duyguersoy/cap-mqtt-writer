"""Response builder for Detection To JSON."""

from sdks.novavision.src.helper.package import PackageHelper

from components.DetectionToJSON.src.models.PackageModel import (
    ConfigExecutor,
    DetectionToJSONExecutor,
    OutputMessage,
    PackageConfigs,
    PackageModel,
    PackageOutputs,
    PackageResponse,
)


def build_response(context):
    output_message = OutputMessage(
        value=context.output_message
    )

    outputs = PackageOutputs(
        outputMessage=output_message
    )

    package_response = PackageResponse(
        outputs=outputs
    )

    component_executor = DetectionToJSONExecutor(
        value=package_response
    )

    executor = ConfigExecutor(
        value=component_executor
    )

    package_configs = PackageConfigs(
        executor=executor
    )

    package_helper = PackageHelper(
        packageModel=PackageModel,
        packageConfigs=package_configs,
    )

    return package_helper.build_model(context)