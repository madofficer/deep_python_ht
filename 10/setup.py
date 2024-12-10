from setuptools import setup, Extension

setup(
    name="custom_json",
    version="1.0",
    ext_modules=[
        Extension("custom_json", sources=["custom_json.c"]),
    ],
)
