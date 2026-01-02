from datetime import date
from fastapi import Request, HTTPException

# In-memory store (MVP)
usage_store = {}

DAILY_LIMIT = 5


def check_rate_limit(request: Request):
    client_ip = request.client.host
    today = date.today().isoformat()

    key = f"{client_ip}:{today}"

    current_count = usage_store.get(key, 0)

    if current_count >= DAILY_LIMIT:
        raise HTTPException(
            status_code=429,
            detail="Daily free limit reached. Please try again tomorrow."
        )

    usage_store[key] = current_count + 1
