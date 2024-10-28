# Use a base image that includes Python and the Google Cloud SDK
FROM google/cloud-sdk:slim

# Specify your e-mail address as the maintainer of the container image
LABEL maintainer="georgeolson92@gmail.com"

# Set the working directory of the container to /app
WORKDIR /app

# Copy only requirements.txt first to leverage Docker's caching
COPY requirements.txt ./

# Install the Python packages specified by requirements.txt into the container
RUN apt update -y && apt install -y python3-pip && pip3 install -r requirements.txt

# Copy the rest of the application files
COPY . .

# Set the parameters to the program
CMD ["gunicorn", "--bind", ":$PORT", "--workers", "1", "--threads", "8", "app:app"]
