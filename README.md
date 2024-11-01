# FIAP ML API | Embrapa

API to return Embrapa data from the website [link](http://vitibrasil.cnpuv.embrapa.br/index.php)

## Índice

- [Introduction](#introduction)
- [Features](#features)
- [Technologies Used](#technologies-used)
- [Installation and run](#installation-and-run)

## Introduction

Project to return Embrapa data from the website [link](http://vitibrasil.cnpuv.embrapa.br/index.php)

## Features

- **Web Scraping**: It uses the robust `Selenium` library to navigate and extract data from the website, ensuring that the information collected is accurate and up-to-date.
  
- **Database**: The extracted data is stored in a `PostgreSQL` database, allowing for fast and efficient queries.

- **API RESTful**: Implements an API that exposes several endpoints, allowing users and external applications to access and query wine information programmatically. Some of the endpoints include:
  - `GET /embrapa/importation`: Retrieve a list of available import data.
  - `GET /embrapa/exportation`: Retrieve a list of available export data..
  - `GET /embrapa/commercialization`: Retrieve a list of available trading data..

Read API Documentation [link](https://fiap-ml-tech-challenge-stage-1-production.up.railway.app/redoc)
  
## Technologies Used

- **Python**: The project's main language, chosen for its rich library for data analysis.
- **Selenium**: Library used for extracting HTML data and analyzing the structure of web pages.
- **PostgreSQL**: Database management system, ideal for storing collected data.
- **FastAPI**: FastAPI is a modern, fast (high-performance), web framework for building APIs with Python.

## Installation and run

Instructions on how to install and run the project.

```bash
python3 -m venv .venv # Run to create the environment
source .venv/bin/activate # Run to start the environment
pip install -r requirements.txt # Run to install the necessary packages
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload # Run to run in dev mode
```