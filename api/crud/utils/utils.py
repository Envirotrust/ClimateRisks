def validate_coordinates(longitude:float,
                        latitude:float) -> tuple:
    """Validate and normalize coordinate inputs"""
    if isinstance(longitude, (float)) and isinstance(latitude, (float)):
        return [longitude], [latitude]
    raise ValueError("Coordinates must be floats")