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

#### NB: there are three branches in the project. `setp-1`, `step-2` and `step-3`. The complete task is in the `step-3` branch. Also this branch is deployed in heroku.
