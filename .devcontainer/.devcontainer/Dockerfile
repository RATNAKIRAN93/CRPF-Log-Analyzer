FROM mcr.microsoft.com/devcontainers/base:ubuntu-22.04

# Install basics
RUN apt-get update \
  && DEBIAN_FRONTEND=noninteractive apt-get install -y --no-install-recommends \
     curl wget gnupg apt-transport-https ca-certificates openjdk-17-jre-headless python3 python3-pip docker.io docker-compose-plugin \
  && apt-get clean && rm -rf /var/lib/apt/lists/*

# Node.js (recommended LTS 18)
RUN curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
  && apt-get install -y nodejs \
  && npm install -g npm@latest
