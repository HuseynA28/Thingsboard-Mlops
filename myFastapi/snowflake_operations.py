from typing import Dict, List, Any
import os
from datetime import datetime
from dotenv import load_dotenv
import snowflake.connector
from pydantic import BaseModel
from fastapi import HTTPException

# Load environment variables
load_dotenv()

class TelemetryData(BaseModel):
    ts: int
    value: str

class SnowflakeConfig:
    def __init__(self):
        self.account = os.getenv("SNOWFLAKE_ACCOUNT")
        self.user = os.getenv("SNOWFLAKE_USER")
        self.password = os.getenv("SNOWFLAKE_PASSWORD")
        self.database = os.getenv("SNOWFLAKE_DATABASE")
        self.schema = os.getenv("SNOWFLAKE_SCHEMA")
        self.warehouse = os.getenv("SNOWFLAKE_WAREHOUSE")
        
        if not all([self.account, self.user, self.password, self.database, self.schema, self.warehouse]):
            raise ValueError("Missing required Snowflake configuration in .env file")

class SnowflakeOperations:
    def __init__(self):
        self.config = SnowflakeConfig()
        
    def get_connection(self):
        return snowflake.connector.connect(
            account=self.config.account,
            user=self.config.user,
            password=self.config.password,
            database=self.config.database,
            schema=self.config.schema,
            warehouse=self.config.warehouse
        )

    def create_table_if_not_exists(self, table_name: str, column_name: str):
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            ENTITY_ID VARCHAR(255),
            TELEMETRY_KEY VARCHAR(255),
            TIMESTAMP TIMESTAMP_NTZ,
            VALUE VARCHAR(255),
            CREATED_AT TIMESTAMP_NTZ DEFAULT CURRENT_TIMESTAMP()
        )
        """
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                cursor.execute(create_table_sql)
            except Exception as e:
                raise HTTPException(status_code=500, detail=f"Failed to create table: {str(e)}")
            finally:
                cursor.close()

    async def save_telemetry_data(self, entity_id: str, telemetry_data: Dict[str, List[Dict[str, Any]]]):
        table_name = "DEVICE_TELEMETRY"
        
        with self.get_connection() as conn:
            cursor = conn.cursor()
            try:
                # Ensure table exists
                self.create_table_if_not_exists(table_name, "VALUE")
                
                # Prepare insert statement
                insert_sql = f"""
                INSERT INTO {table_name} 
                (ENTITY_ID, TELEMETRY_KEY, TIMESTAMP, VALUE)
                VALUES (%s, %s, %s, %s)
                """
                
                # Process each telemetry key and its data
                for telemetry_key, measurements in telemetry_data.items():
                    for measurement in measurements:
                        timestamp = datetime.fromtimestamp(measurement["ts"] / 1000)  # Convert milliseconds to seconds
                        value = measurement["value"]
                        
                        cursor.execute(
                            insert_sql,
                            (entity_id, telemetry_key, timestamp, value)
                        )
                
                conn.commit()
                return {"message": f"Successfully saved {len(telemetry_data)} telemetry keys to Snowflake"}
                
            except Exception as e:
                conn.rollback()
                raise HTTPException(status_code=500, detail=f"Failed to save data to Snowflake: {str(e)}")
            finally:
                cursor.close()