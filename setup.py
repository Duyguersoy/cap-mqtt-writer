import setuptools


setuptools.setup(
    name="mqtt-writer",
    version="0.0.1",
    author="NovaVision AI",
    author_email="info@novavision.ai",
    description="MQTT Writer component for NovaVision",
    url="https://github.com/Duyguersoy/cap-mqtt-writer",
    license="MIT",

    install_requires=[
        "paho-mqtt>=2.1.0,<3.0",
    ],

    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],

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