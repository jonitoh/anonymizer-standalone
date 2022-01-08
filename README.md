# Anonymizer Standalone: FastAPI Server + MongoDB Database + React Frontend

FARM stack in development that aims to be production-ready, fast, easy and secure:

- backend powered by [FastAPI](https://fastapi.tiangolo.com/)
- frontend powered by [React](https://reactjs.org/)
- database powered by [MongoDB](https://www.mongodb.com/)
- platform-agnostic development powered by [Docker](https://www.docker.com/)


This repository contains a RESTful API app which can perform basic statistics on given datasets. It also renders an anonymisation process for dataset. **under construction**

This repository can also be used to create machine learning application. 

## Docker Requirements

**under construction**

## Backend Requirements

**under construction**

## Frontend Requirements

**under construction**

## Database Requirements

**under construction**

## Setup
1. Create a file named `.env` at the root based upon `.env.example` file.

2. Open a terminal, build the image:
```bash
docker-compose build
```

2. Run the container:
```bash
docker-compose up
```

## Run tests

**under construction**

## Next steps

Create a shareable environment file instead of three different ones.

Fully test the app (provide a preconfigured `tox` for the backend section).

Add some sample in the database section to fully test the application with example.

Add the scripts performance the backend tasks (basic stats, correlation and anonymisation) as a pip-able package.

Add an authentification security to the application (JWT Authentication).

Add a DOC section

