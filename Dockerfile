# Use Google Cloud SDK's container as the base image
FROM google/cloud-sdk

# Specify your e-mail address as the maintainer of the container image
LABEL maintainer="georgeolson92@gmail.com"

# Install Python 3 and virtualenv
RUN apt update -y && apt install -y python3 python3-pip python3-venv

# Set the working directory of the container to /app
WORKDIR /app

# Copy the contents of the current directory into the container directory /app
COPY . /app

# Create a virtual environment and install dependencies
RUN python3 -m venv /app/env && \
    . /app/env/bin/activate && \
    pip install -r requirements.txt

# Set environment variables to ensure the virtual environment is used
ENV PATH="/app/env/bin:$PATH"

# Set the parameters to the program
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 app:app
