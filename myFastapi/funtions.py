from datetime import datetime
from typing import List, Dict, Any, Set, Tuple, Optional
import httpx
from fastapi import Header, HTTPException, Depends
from urllib.parse import urljoin, urlencode
import os
from fastapi import HTTPException
import pytz

show_result_in_my_local_time = True
get_timestamp_in_my_local_time = True
token_global = None  # Initialize token_global

def convert_time(start_date, end_date, convert_to_local=get_timestamp_in_my_local_time):
    date_formats = ["%Y-%m-%dT%H:%M:%S.%fZ", "%Y-%m-%dT%H:%M:%SZ"]
    for date_format in date_formats:
        try:
            if convert_to_local:
                utc_time_start = datetime.strptime(start_date, date_format).replace(tzinfo=pytz.utc)
                utc_time_stop = datetime.strptime(end_date, date_format).replace(tzinfo=pytz.utc)
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



async def get_token_header(authorization: str = Header(...)):
    if authorization.startswith("Bearer "):
        return authorization[7:]
    else:
        raise HTTPException(status_code=401, detail="Invalid or missing Authorization header")


async def fetch_all_telemetry(
    entityType: str,
    client: httpx.AsyncClient,
    entityId: str,
    start_time_millis: int,
    end_time_millis: int,
    limit: int, 
    interval=Optional[int]=0,
    agg=Optional[str]=None,
    telemetry_keys: Optional[List[str]] = None,
    token: str = token_global,

) -> Dict[str, Any]:

    base_url = os.getenv('BASE_URL')
    if not base_url:
        raise ValueError("BASE_URL environment variable is not set")

    entity_url = urljoin(base_url, f'/api/plugins/telemetry/{entityType}/{entityId}/values/timeseries')
    params = {
        "startTs": start_time_millis,
        "endTs": end_time_millis,
        "limit": limit
    }
    if telemetry_keys:
        if isinstance(telemetry_keys, list) and all(isinstance(k, str) for k in telemetry_keys):
            keys_str = ",".join(telemetry_keys)
            params["keys"] = keys_str
        else:
            raise ValueError("telemetry_keys must be a list of strings")
    headers = {'Authorization': f'Bearer {token}'}
    response = await client.get(entity_url, headers=headers, params=params)
    response.raise_for_status()
    telemetry = response.json()
    return telemetry

