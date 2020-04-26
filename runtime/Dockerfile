FROM nvcr.io/nvidia/pytorch:19.05-py3

VOLUME "/home/aditya"

ARG http_proxy=http://adityafarizki:11377705@cache.itb.ac.id:8080
ARG https_proxy=http://adityafarizki:11377705@cache.itb.ac.id:8080

RUN apt update
RUN touch /etc/apt/sources.list.d/pgdg.list
RUN echo 'deb http://apt.postgresql.org/pub/repos/apt/ xenial-pgdg main' > /etc/apt/sources.list.d/pgdg.list
RUN wget --quiet -O - https://www.postgresql.org/media/keys/ACCC4CF8.asc | sudo apt-key add -
RUN apt update

RUN apt install libpq-dev

RUN pip install psycopg2