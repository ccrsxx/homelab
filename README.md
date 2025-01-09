# Homelab

## Overview

This repository contains the configuration files for my homelab. It includes Docker Compose files, scripts, and other stuff.

### Prerequisites

- Docker installed on your machine.
- Python 3.x with UV. You can install it [here](https://docs.astral.sh/uv/#getting-started).
- Node.js 20.x with Volta. You can install it [here](https://docs.volta.sh/guide/getting-started).

## Running Scripts with Python

Python scripts are used to automate various tasks in my homelab. For example, `docker.py` is used to deploy and update Docker containers via Docker Compose files, and `failover.py` is used to perform failover operations when my main WAN connection goes down.

### How to Use Scripts

1. Clone the repository:

   ```bash
   git clone https://github.com/ccrsxx/homelab.git
   ```

1. Navigate to the project directory:

   ```bash
   cd homelab
   ```

1. Install the dependencies:

   ```bash
   uv sync
   ```

1. Run the Python script:

   ```bash
   uv run ./scripts/docker.py
   ```

   Or you can run it via bash script:

   ```bash
   ./scripts/bin/docker.sh
   ```
