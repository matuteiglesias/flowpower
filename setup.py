from setuptools import setup, find_packages

setup(
    name="flowpower",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    entry_points={
        "console_scripts": [
            "fp = flowpower.cli:cli"
        ]
    },
    install_requires=["promptflow", "typer", "rich", "pyyaml"],
)
