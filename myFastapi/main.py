from typing import List, Dict, Any, Set, Tuple, Optional
import httpx
from fastapi import FastAPI, HTTPException, Path, Query, Depends, Body

try:
    from myFastapi.funtions import convert_time, fetch_all_telemetry
except:
    from funtions import convert_time, fetch_all_telemetry

try:
    from myFastapi.s3_script import *
except:
    from s3_script import *


from pydantic import BaseModel
token_global = ""
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

base_url = os.getenv('BASE_URL')
region_aws = os.getenv('AWS_DEFAULT_REGION')


AWS_ACCESS_KEY_ID = os.getenv('AWS_ACCESS_KEY_ID')
AWS_SECRET_ACCESS_KEY = os.getenv('AWS_SECRET_ACCESS_KEY')
S3_ENDPOINT_URL = os.getenv('S3_ENDPOINT_URL')



app = FastAPI()

if not base_url:
    raise ValueError("BASE_URL environment variable is not set")
login_url = f"{base_url}/api/auth/login"

class CustomLoginForm(BaseModel):
    username: str
    password: str

@app.post("/login")
async def login(form_data: CustomLoginForm = Depends()):
    global token_global
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(login_url, json={
                "username": form_data.username,
                "password": form_data.password
            })
            response.raise_for_status()
        except httpx.HTTPError as exc:
            raise HTTPException(status_code=exc.response.status_code if exc.response else 500,
                                detail=str(exc)) from exc
        data = response.json()
        token = data.get("token")
        if not token:
            raise HTTPException(status_code=500, detail="Token not found in response")
        token_global = token
        return {"token": token_global}
    



# Instantiate the MinIOClient
s3_client = S3Client(
    bucket_name='fastapi-snowflake',
    region=region_aws,
    aws_access_key_id=AWS_ACCESS_KEY_ID,
    aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
    endpoint_url=S3_ENDPOINT_URL  
)


@app.get("/get-elements")

async def get_elements_by_id(
    entityType: str = Query(..., description="String value representing the entity type. For example, 'DEVICE'"),
    entityId: str = Query(..., description="A string value representing the entity id. For example, '784f394c-42b6-435a-983c-b7beff2784f9'"),
    start_date: str = Query(..., description="Start time/date in UTC format, e.g., '2024-01-01T00:00:00.000Z'", alias="start-date"),
    end_date: str = Query(..., description="End time/date in UTC format, e.g., '2023-04-23T17:25:43.511Z'", alias="end-date"),
    interval : Optional[int] = Query(..., description="A long value representing the aggregation interval range in milliseconds. Default value : 0", alias="interval"),
    agg : Optional[int]=Query(..., description="A string value representing the aggregation function. If the interval is not specified, 'agg' parameter will use 'NONE' value. \
    Available values : MIN, MAX, AVG, SUM, COUNT, NONE", alias="aggregation_function"),
    telemetry_keys: Optional[str] = Query(None, description="Comma-separated list of telemetry keys."),
    table_name:  Optional[str] = Query(None, description="The table name for the telemetry data"),
    LIMIT : Optional[str] = Query(100, description="The table name for the telemetry data"),
    savebase: bool = Query(False, description="Whether to save data to S3")
):
    global token_global 
    if not token_global:
        raise HTTPException(status_code=401, detail="User not authenticated. Please login. There is no token_global.")

    # Convert start_date and end_date to milliseconds
    start_time_millis, end_time_millis = convert_time(start_date, end_date)

    # Convert telemetry_keys to a list
    telemetry_keys_list = telemetry_keys.split(",") if telemetry_keys else None

    async with httpx.AsyncClient() as client:
        telemetry = await fetch_all_telemetry(
            entityType=entityType,
            client=client,
            entityId=entityId,
            start_time_millis=start_time_millis,
            end_time_millis=end_time_millis,
            telemetry_keys=telemetry_keys_list,
            interval=interval,
            agg=agg,
            token=token_global,
            limit=LIMIT
        )
        if savebase:
            success = s3_client.save_telemetry(telemetry, table_name)
            if not success:
                raise HTTPException(status_code=500, detail="Failed to save data to S3")


     
    return telemetry 





