def validate_coordinates(longitude:float,
                        latitude:float) -> tuple:
    """Validate and normalize coordinate inputs"""
    if isinstance(longitude, (float)) and isinstance(latitude, (float)):
        return [longitude], [latitude]
    raise ValueError("Coordinates must be floats")


def validate_bucket_and_key(bucket: str, key: str) -> tuple:
    """Validate S3 bucket and key inputs"""
    if not isinstance(bucket, str) or not isinstance(key, str):
        raise ValueError("Bucket and key must be strings")
    return bucket, key

def validate_credentials(access_key: str, secret_key: str) -> tuple:
    """Validate AWS credentials"""
    if not isinstance(access_key, str) or not isinstance(secret_key, str):
        raise ValueError("AWS credentials must be strings")
    return access_key, secret_key

def validate_european_coordinates(longitude, latitude):
    """Validate European coordinates (supports float or single-item list)."""
    
    # Unwrap from list if necessary
    if isinstance(longitude, list):
        longitude = longitude[0]
    if isinstance(latitude, list):
        latitude = latitude[0]

    if not (-25.0 <= longitude <= 50.0) or not (35.0 <= latitude <= 72.0):
        raise ValueError(f"Coordinates ({longitude}, {latitude}) are out of bounds for Europe.")
    
    return longitude, latitude