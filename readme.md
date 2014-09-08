# Snapit (new name required)

Simple mobile file upload.

## Run using Docker

Build Docker image

    docker build -t 'snapit' .

Run on Docker

    docker run -t -i -p 80:80 -v /path/for/the/pictures:/data snapit

