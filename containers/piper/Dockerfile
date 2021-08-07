FROM python:3.7.4-slim

ARG SRC="src/piper/package"
WORKDIR application

# Pre-install requirements, so that this sub-image is cached - no need to re-download it upon code-only change.
COPY ${SRC}/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Prepare package installation copying sources
COPY ${SRC}/setup.py .
COPY ${SRC}/MANIFEST.in .
COPY ${SRC}/piper piper/

# Install the package
RUN pip install -e .

# Run it
ENTRYPOINT ["python", "-m", "piper"]
