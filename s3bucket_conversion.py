import boto3

def get_standard_buckets():
    # Create an S3 client
    s3_client = boto3.client('s3')

    # List all S3 buckets
    response = s3_client.list_buckets()

    standard_buckets = []

    # Check the storage class of each bucket
    for bucket in response['Buckets']:
        bucket_name = bucket['Name']

        # List objects in the bucket
        objects_response = s3_client.list_objects_v2(Bucket=bucket_name)

        # Check the storage class of each object
        if 'Contents' in objects_response:
            for obj in objects_response['Contents']:
                storage_class = obj['StorageClass']

                # Check if the storage class is "STANDARD"
                if storage_class == 'STANDARD':
                    standard_buckets.append(bucket_name)
                    break

    return standard_buckets

def convert_to_intelligent_tiering(bucket_name):
    # Create an S3 client
    s3_client = boto3.client('s3')

    # Configure the Intelligent-Tiering storage class
    intelligent_tiering_config = {
        'StorageClass': 'INTELLIGENT_TIERING'
    }

    # Update the bucket's lifecycle configuration
    response = s3_client.put_bucket_lifecycle_configuration(
        Bucket=bucket_name,
        LifecycleConfiguration={
            'Rules': [
                {
                    'Status': 'Enabled',
                    'Filter': {},
                    'Transitions': [
                        {
                            'Days': 0,
                            'StorageClass': intelligent_tiering_config['StorageClass']
                        }
                    ]
                }
            ]
        }
    )

    if response['ResponseMetadata']['HTTPStatusCode'] == 200:
        print(f"Bucket '{bucket_name}' converted to Intelligent-Tiering.")
    else:
        print(f"Error converting bucket '{bucket_name}' to Intelligent-Tiering.")

# Get the standard buckets
standard_buckets = get_standard_buckets()

# Convert each standard bucket to Intelligent-Tiering
for bucket_name in standard_buckets:
    convert_to_intelligent_tiering(bucket_name)

