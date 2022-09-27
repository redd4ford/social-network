FROM    python:3.8
ENV     PYTHONFAULTHANDLER            1
ENV     PYTHONUNBUFFERED              1
ENV     PYTHONHASHSEED                random
ENV     PYTHONDONTWRITEBYTECODE       1
ENV     PIP_NO_CACHE_DIR              0
ENV     PIP_DISABLE_PIP_VERSION_CHECK 1
ENV     PIP_DEFAULT_TIMEOUT           100

EXPOSE  8000

WORKDIR /api
COPY    . .
RUN     pip install -r requirements.txt
