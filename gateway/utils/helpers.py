from fastapi import HTTPException
import httpx
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("api-gateway")

async def forward_request(method: str, url: str, **kwargs):
    """
    Generic helper to forward a request to a microservice.
    """
    async with httpx.AsyncClient() as client:
        try:
            logger.info(f"Forwarding {method} request to {url}")
            response = await client.request(method, url, **kwargs)
            
            # Check for errors from the microservice
            if response.status_code >= 400:
                logger.error(f"Microservice error: {response.status_code} - {response.text}")
                try:
                    detail = response.json()
                except:
                    detail = response.text
                raise HTTPException(status_code=response.status_code, detail=detail)
            
            return response.json()
            
        except httpx.RequestError as exc:
            logger.error(f"HTTP Request failed: {exc}")
            raise HTTPException(status_code=503, detail=f"Service Unavailable: {str(exc)}")
        except HTTPException as exc:
            raise exc
        except Exception as exc:
            logger.error(f"Unexpected error: {exc}")
            raise HTTPException(status_code=500, detail="Internal Gateway Error")
