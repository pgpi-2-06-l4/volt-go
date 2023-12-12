FROM python:3.10-alpine

RUN apk add --no-cache git postgresql-dev gcc libc-dev
RUN apk add --no-cache gcc g++ make libffi-dev python3-dev build-base

RUN pip install gunicorn
RUN pip install psycopg2
RUN pip install ipdb
RUN pip install ipython

WORKDIR /app

RUN git clone --branch feat/docker https://github.com/pgpi-2-06-l4/volt-go.git .
RUN pip install -r requirements.txt

WORKDIR /app/voltgo

ARG STRIPE_PUBLIC_KEY=pk_test_51OHWDGGXSBM20rPRZ6SWDsMZgnA5KXRfuSvG5V7yoCWL90qFiLalG3ggssj6rvynDmx6JB49CG3F1kLQmGeZFxkD00zga40NBD
ARG STRIPE_SECRET_KEY=sk_test_51OHWDGGXSBM20rPRxhKaoXCzDbXklKvuYZJqrIsQkpg1bq9Voc94E4OReS33BriBiyIAEDE8nCg5E2yvuMATNc5V000rY2IUn4
ENV STRIPE_PUBLIC_KEY=$STRIPE_PUBLIC_KEY
ENV STRIPE_SECRET_KEY=$STRIPE_SECRET_KEY

RUN python manage.py migrate