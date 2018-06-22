FROM python:3.6-slim

ARG APP_DIR_NAME=app
ARG PORT=8000

ENV PORT=${PORT}

COPY . /${APP_DIR_NAME}
RUN pip install -r /app/requirements/common.txt

WORKDIR /${APP_DIR_NAME}

EXPOSE ${PORT}

RUN chmod +x ./entrypoint.sh
RUN chmod +x ./run.sh

ENTRYPOINT ["./entrypoint.sh"]

CMD ["./run.sh"]
