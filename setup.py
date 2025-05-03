from setuptools import setup, find_packages

setup(
    name="water-reminder",
    version="0.1.0",
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        "click>=8.1.7",
        "pystray>=0.19.5",
        "Pillow>=10.2.0",
        "python-dotenv>=1.0.1",
        "schedule>=1.2.1",
    ],
    entry_points={
        "console_scripts": [
            "water-reminder=water_reminder.cli:cli",
        ],
    },
    author="Your Name",
    author_email="your.email@example.com",
    description="A CLI tool to remind you to drink water",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/water-reminder-cli",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
) 