from setuptools import setup

setup(
  name="expense-tracker",
  version="1.0.0",
  description="A simple command-line expense tracker",
  author="Juan Cruz Magariños",
  py_modules=["expense_tracker"],
  entry_points={
    "console_scripts": [
      "expense-cli=expense_tracker:main",
    ],
  }
)