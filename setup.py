from setuptools import setup

setup(
    name="matchy",
    version="0.1",
    py_modules=["matchy"],
    include_package_data=True,
    install_requires=["click", "numpy"],
    entry_points="""
        [console_scripts]
        matchy=matchy.cli:cli
    """,
)
