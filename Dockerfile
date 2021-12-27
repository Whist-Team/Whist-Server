FROM python:3.9

COPY ./requirements/requirements.txt requirements.txt

RUN pip install --no-cache-dir -r requirements.txt

WORKDIR .
COPY ./whist /whist

ENV PYTHONPATH "${PYTHONPATH}:/whist/"
CMD ["python", "whist/server", "0.0.0.0", "8080"]
