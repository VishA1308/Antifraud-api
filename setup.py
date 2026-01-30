from setuptools import setup, find_packages

setup(
    name="antifraud-service",
    version="0.1.0",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    install_requires=[
        "fastapi==0.109.2",
        "pydantic==2.6.0",
        "python-dateutil==2.8.2",
        "uvicorn==0.27.0",
        "redis==5.0.1"
    ],
    extras_require={
        "dev": [
            "pytest==8.0.1",
            "httpx==0.27.0"
        ]
    }
)