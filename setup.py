"""stac_fastapi: HTML middleware module."""

from setuptools import find_namespace_packages, setup

with open("README.md") as f:
    desc = f.read()

install_requires = [
    "starlette",
    "jinja2>=2.11.2,<4.0.0",
]

extra_reqs = {
    "test": [
        "fastapi",
        "pytest",
        "pytest-cov",
        "pytest-asyncio",
        "httpx",
    ],
    "dev": [
        "pre-commit",
        "bump-my-version",
    ],
}


setup(
    name="stac-fastapi.html",
    description="A stac-fastapi middleware to encode response into HTML document.",
    long_description=desc,
    long_description_content_type="text/markdown",
    python_requires=">=3.9",
    classifiers=[
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Intended Audience :: Science/Research",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
    ],
    author="Vincent Sarago",
    author_email="vincent@developmentseed.com",
    url="https://github.com/developmentseed/stac-fastapi-html-middleware",
    license="MIT",
    packages=find_namespace_packages(exclude=["tests", "scripts"]),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=extra_reqs["dev"],
    extras_require=extra_reqs,
)
