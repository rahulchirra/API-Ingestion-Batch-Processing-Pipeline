# End-to-End Automated Crypto ETL Pipeline

## Overview
This project is a fully automated Data Engineering pipeline that extracts real-time cryptocurrency data from the Binance API, transforms it, and loads it into a PostgreSQL data warehouse. The entire workflow is containerized using Docker and orchestrated to run daily using Apache Airflow.

## Tech Stack
* **Data Source:** Binance Public API
* **Language:** Python (requests, pandas)
* **Destination:** PostgreSQL
* **Infrastructure:** Docker & Docker Compose
* **Orchestration:** Apache Airflow


## How to Run Locally
1. Clone the repository.
2. Start the database:
   `docker-compose up -d`
3. Install dependencies:
   `pip install -r requirements.txt`
4. Start Airflow:
   `airflow standalone`
5. Access the Airflow UI at `localhost:8080` and trigger the `crypto_daily_etl_pipeline` DAG.