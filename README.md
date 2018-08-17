# grade-alert


## Credentials and messenger key set-up

1) Get Nimrod messenger API key -> https://m.me/251459615313202

2) Modify config.py.example to contain UdeS user and password and the api key. Rename to config.py

## With Docker

1) Navigate inside repo and build image:

        $ cd grade-alert/
        $ docker build -t grade_alert_image .


2) Set-up cronjob to run script every 30 minutes:

        $ crontab -e

3) Add this line to the cronjobs, **where** *REPO* **is the full path to cd into the grade-alert directory**:

        */30 * * * * cd REPO && docker run -v "$(pwd)":/deploy/ grade_alert_image

## Without Docker

1) Install python 3

2) Navigate inside repo:

        $ cd grade-alert/

3) Download dependencies:

        $ pip install -r requirements.txt

4) Open cronjob editor:

        $ crontab -e

5) Add this line to the cronjobs, **where** *REPO* **is the full path to cd into the grade-alert directory**:

        */30 * * * * cd REPO && python3 grade-alert.py



