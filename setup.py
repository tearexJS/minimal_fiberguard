from setuptools import setup, find_packages

setup(
    name="fiber-guard",
    version="0.1.0",
    author="noper nopers",
    author_email="noper@nopers.com",
    description="GUI and backend for fast change polarization detector",
    python_requires=">=3.6",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "fiber-guard = fiber_guard.__main__:main",
        ],
    },
    install_requires=[
        "h5py",
        "numpy",
        "sklearn",
        "scipy",
        "matplotlib",
        "numba",
        "joblib",
        "tqdm",
        "torch",
    ],
)
