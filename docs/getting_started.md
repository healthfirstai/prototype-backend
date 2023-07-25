# Getting Started

This is an example of how you may give instructions on setting up your project locally.
To get a local development instance up and running follow these simple steps.

## Pre-requisites

- Docker
- Poetry

### Deploy with Docker

1. Ensure you have [Docker](https://www.docker.com/) installed.

   ```sh
   docker --version
   ```

2. Clone the repo

   ```sh
   git clone https://github.com/healthfirstai/prototype-backend
   cd prototype-backend
   ```

3. Create `.env` file from `example.env` and change the values

   ```sh
   cp example.env .env
   ```

4. Run docker compose up

   Building for first time

   ```sh
   docker compose up --build -d
   ```

   Fresh Rebuild

   ```sh
   docker compose build --no-cache
   docker compose up -d --build
   ```

5. Setup Python virtual environment with Poetry

   ```sh
   poetry config virtualenvs.in-project true # Make poetry use local .venv folder
   poetry install # Install dependencies
   source .venv/bin/activate # Activate virtual environment in zsh
   source .venv/bin/activate.[fish|csh] # For other shell types
   ```

### CLI Usage

1. Activate virtual environment

   ```sh
   source .venv/bin/activate # Activate virtual environment in zsh
   source .venv/bin/activate.[fish|csh] # For other shell types
   ```

2. CLI Help

   ```sh
   cli # or python3 healthfirstai_prototype/cli.py
   ```
