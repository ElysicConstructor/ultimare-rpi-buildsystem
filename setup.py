# setup.py
from setuptools import setup, find_packages
from pathlib import Path

# Long description aus README.md
here = Path(__file__).parent
long_description = (here / "README.md").read_text(encoding="utf-8")

# Requirements einlesen
requirements_file = here / "requirements.txt"
if requirements_file.exists():
    with requirements_file.open(encoding="utf-8") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]
else:
    requirements = []

setup(
    name="ultimate-firmware-builder",
    version="0.1.0",
    author="Calvin Ronksley",
    author_email="hexzhen3x7@gmail.com",
    description="Ein modularer ARM64 Firmware-Builder für Raspberry Pi 4B/5",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ElysicConstructor/ultimare-rpi-buildsystem",
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    python_requires=">=3.10",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "ufb=main:main",  # ruft main.py main() auf
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: POSIX :: Linux",
        "Intended Audience :: Developers",
        "Topic :: System :: Installation/Setup",
    ],
    include_package_data=True,
    zip_safe=False,
)
