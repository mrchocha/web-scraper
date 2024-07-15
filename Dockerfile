# 
FROM python:3.12

# 
WORKDIR /code

# 
COPY ./requirements.txt /code/requirements.txt

COPY Makefile /code/Makefile

# 
RUN make install

# 
COPY ./app /code/app


COPY .env /code/.env

RUN echo pwd

# 
CMD ["make", "run"]