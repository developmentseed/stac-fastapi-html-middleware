# Development - Contributing

Issues and pull requests are more than welcome: https://github.com/developmentseed/stac-fastapi-html-middleware/issues

**dev install**

```bash
git clone https://github.com/developmentseed/stac-fastapi-html-middleware.git
cd stac-fastapi-html-middleware
python -m pip install -e .["dev"]
```

You can then run the tests with the following command:

```sh
python -m pytest --cov stac-fastapi-html --cov-report term-missing --asyncio-mode=strict
```

**pre-commit**

This repo is set to use `pre-commit` to run *isort*, *flake8*, *pydocstring*, *black* ("uncompromising Python code formatter") and mypy when committing new code.

```bash
# Install pre-commit command
$ pip install pre-commit

# Setup pre-commit withing your local environment
$ pre-commit install
```
