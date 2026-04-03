from fastapi import HTTPException, Request
import httpx
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api-gateway")

async def forward_request(method: str, url: str, request: Request = None, **kwargs):
    """
    Generic helper to forward a request to a microservice, including user identity headers.
    """
    headers = kwargs.get("headers", {})
    
    # If the request object is provided, extract user details from request state
    if request and hasattr(request, "state"):
        if hasattr(request.state, "user_id") and request.state.user_id:
            headers["X-User-Id"] = str(request.state.user_id)
        if hasattr(request.state, "role") and request.state.role:
            headers["X-User-Role"] = str(request.state.role)
        if hasattr(request.state, "nic") and request.state.nic:
            headers["X-User-NIC"] = str(request.state.nic)
            
    kwargs["headers"] = headers

    async with httpx.AsyncClient(trust_env=False, follow_redirects=True, timeout=30.0) as client:
        try:
            logger.info(f"Forwarding {method} request to {url}")
            response = await client.request(method, url, **kwargs)
            
            # Check for errors from the microservice
            if response.status_code >= 400:
                logger.error(f"Microservice error {response.status_code} from {url}: {response.text}")
                try:
                    detail = response.json()
                except:
                    detail = response.text
                raise HTTPException(status_code=response.status_code, detail=detail)
            
            return response.json() if response.status_code != 204 else {}
            
        except httpx.RequestError as exc:
            logger.error(f"HTTP Request failed to {url}: {exc!r}")
            raise HTTPException(status_code=503, detail=f"Service Unavailable logic failed for {url}: {type(exc).__name__} - {str(exc)}")
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            logger.error(f"Unexpected error: {exc}")
            raise HTTPException(status_code=500, detail="Internal Gateway Error")
