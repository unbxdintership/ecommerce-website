# Project: ecommerce-website
A simple e-commerce website for a small business which sells apparels. User can search for products, browse through the available products and also view the details of any product. 

#### Tools used for the project:
  - Frontend: HTML, CSS, JavaScript
  - Backend: Python-Flask
  - Database Component: PostgreSQL
  - Cache Component: Redis

# Overview of API specs
The backend exposes API routes for seven functionalities:
  1. Header
  2. Home
  3. Products
  4. Product-Details
  5. Category
  6. Search
  7. Ingestion

The details regarding the APIs can be found in this [document](https://docs.google.com/document/d/1oUA8EzTVEeVuQZPuW5lUjyoHHjosA5ALpCVDKJ1Allk/edit?usp=sharing)

# Installation Instructions
## To run the application locally:
  1. Change the host in the db_object.py and cache_object.py files to ```localhost```.
  2. The frontend is hosted in the nginx docker container. To run the frontend:
  
     ```
     cd frontend
     docker build . -t frontend_docker
     docker run -it --rm -p 8080:80 frontend_docker
     ```
  3. The frontend is now running on the port 8080.
  4. To run the backend:
     
     ```
     cd ../backend
     python3 backend.py
     ```
  5. The backend is now running on the port 3000.

## To run the application using docker containers:
  1. To run the frontend:
     ```
     cd frontend
     docker build . -t frontend_docker
     ```
  2. To run the backend:
     ```
     cd ../backend
     docker build . -t backend_docker
     ```
  3. In the docker compose file, change the image names of the frontend and backend services to ```frontend_docker``` and ```backend_docker``` respectively.
  4. In the root directory, run the following command:
     ```
     docker-compose up
     ```
  5. Now the frontend is running on port 5000 while the backend is running on port 3000.
