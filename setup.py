import setuptools


setuptools.setup(
    name="detection-to-json",
    version="0.0.1",
    author="NovaVision AI",
    author_email="info@novavision.ai",
    description="Convert NovaVision detections to JSON string",
    license="MIT",

    packages=[
        "novavision.package",
        "novavision.package.executors",
        "novavision.package.models",
        "novavision.package.utils",
    ],

    package_dir={
        "novavision.package": "src",
    },

    python_requires=">=3.7",
)