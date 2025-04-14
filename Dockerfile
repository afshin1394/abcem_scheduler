FROM python:3.12
# Set the working directory inside the container
WORKDIR /app
# Install PostgreSQL client so pg_isready is available
RUN apt-get update && apt-get install -y postgresql-client && rm -rf /var/lib/apt/lists/*

# Ensure Python finds `customers` as a package
ENV PYTHONPATH=/app
# Copy requirements and install dependencies
COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application
COPY . /app



# Expose the port
EXPOSE 8001
