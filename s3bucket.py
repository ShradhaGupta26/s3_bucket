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

# Call the function to get the standard buckets
standard_buckets = get_standard_buckets()

# Print the bucket names
for bucket_name in standard_buckets:
    print(bucket_name)

