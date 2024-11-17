# snowflake_utils.py

import os
import json
import snowflake.connector
from typing import Dict, List, Any

# Configure Snowflake connection parameters via environment variables for security
SNOWFLAKE_USER = os.getenv('SNOWFLAKE_USER')
SNOWFLAKE_PASSWORD = os.getenv('SNOWFLAKE_PASSWORD')
SNOWFLAKE_ACCOUNT = os.getenv('SNOWFLAKE_ACCOUNT')
SNOWFLAKE_WAREHOUSE = os.getenv('SNOWFLAKE_WAREHOUSE')
SNOWFLAKE_DATABASE = os.getenv('SNOWFLAKE_DATABASE')
SNOWFLAKE_SCHEMA = os.getenv('SNOWFLAKE_SCHEMA')

def get_snowflake_connection():
    return snowflake.connector.connect(
        user=SNOWFLAKE_USER,
        password=SNOWFLAKE_PASSWORD,
        account=SNOWFLAKE_ACCOUNT,
        warehouse=SNOWFLAKE_WAREHOUSE,
        database=SNOWFLAKE_DATABASE,
        schema=SNOWFLAKE_SCHEMA
    )

async def save_telemetry_data(table_name: str, telemetry: Dict[str, List[Dict[str, Any]]]):
    """
    Saves telemetry data to a specified Snowflake table.

    :param table_name: Name of the table to save data into.
    :param telemetry: Telemetry data as a dictionary.
    """
    # Connect to Snowflake
    conn = get_snowflake_connection()
    try:
        cursor = conn.cursor()

        # Extract all telemetry keys (columns)
        telemetry_keys = list(telemetry.keys())

        # Define table schema: ts (timestamp) and one column per telemetry key
        # Adjust data types as necessary
        columns_def = ', '.join([f"{key} STRING" for key in telemetry_keys])
        create_table_sql = f"""
        CREATE TABLE IF NOT EXISTS {table_name} (
            ts BIGINT,
            {columns_def}
        )
        """
        cursor.execute(create_table_sql)

        # Prepare insert statement
        placeholders = ', '.join(['%s'] * (1 + len(telemetry_keys)))  # ts + telemetry values
        columns = ', '.join(['ts'] + telemetry_keys)
        insert_sql = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders})"

        # Collect all unique timestamps
        ts_set = set()
        for records in telemetry.values():
            for record in records:
                ts_set.add(record['ts'])
        sorted_ts = sorted(ts_set)

        # Create a mapping from telemetry key to ts to value
        telemetry_map = {key: {record['ts']: record['value'] for record in records} for key, records in telemetry.items()}

        # Prepare rows for insertion
        rows = []
        for ts in sorted_ts:
            row = [ts]
            for key in telemetry_keys:
                value = telemetry_map[key].get(ts, None)
                row.append(value)
            rows.append(tuple(row))

        # Insert data in batches
        cursor.executemany(insert_sql, rows)

        # Commit the transaction
        conn.commit()
    except Exception as e:
        # Handle exceptions (e.g., log them)
        print(f"Error saving telemetry data to Snowflake: {e}")
        raise e
    finally:
        cursor.close()
        conn.close()
