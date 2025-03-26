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

```bash
# regular request - return JSON document
$ curl http://127.0.0.1:8000 -s -D - -o /dev/null
HTTP/1.1 200 OK
date: Wed, 26 Mar 2025 11:16:18 GMT
server: uvicorn
content-length: 3001
content-type: application/json

# Ask for html with `Accept` header - return HTML document
$ curl http://127.0.0.1:8000 -s -D - -o /dev/null -H 'accept: text/html'
HTTP/1.1 200 OK
date: Wed, 26 Mar 2025 11:15:38 GMT
server: uvicorn
content-length: 3560
content-type: text/html

# Ask for html with `f=html` QueryParameter - return HTML document
$ curl http://127.0.0.1:8000\?f\=html -s -D - -o /dev/null
HTTP/1.1 200 OK
date: Wed, 26 Mar 2025 11:16:03 GMT
server: uvicorn
content-length: 3569
content-type: text/html
```

This middleware will also intercept the openapi document from stac-fastapi application to enhance the schemas by adding `f=html` query-parameter and `Accept: text/html` available headers.

<img width="800" alt="Screenshot 2025-03-25 at 3 16 44 PM" src="https://github.com/user-attachments/assets/07b53933-fbfd-4ba1-b654-6f2d72a2334b" />

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

:warning: You should place the `HTMLRenderMiddleware` before any `compression` middleware in the `middlewares` stack

```python
# NOK
api = StacApi(
    ...
    middlewares=[
        Middleware(BrotliMiddleware),
        Middleware(HTMLRenderMiddleware),
    ],
)
# OK
api = StacApi(
    ...
    middlewares=[
        Middleware(HTMLRenderMiddleware),  # <-- Put the HTML Render middleware before the compression middleware
        Middleware(BrotliMiddleware),
    ],
)
```

## HTML documents

See [docs/pages.md](docs/pages.md) for HTML preview


## Contribution & Development

See [CONTRIBUTING.md](https://github.com/developmentseed/stac-fastapi-html-middleware/blob/main/CONTRIBUTING.md)

## License

See [LICENSE](https://github.com/developmentseed/stac-fastapi-html-middleware/blob/main/LICENSE)

## Authors

Created by [Development Seed](<http://developmentseed.org>)

## Changes

See [CHANGES.md](https://github.com/developmentseed/stac-fastapi-html-middleware/blob/main/CHANGES.md).

