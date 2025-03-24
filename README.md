## stac-fastapi HTML middleware

<p align="center">
  <img width="500" src="https://github.com/user-attachments/assets/f243a238-5ba7-44da-963a-cd865578c2a5"/>
  <p align="center">stac-fastapi middleware to encode responses into HTML documents</p>
</p>
<p align="center">
  <a href="https://github.com/developmentseed/stac-fastapi-html-middleware/actions?query=workflow%3ACI" target="_blank">
      <img src="https://github.com/developmentseed/stac-fastapi-html-middleware/workflows/CI/badge.svg" alt="Test">
  </a>
  <a href="https://github.com/developmentseed/stac-fastapi-html-middleware/blob/main/LICENSE" target="_blank">
      <img src="https://img.shields.io/github/license/developmentseed/stac-fastapi-html-middleware.svg" alt="License">
  </a>
</p>


---

**Documentation**:

**Source Code**: <a href="https://github.com/developmentseed/stac-fastapi-html-middleware" target="_blank">https://github.com/developmentseed/stac-fastapi-html-middleware</a>

---

## Install

```bash
$ git clone https://github.com/developmentseed/stac-fastapi-html-middleware.git
$ cd stac-fastapi-html-middleware
$ python -m pip install -e .
```

## What

The `HTMLRenderMiddleware` is designed to intercept responses from stac-fastapi application (`json` or `geojson`) and to encode it to HTML responses when:
- the user set `f=html` query-parameter
- `Accept: text/html` request's headers is the highest *priority*

## How

```python
from starlette.middleware import Middleware

from stac_fastapi.api.app import StacApi
from stac_fastapi.html.middleware import HTMLRenderMiddleware

api = StacApi(
    middlewares=[
        Middleware(HTMLRenderMiddleware),
    ],
)
```

## Contribution & Development

See [CONTRIBUTING.md](https://github.com/developmentseed/stac-fastapi-html-middleware/blob/main/CONTRIBUTING.md)

## License

See [LICENSE](https://github.com/developmentseed/stac-fastapi-html-middleware/blob/main/LICENSE)

## Authors

Created by [Development Seed](<http://developmentseed.org>)

## Changes

See [CHANGES.md](https://github.com/developmentseed/stac-fastapi-html-middleware/blob/main/CHANGES.md).

