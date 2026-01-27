# Trading Dashboard – Renewable Energy Trading

This project is a data visualization dashboard for renewable energy production (wind and solar).
It allows traders to inspect aggregated production data per hour and over time.

The application is designed as a serverless system with a Python-based backend and a React frontend.

---

## Architecture Overview

The system follows a serverless architecture:

- CSV files are stored in object storage
- A Python data processing layer aggregates and validates data
- A lightweight API exposes processed results
- A React application visualizes the data in tables and charts

The architecture is designed to be scalable, maintainable, and cost-efficient.

---

## Tech Stack

### Backend
- Python 3.11
- FastAPI
- AWS Lambda
- Amazon S3
- Amazon DynamoDB

### Frontend
- React
- TypeScript
- Vite
- Recharts

---

## Features

- Average wind and solar production per hour
- Total production over time
- Time range and date filtering
- Interactive charts and tables

---

## Project Structure

backend/ # Python backend and data processing
frontend/ # React application
infrastructure/ # Architecture and deployment documentation
data/ # Sample CSV files

---

## Notes
The CSV files are included for local development and testing. In production, these files would be stored in Amazon S3 and processed by AWS Lambda.
This project is a coding challenge and is not intended for production use.
However, it is written following production-ready principles.