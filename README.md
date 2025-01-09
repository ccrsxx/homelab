# Homelab

## Overview

This repository contains the configuration files for my homelab. It includes Docker Compose files, scripts, and other stuff.

### Prerequisites

- Docker installed on your machine.
- Python 3.x installed on your machine.

## Running Scripts with Python

Python scripts are used to automate various tasks in my homelab. For example, `docker.py` is used to deploy and update Docker containers via Docker Compose files, and `failover.py` is used to perform failover operations when my main WAN connection goes down.

### How to Use Scripts

1. Clone the repository

   ```bash
   git clone https://github.com/ccrsxx/homelab.git
   ```

1. Navigate to the project directory

   ```bash
   cd homelab
   ```

1. Install UV package manager

   ```bash
   pip install uv
   ```

1. Sync all the project dependencies

   ```bash
   uv sync --no-dev
   ```

1. Run the python script

   ```bash
   uv run ./scripts/docker.py
   ```
