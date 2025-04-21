from setuptools import setup, find_packages

setup(
    name="flowpower",
    version="0.1.0",
    description="Lean runner + tracer for PromptFlow",
    author="Matías",
    license="Business Source License 1.1",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "promptflow",
        "typer",
        "rich",
        "pyyaml"
    ],
    entry_points={
        "console_scripts": [
            "fp = flowpower.main:main"
        ]
    },
    python_requires=">=3.9,<4.0",
)
