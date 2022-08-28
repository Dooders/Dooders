FROM python:3.10-slim

RUN apt-get update && apt-get install -y \
    git \
    python3 \
    python3-pip

ENV NODE_VERSION=16.13.0
RUN apt install -y curl
RUN curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
ENV NVM_DIR=/root/.nvm
RUN . "$NVM_DIR/nvm.sh" && nvm install ${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm use v${NODE_VERSION}
RUN . "$NVM_DIR/nvm.sh" && nvm alias default v${NODE_VERSION}
ENV PATH="/root/.nvm/versions/node/v${NODE_VERSION}/bin/:${PATH}"
RUN node --version
RUN npm --version

ENV APP_DIR=/platform

ENV PYTHONUNBUFFERED=1

WORKDIR /opt/Dooders

COPY . /opt/Dooders/

RUN pwd

RUN pip install -r requirements.txt

RUN chmod +x ./start.sh
RUN ./start.sh

CMD ["python", "api.py"]