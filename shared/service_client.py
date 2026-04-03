import httpx
import os
from fastapi import Request, HTTPException
from typing import Any, Dict, Optional

class ServiceClient:
    def __init__(self, base_url: str, service_name: str):
        self.base_url = base_url.rstrip("/")
        self.service_name = service_name

    async def _request(
        self, 
        method: str, 
        path: str, 
        request: Optional[Request] = None,
        **kwargs
    ) -> Dict[str, Any]:
        url = f"{self.base_url}/{path.lstrip('/')}"
        
        # Prepare headers
        headers = kwargs.pop("headers", {})
        if request:
            # Forward user context headers
            for header in ["X-User-Id", "X-User-Role", "X-User-NIC"]:
                val = request.headers.get(header)
                if val:
                    headers[header] = val
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.request(method, url, headers=headers, **kwargs)
                if response.status_code >= 400:
                    try:
                        detail = response.json()
                    except:
                        detail = response.text
                    raise HTTPException(status_code=response.status_code, detail=detail)
                return response.json() if response.status_code != 204 else {}
            except httpx.RequestError as exc:
                raise HTTPException(
                    status_code=503, 
                    detail=f"Upstream service unavailable: {self.service_name}"
                )

    async def get(self, path: str, request: Optional[Request] = None, **kwargs):
        return await self._request("GET", path, request, **kwargs)

    async def post(self, path: str, request: Optional[Request] = None, **kwargs):
        return await self._request("POST", path, request, **kwargs)

    async def put(self, path: str, request: Optional[Request] = None, **kwargs):
        return await self._request("PUT", path, request, **kwargs)

    async def patch(self, path: str, request: Optional[Request] = None, **kwargs):
        return await self._request("PATCH", path, request, **kwargs)

    async def delete(self, path: str, request: Optional[Request] = None, **kwargs):
        return await self._request("DELETE", path, request, **kwargs)
