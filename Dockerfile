FROM python:3-alpine
MAINTAINER Graham Moore "graham.moore@sesam.io"
RUN apk update
RUN apk add --no-cache g++ gcc libxslt-dev
COPY ./service /service
WORKDIR /service
RUN pip install -r requirements.txt
EXPOSE 5000/tcp
ENTRYPOINT ["python"]
CMD ["termstore-service.py"]