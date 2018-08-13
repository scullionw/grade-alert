FROM python:3.6
RUN mkdir deploy
COPY . /deploy
WORKDIR "/deploy"
RUN pip install -r requirements.txt
ENTRYPOINT ["python", "grade-alert.py"]