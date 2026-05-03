from setuptools import setup

setup(
    name="task-cli",
    version="1.0.0",
    py_modules=["task_cli"],
    install_requires=[],
    entry_points={
        'console_scripts': [
            'task-cli = task_cli:main',
        ],
    },
)