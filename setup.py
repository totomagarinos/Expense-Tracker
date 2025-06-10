from setuptools import setup

setup(
  name="sales-tracker",
  version="1.0.0",
  description="A simple command-line sales tracker",
  author="Juan Cruz Magariños",
  py_modules=["sales_tracker"],
  entry_points={
    "console_scripts": [
      "sales-cli=sales_tracker:main",
    ],
  }
)