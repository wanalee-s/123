# Build stage
FROM python:3.10-alpine3.17 AS build

# Update the system and add git
RUN apk --no-cache add git

# Set work directory
WORKDIR /fastapi_app

# Install dependencies
COPY ./requirements.txt /fastapi_app/
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy the project
COPY . /fastapi_app

# Application image
FROM python:3.10-alpine3.17

# Copy only necessary files from the build stage
COPY --from=build /fastapi_app /fastapi_app

# Set work directory
WORKDIR /fastapi_app

# Prevent Python from writing out pyc files and buffering stdin/stdout
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Copy installed dependencies from the build stage
COPY --from=build /usr/local/lib/python3.10/site-packages /usr/local/lib/python3.10/site-packages

# Specify the entry point
ENTRYPOINT [ "./uvicorn_starter.sh" ]

# Keep the Docker process running even when crashes
CMD ["tail", "-f", "/dev/null"]
