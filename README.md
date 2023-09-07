# Web Scraping and Database Integration

This repository contains Python code for web scraping real estate advertisements from cessionpme.com and integrating the scraped data into a PostgreSQL database. The code is organized into three main files: `conf.py` for configuration, `database.py` for database operations, and `main.py` for the main scraping logic.

## Table of Contents

1. [Features](#features)
2. [Prerequisites](#prerequisites)
3. [Getting Started](#getting-started)
4. [Usage](#usage)
5. [Configuration](#configuration)
6. [Database Setup](#database-setup)
7. [Logging](#logging)
8. [Contact](#contact)

## Features

- Web scraping of real estate advertisements from cessionpme.com.
- Dynamic URL generation for different departments and categories.
- Storage of scraped data in a PostgreSQL database.
- Logging to track the scraping process and any errors.
- Saving scraped data as JSON files for each department.

## Prerequisites

Before you begin, ensure you have met the following requirements:

- **Python 3.7 or higher:** You can download Python from the 
  [official Python website](https://www.python.org/downloads/).  
- **PostgreSQL database server and credentials:** [Visit the PostgreSQL download page](https://www.postgresql.org/download/).
- **Visual Studio Build Tools 2022:** These tools are required for building certain Python packages. You can download and install them from the [Microsoft Visual Studio website](https://visualstudio.microsoft.com/visual-cpp-build-tools/). A minimal installation without additional workloads is sufficient.
- **Required Python libraries** (can be installed using `pip`):
  - `beautifulsoup4`
  - `requests`
  - `psycopg2`

## Getting Started

To get started with this project, follow these steps:

1. Clone this repository to your local machine:

   ```bash
   git clone https://github.com/yourusername/your-repo-name.git

2. Change to the project directory:
	```bash
	cd your-repo-name

3. Install the required Python libraries:
	```bash
	pip install -r requirements.txt


## Usage

To use the web scraping and database integration code, follow these steps:

1. Configure your settings in the `conf.py` file, including the log file path, database connection details, and other options as needed.

2. Set up your PostgreSQL database and ensure you have the necessary privileges to create tables and insert data.

3. Run the `main.py` script to start the web scraping process:

   ```bash
   python main.py

## Configuration

You can configure the following options in the `conf.py` file:

- `log_file_path`: The path to the log file for tracking the scraping process.
- `db_host`, `db_name`, `db_user`, and `db_password`: Database connection details.

## Database setup
### How I set up my database table
1. Install `pgadmin4` [pgadmin4 official website](https://www.pgadmin.org/download/)
2. Right click on `server` to create a new one, mention the name, then localhost then the name and password according to your postgresql database server.
3. In your new server right click on it and create a new `database`
4. Open the database and go on `Schemas` then `public` and `tables`
5. On tables you right click and `PSQL tool` and you copy paste to create the adverts table:
    ```sql
    CREATE TABLE adverts (
      id SERIAL PRIMARY KEY,
      advert_title VARCHAR(255),
      advert_price VARCHAR(255),
      advert_surface VARCHAR(255),
      advert_url VARCHAR(255) UNIQUE
    );
6.  to check if it works in pgadmin4 go in the table, here adverts => `query tool` and type the following then run it (f5):
    ```sql
    SELECT * FROM adverts;


## Logging
Logging is configured to track the scraping process and any errors. Log messages are written to the specified log file path in the conf.py file.

## Contact
- [adrienbrune.pro@gmail.com](adrienbrune.pro@gmail.com)
- [GitHub](https://github.com/Ooxz)
- [Portfolio](https://adrienbrune.com/)
- [Linkedin](https://www.linkedin.com/in/adrien-brune/)