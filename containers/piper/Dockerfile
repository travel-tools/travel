# Args
ARG SRC="piper-dist"
ARG TAG="3.7.4-slim"

# From python image
FROM python:${TAG}

# Copy the dist
COPY ${SRC} dist

# Install the package
RUN pip install --no-cache-dir -e $(ls dist)

# Run it
ENTRYPOINT ["piper"]
