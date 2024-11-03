# FIAP ML API | Embrapa

API to return Embrapa data from the website [link](http://vitibrasil.cnpuv.embrapa.br/index.php)

## Índice

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation and run](#installation-and-run)
- [Deployment Plan](#deployment-plan)
- [Flowchart Documentation](#flowchart-documentation)
- [Contribution](#contribution)
- [License](#license)
- [Contact](#contact)

## Introduction

Project to return Embrapa data from the website [link](http://vitibrasil.cnpuv.embrapa.br/index.php)

## Features

- **Database**: Uses a `PostgreSQL` database to store extracted data, allowing for fast and efficient queries.

- **Cron Web Scraping**: A cron script that utilizes the robust `Selenium` library to browse and extract data from websites, ensuring that the collected information is accurate and up-to-date. For detailed documentation, refer to [docs/CronJobDocumentation.md](docs/CronJobDocumentation.md).

- **RESTful API**: Implements an API that exposes several endpoints, enabling users and external applications to programmatically access and query wine information.

  **Available Endpoints:**
  - `GET /embrapa/importation`: Retrieve a list of available import data.
  - `GET /embrapa/exportation`: Retrieve a list of available export data.
  - `GET /embrapa/commercialization`: Retrieve a list of available trading data.

  **Documentation Links:**
  - Read the full API documentation: [docs/APIDocumentation.md](docs/APIDocumentation.md)
  - Access the API Swagger documentation: [Swagger UI](https://efficient-freedom-production.up.railway.app/redoc)
  
## Technologies Used

- **Python**: The project's main language, chosen for its rich library for data analysis.
- **Selenium**: Library used for extracting HTML data and analyzing the structure of web pages.
- **PostgreSQL**: Database management system, ideal for storing collected data.
- **FastAPI**: FastAPI is a modern, fast (high-performance), web framework for building APIs with Python.

## Installation and run

Instructions on how to install and run the project.

Create a .env file in the project root following the example in the .env-example file

Required python version: 3.10.12

```bash
python3 -m venv .venv # Run to create the environment
source .venv/bin/activate # Run to start the environment
pip install --upgrade pip && pip install --no-cache-dir -r requirements.txt # Run to install the necessary packages
```

Run the scrape script to populate database
```bash
python3 -m cron_jobs.app.scraping
```

Run the API to load embrapa data
```bash
uvicorn api.app.main:app --host 0.0.0.0 --port 8000 --reload # Run in dev mode
```

## Deployment Plan
This is the step by step guide to deploying the API on Railway.

### Prerequisites
- Create an account on [Railway](https://railway.app/)
- Click on create a new project
- Select the option to create an "Empty project"

### Configure Database Service
<details>
  <summary><strong>View Database Configuration Steps</strong></summary>

  #### 1. Create a New Service
  - Click the "Create" button and select "Database"
  - Click on "Add PostgreSQL"
  #### 2. Get the Database Connection Variable
  - In the "Variables" tab, copy the value of "DATABASE_PUBLIC_URL"
  - Paste this "DATABASE_PUBLIC_URL" value into the ".env-example" file in the "DATABASE_URL" field
</details>

### Configure Cron service
<details>
  <summary><strong>View Deployment Cron Steps</strong></summary>

  #### 1. Create a new service
  - Click the "Create" button and select "Empty service"
  #### 2. Configure environment variables
  - In the "Variables" tab, select "Shared variables"
  - Create all the necessary environment variables following the `.env-example` file in the project
  - Go back and apply the shared variables to the service by clicking "Add all"
  #### 3. Connect GitHub project to the service
  - In the "Settings" tab, select "Source"
  - Click "Connect Repo"
  - Select the repository that contains the project
  #### 4. Configure the build
  - In the "Settings" tab, select "Config-as-code"
  - Click "Add File Path"
  - In the text field, enter `./cron_jobs/railway.json`
  - Click the checkmark to confirm
  #### 5. Deploy the application
  - In the upper left corner of the screen
  - Click "Deploy"
  - Wait for the project deployment to complete

</details>

### Configure API service
<details>
  <summary><strong>View Deployment API Steps</strong></summary>

  #### 1. Create a new service
  - Click the "Create" button and select "Empty service"
  #### 2. Configure environment variables
  - In the "Variables" tab, select "Shared variables"
  - Create all the necessary environment variables following the `.env-example` file in the project
  - Go back and apply the shared variables to the service by clicking "Add all"
  #### 3. Connect GitHub project to the service
  - In the "Settings" tab, select "Source"
  - Click "Connect Repo"
  - Select the repository that contains the project
  #### 4. Configure the build
  - In the "Settings" tab, select "Config-as-code"
  - Click "Add File Path"
  - In the text field, enter `./api/railway.json`
  - Click the checkmark to confirm
  #### 5. Deploy the application
  - In the upper left corner of the screen
  - Click "Deploy"
  - Wait for the project deployment to complete
  #### 6. Access the API
  - In the "Settings" tab, select "Networking"
  - Click "Generate Domain"
  - Copy the domain created by Railway
  - Paste the link in your browser
  - Add '/redoc' on url to read API documentation

</details>

## Flowchart Documentation
Project flowchart, covering everything from data ingestion to feeding the machine learning model. Read the full Flowchart documentation: [docs/FlowchartDocumentation.md](docs/FlowchartDocumentation.md)

## Contribution

We welcome contributions to this project! Here’s how you can help:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourFeatureName`).
3. Make your changes and commit them (`git commit -m 'feat: Add some feature'`).
4. Push to the branch (`git push origin feature/YourFeatureName`).
5. Open a Pull Request.

Please ensure that your code adheres to the project's coding standards and includes appropriate tests where necessary.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE.txt) file for details.

## Contact

For questions, suggestions, or feedback, please contact:

* **Edson Vitor**  
  GitHub: [barravitor](https://github.com/barravitor)