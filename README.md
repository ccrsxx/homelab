# Homelab

## Overview

This repository contains the configuration files for my homelab. There's some docker compose files, some scripts, and some other stuff.

### Prerequisites

- Docker installed on your machine.
- Python 3.x installed on your machine.

## Running Scripts with Python

Python scripts are used to automate various tasks on my homelab. For example. there's `docker.py` which is to deploy and update docker containers via docker compose files and `failover.py` which is to perform failover operations when my main WAN connection goes down.

### How to Use Scripts

1. Clone the repository

   ```bash
   git clone https://github.com/ccrsxx/homelab.git
   ```

1. Navigate to the project directory

   ```bash
   cd homelab
   ```

1. Create a virtual environment for python

   ```bash
   python -m venv venv
   ```

1. Activate the virtual environment

   ```bash
   source venv/bin/activate
   ```

1. Install the required Python packages

   ```bash
   pip install -r requirements.txt
   ```

1. Deactivate the virtual environment

   ```bash
   deactivate
   ```

1. Run the script via bash script

   ```bash
   ./scripts/bin/docker.sh
   ```
