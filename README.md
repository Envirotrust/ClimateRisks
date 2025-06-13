# Climate Risks ETL Pipeline And API Endpoints
The **Climate Risks Pipeline API** is a lightweight ETL and API system for climate data processing, conversion, and access—designed with flexibility and performance in mind. It includes features for querying and visualizing flood-related datasets.

## Features
* **ETL Pipeline**: Process raw climate datasets into a structured format.
* **Data Conversion**: Read and transform data (e.g., from Parquet) using efficient tools like DuckDB.
* **RESTful API Endpoints**: Access processed flood data via HTTP.
*  **Interactive Documentation**: Swagger UI available at `/docs`.


## Project Structure

```
CLimateRisks
├── Makefile
├── README.md
├── api
│   ├── __init__.py
│   ├── crud
│   │   ├── __init__.py
│   │   ├── flood.py
│   │   └── utils
│   │       ├── __init__.py
│   │       ├── duckdb.py
│   │       └── utils.py
│   └── route
│       ├── __init__.py
│       └── flood.py
├── core
│   ├── __init__.py
│   └── config.py
├── data
│   └── flood.parquet
├── logger
│   ├── __init__.py
│   └── logging.py
├── main.py
├── requirements.txt
└── schema
    ├── __init__.py
    └── flood.py
```

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Envirotrust/ClimateRisks.git
cd climaterisks
```

### 2. Create and activate a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\activate` on Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the API

```bash
cd api/crud/
python flood.py
```

The API will start running on:

```
http://127.0.0.1:8082
```

### 5. Access the API Docs

Open this in your browser:

```
http://127.0.0.1:8082/docs
```
You can explore the available endpoints using Swagger UI.

## Development Notes
* Configurations (e.g., file paths) are stored in `core/config.py`.
* Logging is handled using custom utilities in the `logger/` module.
