# Medical Product Data Pipeline

This project is a data pipeline that scrapes medical product data from Telegram channels, loads it into a PostgreSQL database, and transforms it using dbt.

## Features

- Scrapes data from public Telegram channels.
- Loads data into a PostgreSQL database.
- Transforms raw data into a structured format using dbt.
- Containerized with Docker for easy setup and deployment.

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Prerequisites

- Docker
- Docker Compose
- Python 3.9+

### Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/AbenezerWork/Medical-Product-Data-Pipeline.git
   cd Medical-Product-Data-Pipeline
   ```

2. **Set up the environment variables:**

   Create a `.env` file by copying the example file:

   ```bash
   cp .env.example .env
   ```

   Then, fill in the required values in the `.env` file.

3. **Build and run the Docker containers:**

   ```bash
   docker-compose up -d --build
   ```

## Usage

1. **Run the scraper:**

   ```bash
   docker-compose exec app python scraper.py
   ```

2. **Load the data into PostgreSQL:**

   ```bash
   docker-compose exec app python load_to_postgres.py
   ```

3. **Run the dbt models:**

   ```bash
   docker-compose exec app dbt run --project-dir my_dbt_project
   ```

## Project Structure

```
.
├── data/                # Raw and processed data
├── dbt/                 # dbt models for data transformation
├── docker-compose.yml   # Docker Compose configuration
├── Dockerfile           # Docker configuration
├── load_to_postgres.py  # Script to load data into PostgreSQL
├── requirements.txt     # Python dependencies
└── scraper.py           # Script to scrape data from Telegram
```
