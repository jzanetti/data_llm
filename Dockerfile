# Use the official Miniconda3 image from the Docker Hub
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /app

# Copy the environment.yml file into the container
COPY env.yml .

# Create the Conda environment
RUN conda env create -f env.yml

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "data_llm", "/bin/bash", "-c"]

# Copy the rest of the application code into the container
COPY . .

# Ensure the environment is activated when the container starts
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "myenv", "python", "app.py"]