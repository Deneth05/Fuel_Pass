import asyncio
import httpx

async def test_endpoint():
    url = "http://127.0.0.1:8006/quotas/vehicle/69d0b4c10da910fd899a125d"
    headers = {
        "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyNTQxMjM2OTg3ViIsInJvbGUiOiJhZG1pbiIsImV4cCI6MTc3NTM3MTgwOH0.LHiwf2EgOCaPTO9YrO7BGRq8Gm4rMLpvJYkaTNqUXOc"
    }
    
    async with httpx.AsyncClient() as client:
        try:
            resp = await client.get(url, headers=headers)
            print(f"STATUS: {resp.status_code}")
            print(f"BODY: {resp.text}")
        except Exception as e:
            print(f"ERROR: {str(e)}")

if __name__ == "__main__":
    asyncio.run(test_endpoint())
