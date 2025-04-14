import httpx





# Shared client instance (optional: you can also create a new one per request)
_client: httpx.AsyncClient | None = None

async def get_http_client() -> httpx.AsyncClient:
    global _client
    if _client is None:
        _client = httpx.AsyncClient()
    return _client
