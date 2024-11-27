from datetime import datetime
from typing import List, Dict, Any, Optional
import httpx
from fastapi import Header, HTTPException
from urllib.parse import urljoin
import os
import pytz

# Global configuration
show_result_in_my_local_time: bool = True
get_timestamp_in_my_local_time: bool = True
token_global: Optional[str] = None

def convert_time(
    start_date: str,
    end_date: str,
    convert_to_local: bool = get_timestamp_in_my_local_time
) -> tuple[int, int]:
    """
    Convert datetime strings to millisecond timestamps.
    
    Args:
        start_date: Start date string in ISO format
        end_date: End date string in ISO format
        convert_to_local: Whether to convert to local timezone
        
    Returns:
        Tuple of start and end timestamps in milliseconds
    """
    date_formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"]
    
    for date_format in date_formats:
        try:
            if convert_to_local:
                utc_time_start = datetime.strptime(start_date, date_format).replace(tzinfo=pytz.UTC)
                utc_time_stop = datetime.strptime(end_date, date_format).replace(tzinfo=pytz.UTC)
            else:
                utc_time_start = datetime.strptime(start_date, date_format)
                utc_time_stop = datetime.strptime(end_date, date_format)
            break
        except ValueError:
            continue
    else:
        raise HTTPException(
            status_code=400,
            detail=f"Time format error. Ensure the format is one of {date_formats}."
        )

    start_time_millis = int(utc_time_start.timestamp() * 1000)
    end_time_millis = int(utc_time_stop.timestamp() * 1000)

    return start_time_millis, end_time_millis

async def get_token_header(authorization: str = Header(...)) -> str:
    """
    Extract Bearer token from authorization header.
    
    Args:
        authorization: Authorization header value
        
    Returns:
        The token string
        
    Raises:
        HTTPException: If authorization header is invalid
    """
    if authorization.startswith("Bearer "):
        return authorization[7:]
    raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")

async def fetch_all_telemetry(
    entityType: str,
    client: httpx.AsyncClient,
    entityId: str,
    start_time_millis: int,
    end_time_millis: int,
    limit: int,
    interval: Optional[int] = 0,
    agg: Optional[str] = None,
    telemetry_keys: Optional[List[str]] = None,
    token: Optional[str] = None
) -> Dict[str, Any]:
    """
    Fetch telemetry data for an entity.
    
    Args:
        entityType: Type of entity
        client: HTTPX client instance
        entityId: ID of the entity
        start_time_millis: Start time in milliseconds
        end_time_millis: End time in milliseconds
        limit: Maximum number of records to return
        interval: Time interval for aggregation
        agg: Aggregation function
        telemetry_keys: List of telemetry keys to fetch
        token: Authentication token
        
    Returns:
        Dictionary containing telemetry data
        
    Raises:
        ValueError: If BASE_URL is not set or telemetry_keys is invalid
        HTTPException: If the API request fails
    """
    base_url = os.getenv('BASE_URL')

    if not base_url:
        raise ValueError("BASE_URL environment variable is not set")

    entity_url = urljoin(base_url, f'/api/plugins/telemetry/{entityType}/{entityId}/values/timeseries')
    
    params = {
        "startTs": start_time_millis,
        "endTs": end_time_millis,
        "limit": limit
    }
    
    if interval is not None:
        params["interval"] = interval
    if agg is not None:
        params["agg"] = agg
        
    if telemetry_keys:
        if not isinstance(telemetry_keys, list) or not all(isinstance(k, str) for k in telemetry_keys):
            raise ValueError("telemetry_keys must be a list of strings")
        params["keys"] = ",".join(telemetry_keys)

    headers = {'Authorization': f'Bearer {token or token_global}'}
    
    response = await client.get(entity_url, headers=headers, params=params)
    response.raise_for_status()
    
    return response.json()