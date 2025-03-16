from setuptools import setup, find_packages

setup(
    name="moderation-ai-project",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "torch>=2.0.0",
        "torchvision>=0.15.0",
        "ultralytics>=8.0.0",
        "opencv-python>=4.5.0",
        "numpy>=1.21.0",
        "comet-ml>=3.31.0",
        "requests>=2.26.0",
        "lxml>=4.9.1",
        "xmltodict>=0.13.0",
        "python-telegram-bot>=20.0",
        "pandas>=1.3.0",
        "openpyxl>=3.0.9",
        "PyYAML>=6.0",
        "tqdm>=4.64.0",
        "scikit-learn>=1.0.0",
        "matplotlib>=3.5.0"
    ],
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "train-yolo=scripts.training.train_yolo:main",
            "auto-annotate=scripts.auto_annotation.auto_annotate:main",
            "notify-bot=scripts.utils.notify_bot:main"
        ]
    },
    author="Твой Ник",
    description="Проект модерации макетов с использованием ИИ",
    license="MIT",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
