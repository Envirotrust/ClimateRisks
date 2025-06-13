import duckdb

def setup_spatial_extensions():
    """Install and load spatial extension with performance settings"""
    try:
        duckdb.sql("INSTALL spatial;")
        duckdb.sql("LOAD spatial;")
        
        # Performance optimizations
        duckdb.sql("SET threads=2;")  # Use multiple threads
        duckdb.sql("SET memory_limit='2GB';")  # Increase memory limit
        duckdb.sql("SET max_memory='2GB';")
        
        print("Spatial extension loaded with performance settings")
    except Exception as e:
        print(f"Note: Spatial extension setup: {e}")