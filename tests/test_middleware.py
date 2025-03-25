"""test middleware."""

import json
import os
from typing import Optional

import pytest
from fastapi import FastAPI
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.testclient import TestClient

from stac_fastapi.html.middleware import HTMLRenderMiddleware, preferred_encoding

fixtures_dir = os.path.join(os.path.dirname(__file__), "fixtures")

collections_data = json.load(open(os.path.join(fixtures_dir, "collections.json"), "r"))
conformances_data = json.load(open(os.path.join(fixtures_dir, "conformances.json"), "r"))
items_data = json.load(open(os.path.join(fixtures_dir, "items.json"), "r"))
landing_data = json.load(open(os.path.join(fixtures_dir, "landing.json"), "r"))
search_data = json.load(open(os.path.join(fixtures_dir, "search.json"), "r"))
queryables_data = json.load(open(os.path.join(fixtures_dir, "queryables.json"), "r"))
collection_queryables_data = json.load(
    open(os.path.join(fixtures_dir, "collection_queryables.json"), "r")
)


class GeoJSONResponse(JSONResponse):
    """JSON with custom, vendor content-type."""

    media_type = "application/geo+json"


class JSONSchemaResponse(JSONResponse):
    """JSON with custom, vendor content-type."""

    media_type = "application/schema+json"


@pytest.mark.parametrize(
    "header,expected",
    [
        ("deflate, gzip;q=0.8", ["deflate"]),
        ("deflate, gzip;q=0.8", ["deflate"]),
        ("br;q=1.0, gzip;q=0.8", ["br"]),
        ("br;q=1.0, gzip;q=1.0", ["br", "gzip"]),
        ("*;q=1.0", ["*"]),
        ("br;q=aaa, gzip", ["gzip"]),
        ("br;q=0.0, gzip", ["gzip"]),
        ("", None),
    ],
)
def test_get_compression_backend(header, expected):
    """Make sure we use the right compression."""
    assert preferred_encoding(header) == expected


@pytest.fixture
def client():  # noqa: C901
    app = FastAPI(
        openapi_url="/api",
        docs_url="/api.html",
    )
    app.add_middleware(HTMLRenderMiddleware)

    @app.get("/", name="Landing Page")
    async def landing(request: Request):
        return JSONResponse(landing_data, status_code=200)

    @app.get("/conformance", name="Conformance Classes")
    async def conformance(request: Request):
        return JSONResponse(conformances_data, status_code=200)

    @app.get("/collections", name="Get Collections")
    async def all_collections(request: Request):
        return JSONResponse(collections_data, status_code=200)

    @app.get("/collections/{collectionId}", name="Get Collection")
    async def get_collection(request: Request, collectionId: str):
        return JSONResponse(collections_data["collections"][0], status_code=200)

    @app.get("/collections/{collectionId}/items", name="Get ItemCollection")
    async def item_collection(request: Request, collectionId: str):
        return GeoJSONResponse(items_data, status_code=200)

    @app.get("/collections/{collectionId}/items/{itemId}", name="Get Item")
    async def get_item(request: Request, collectionId: str, itemId: str):
        return GeoJSONResponse(items_data["features"][0], status_code=200)

    @app.get("/search", name="Search")
    async def get_search(request: Request):
        return GeoJSONResponse(search_data, status_code=200)

    @app.post("/search", name="Search")
    async def post_search(request: Request):
        return GeoJSONResponse(search_data, status_code=200)

    @app.get("/queryables", name="Queryables")
    async def get_queryables(request: Request, collectionId: Optional[str] = None):
        return JSONSchemaResponse(queryables_data, status_code=200)

    @app.get("/collections/{collectionId}/queryables", name="Collection Queryables")
    async def get_collection_queryables(
        request: Request, collectionId: Optional[str] = None
    ):
        return JSONSchemaResponse(collection_queryables_data, status_code=200)

    with TestClient(app) as client:
        yield client


def test_html_middleware(client):
    """Test HTMLRenderMiddleware middleware."""
    response = client.get("/", headers={"Accept": "application/json"})
    assert response.headers["Content-Type"] == "application/json"

    response = client.get("/", headers={"Accept": "*"})
    assert response.headers["Content-Type"] == "text/html"

    response = client.get("/", headers={"Accept": "text/html"})
    assert response.headers["Content-Type"] == "text/html"

    response = client.get("/", params={"f": "html"})
    assert response.headers["Content-Type"] == "text/html"

    response = client.get("/", params={"f": "yo"})
    assert response.headers["Content-Type"] == "application/json"

    response = client.get(
        "/", params={"f": "html"}, headers={"Accept": "application/json"}
    )
    assert response.headers["Content-Type"] == "text/html"

    # No HTML response for POST request
    response = client.post("/search", headers={"Accept": "text/html"})
    assert response.headers["Content-Type"] == "application/geo+json"

    # No influence on endpoint outside stac-fastapi scope
    response = client.get("/api", headers={"Accept": "text/html"})
    assert response.headers["Content-Type"] == "application/json"


@pytest.mark.parametrize(
    "route,accept,result",
    [
        ("/", "text/html", "text/html"),
        ("/conformance", "text/html", "text/html"),
        ("/collections", "text/html", "text/html"),
        ("/collections/my_collection", "text/html", "text/html"),
        ("/collections/my_collection/items", "text/html", "text/html"),
        ("/collections/my_collection/items/item_1", "text/html", "text/html"),
        ("/search", "text/html", "text/html"),
        ("/queryables", "text/html", "text/html"),
        ("/collections/my_collection/queryables", "text/html", "text/html"),
    ],
)
def test_all_routes(client, route, accept, result):
    response = client.get(route, headers={"accept": accept})
    assert response.headers["Content-Type"] == result
