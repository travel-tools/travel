ARG TAG="3.7.4"

# From python image
FROM python:${TAG}

# Copy the dist
ARG DIST="src/garden/package/dist"
COPY ${DIST} dist/

# Install the package
RUN pip install --no-cache-dir dist/$(ls dist)

