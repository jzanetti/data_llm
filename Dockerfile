# Use the official Miniconda3 image from the Docker Hub
FROM continuumio/miniconda3

# Set the working directory in the container
WORKDIR /app

# Install CMake
RUN apt-get update && \
    apt-get install -y cmake build-essential && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Copy the environment.yml file into the container
COPY env.yml .

# Create the Conda environment
RUN conda env create -f env.yml

# Make RUN commands use the new environment
SHELL ["conda", "run", "-n", "data_llm", "/bin/bash", "-c"]

# Copy the rest of the application code into the container
COPY . .

# Set lib variable
ENV LD_LIBRARY_PATH=/opt/conda/envs/data_llm/lib

# Expose IP:
EXPOSE 8050

CMD ["conda", "run", "-n", "data_llm", "python", "app.py"]
