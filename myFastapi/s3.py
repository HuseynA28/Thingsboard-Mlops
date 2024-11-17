
from typing import List, Dict, Any, Set, Tuple, Optional
import boto3
from botocore.exceptions import ClientError
from typing import Dict
import json
import boto3
from botocore.exceptions import ClientError
import json
from typing import Dict, Optional


class S3Client:
    def __init__(
        self,
        bucket_name: str,
        region: str = 'us-east-1',
        aws_access_key_id: Optional[str] = None,
        aws_secret_access_key: Optional[str] = None,
        endpoint_url: Optional[str] = None
    ):
        self.bucket_name = bucket_name
        self.s3_client = boto3.client(
            's3',
            region_name=region,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key,
            endpoint_url=endpoint_url  # Use this if you're using MinIO or a custom S3 endpoint
        )
        self._ensure_bucket_exists()

    def _ensure_bucket_exists(self) -> None:
        try:
            self.s3_client.head_bucket(Bucket=self.bucket_name)
            print(f"Bucket '{self.bucket_name}' already exists.")
        except ClientError as e:
            error_code = int(e.response['Error']['Code'])
            if error_code == 404:
                try:
                    self.s3_client.create_bucket(
                        Bucket=self.bucket_name,
                        CreateBucketConfiguration={'LocationConstraint': self.s3_client.meta.region_name}
                    )
                    print(f"Bucket '{self.bucket_name}' created successfully.")
                except ClientError as create_err:
                    print(f"Failed to create bucket: {create_err}")
                    raise
            else:
                print(f"Error checking bucket: {e}")
                raise

    def save_telemetry(self, telemetry: Dict, table_name: str) -> bool:
        try:
            json_data = json.dumps(telemetry).encode('utf-8')
            filename = f"{table_name}.json"

            self.s3_client.put_object(
                Bucket=self.bucket_name,
                Key=filename,
                Body=json_data
            )
            print(f"Telemetry data saved to '{filename}' successfully.")
            return True

        except Exception as e:
            print(f"Error saving to S3: {str(e)}")
            return False
