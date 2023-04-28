from setuptools import find_packages, setup

setup(
    name="smarterTuition",
    version="1.0.0",
    description="Procekt Smarter Tuition by Nadja Merkl & Vincent Gundelwein.",
    url="https://github.com/SmarterTuition/ProjektST",
    author="IMS Developers",
    author_email="IMS-Developers@rki.de",
    license="MIT",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=["os", "numpy", "pandas", "PyQt6", "sklearn.model_selection", "xqboost", "scikit-learn", "sys", "openpyxl"],
    entry_points={
        "console_scripts": ["ki=src.main:main"],
    },
    classifiers=["Programming Language :: Python :: 3.8", "Programming Language :: Python :: 3.9"],
)
