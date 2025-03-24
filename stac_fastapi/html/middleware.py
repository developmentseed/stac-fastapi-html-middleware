"""stac-fastapi HTML middlewares."""

import json
import re
from typing import Any, List, Optional

import jinja2
from stac_pydantic.shared import MimeTypes
from starlette.datastructures import MutableHeaders
from starlette.requests import Request
from starlette.templating import Jinja2Templates, _TemplateResponse
from starlette.types import ASGIApp, Message, Receive, Scope, Send

jinja2_env = jinja2.Environment(
    loader=jinja2.ChoiceLoader(
        [
            jinja2.PackageLoader(__package__, "templates"),
        ]
    )
)
DEFAULT_TEMPLATES = Jinja2Templates(env=jinja2_env)


def preferred_encoding(accept: str) -> Optional[List[str]]:
    """Return encoding preference matrix.

    Links:
    - https://www.w3.org/Protocols/rfc2616/rfc2616-sec14.html
    - https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Accept

    """
    accept_values = {}
    for m in accept.replace(" ", "").split(","):
        values = m.split(";")
        if len(values) == 1:
            name = values[0]
            quality = 1.0
        else:
            name = values[0]
            groups = dict([param.split("=") for param in values[1:]])  # type: ignore
            try:
                q = groups.get("q")
                quality = float(q) if q else 1.0
            except ValueError:
                quality = 0

        # if quality is 0 we ignore encoding
        if quality:
            accept_values[name] = quality

    # Create Preference matrix
    encoding_preference = {
        v: [n for (n, q) in accept_values.items() if q == v]
        for v in sorted(set(accept_values.values()), reverse=True)
    }

    return next(iter(encoding_preference.values())) if encoding_preference else None


class HTMLRenderMiddleware:
    """MiddleWare to return HTML response from stac-fastapi."""

    def __init__(self, app: ASGIApp, templates: Optional[Jinja2Templates] = None) -> None:
        """Init Middleware.

        Args:
            app (ASGIApp): starlette/FastAPI application.

        """
        self.app = app
        self.initial_message = {}  # type: Message
        self.templates = templates or DEFAULT_TEMPLATES

    def create_html_response(
        self,
        request: Request,
        data: Any,
        template_name: str,
        title: Optional[str] = None,
        router_prefix: Optional[str] = None,
        **kwargs: Any,
    ) -> _TemplateResponse:
        """Create Template response."""
        router_prefix = request.app.state.router_prefix

        urlpath = request.url.path
        if root_path := request.app.root_path:
            urlpath = re.sub(r"^" + root_path, "", urlpath)

        if router_prefix:
            urlpath = re.sub(r"^" + router_prefix, "", urlpath)

        crumbs = []
        baseurl = str(request.base_url).rstrip("/")

        if router_prefix:
            baseurl += router_prefix

        crumbpath = str(baseurl)
        if urlpath == "/":
            urlpath = ""

        for crumb in urlpath.split("/"):
            crumbpath = crumbpath.rstrip("/")
            part = crumb
            if part is None or part == "":
                part = "Home"
            crumbpath += f"/{crumb}"
            crumbs.append({"url": crumbpath.rstrip("/"), "part": part.capitalize()})

        return self.templates.TemplateResponse(
            request,
            name=f"{template_name}.html",
            context={
                "response": data,
                "template": {
                    "api_root": baseurl,
                    "params": request.query_params,
                    "title": title or template_name,
                },
                "crumbs": crumbs,
                "url": baseurl + urlpath,
                "params": str(request.url.query),
                **kwargs,
            },
        )

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        """Handle call."""
        if scope["type"] != "http":
            await self.app(scope, receive, send)
            return

        request = Request(scope)
        qs = dict(request.query_params)

        endpoint_templates = {
            # endpoint Name: template name
            "Landing Page": "landing",
            "Conformance Classes": "conformances",
            "Get Collections": "collections",
            "Get Collection": "collection",
            "Get ItemCollection": "items",
            "Get Item": "item",
            "Search": "search",
            # Extensions
            "Queryables": "queryables",
            "Collection Queryables": "queryables",
        }

        pref_encoding = preferred_encoding(request.headers.get("accept", "")) or []
        output_type: Optional[MimeTypes] = None
        if qs.get("f", "") == "html":
            output_type = MimeTypes.html
        elif "text/html" in pref_encoding and not qs.get("f", ""):
            output_type = MimeTypes.html

        async def send_wrapper(message: Message):
            """Send Message."""
            message_type = message["type"]

            if message_type == "http.response.start":
                self.initial_message = message

            elif message_type == "http.response.body":
                headers = MutableHeaders(raw=self.initial_message["headers"])

                if (
                    scope["method"] == "GET"
                    and self.initial_message["status"] == 200
                    and output_type
                ):
                    if tpl := endpoint_templates.get(scope["route"].name):
                        headers["content-type"] = "text/html"
                        message["body"] = self.create_html_response(
                            request,
                            json.loads(message["body"].decode()),
                            template_name=tpl,
                            title=scope["route"].name,
                        ).body

                        headers["Content-Encoding"] = "text/html"
                        headers["Content-Length"] = str(len(message["body"]))

                await send(self.initial_message)
                await send(message)

            else:
                await send(self.initial_message)
                await send(message)

        await self.app(scope, receive, send_wrapper)
