# Django Test Project

## Step1

- time tracker:
    
    - start time: 3:43PM
    - end time: 4:12 PM

- Tasks Covered:

    - install pipenv with python version 3.8
    - setup django with postgresql
    - dockerized the application
    - create school and student model and generate the migration
    - writing the doc
    
- How to run the project
    
    - need to install docker and docker compose
    - start the server by `docker-compose up --build`
    - to do the migration first need to exec in the docker container by `docker-compose exec app bash`
    - then need to change directory to src folder in the docker container by `cd src` and then run `python manage.py migrate`
    - the project is running on `http://localhost:8080`
    

## Step 2

- time tracker:

    - start time: 4:40 PM
    - end time: 11:04 PM
    
- Task Covered:

    - install and setup DRF and django-filters
    - api for all the CRUD and school seat availability logics
    - write test cases for the views, models, and serializers
    - add ordering and search filters
    - add a few extra model fields
    
- How to run:

    - need to install docker and docker compose
    - start the server by `docker-compose up --build`
    - to do the migration first need to exec in the docker container by `docker-compose exec app bash`
    - then need to change directory to src folder in the docker container by `cd src` and then run `python manage.py migrate`
    - the project is running on `http://localhost:8080`
    - to run the test cases you need to run from docker shell: `python manage.py test` from the `src` directory
    
## Step 3

- time tracker:

    - start time: 9:45 AM (14.11.2021)
    - end time: 11:14 AM (14.11.2021)
    
- Task Covered:

    - install and setup `drf-nested-routers`
    - api for all the CRUD and school seat availability logics with `drf-nested-routers`
    - write test cases for nested routes
    
- How to run:

    - need to install docker and docker compose
    - start the server by `docker-compose up --build`
    - to do the migration first need to exec in the docker container by `docker-compose exec app bash`
    - then need to change directory to src folder in the docker container by `cd src` and then run `python manage.py migrate`
    - the project is running on `http://localhost:8080`
    - to run the test cases you need to run from docker shell: `python manage.py test` from the `src` directory
    


