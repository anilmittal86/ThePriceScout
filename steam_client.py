
import httpx
import logging
import asyncio
from typing import Optional, Dict, Any

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

STEAM_API_URL = "https://store.steampowered.com/api/appdetails"

async def fetch_game_price(app_id: int) -> Optional[Dict[str, Any]]:
    """
    Fetch game details from Steam Store API.
    Ensures prices are in INR (cc=in).
    Handles rate limits (429) with exponential backoff.
    Returns: {'name': str, 'price': float, 'currency': 'INR', 'discount': int}
    """
    params = {
        "appids": app_id,
        "cc": "in",  # Currency Code: Indian Rupee
        "l": "english"
    }
    
    headers = {
        "User-Agent": "SteamPriceTracker/1.0"
    }
    
    retries = 3
    backoff = 1
    
    for attempt in range(retries):
        try:
            async with httpx.AsyncClient() as client:
                response = await client.get(STEAM_API_URL, params=params, headers=headers)
            
            if response.status_code == 429:
                logger.warning(f"Rate limited. Waiting {backoff} seconds...")
                await asyncio.sleep(backoff)
                backoff *= 2
                continue
            
            if response.status_code != 200:
                logger.error(f"Failed to fetch data for {app_id}: Status {response.status_code}")
                return None
            
            data = response.json()
            app_data = data.get(str(app_id))
            
            if not app_data or not app_data.get("success"):
                logger.error(f"API request failed or success=False for {app_id}")
                return None
                
            game_data = app_data["data"]
            
            # Default values
            price = 0.0
            currency = "INR"
            discount = 0
            
            if game_data.get("is_free"):
                price = 0.0
                discount = 0
            elif "price_overview" in game_data:
                price_data = game_data["price_overview"]
                # Steam price is in cents/paisa
                price = price_data["final"] / 100
                currency = price_data["currency"]
                discount = price_data["discount_percent"]
            
            return {
                "name": game_data["name"],
                "price": price,
                "currency": currency,
                "discount": discount
            }

        except httpx.RequestError as e:
            logger.error(f"Request error: {e}")
            await asyncio.sleep(backoff)
            backoff *= 2
    
    logger.error(f"Max retries reached for {app_id}")
    return None

if __name__ == "__main__":
    # Test directly
    async def main():
        print(await fetch_game_price(813780)) # AOE II DE
    asyncio.run(main())
