text
# Bim Viewer

## Overview

This project is an Bim Viewer application built using PyQt5 and OpenGL and IfcOpenShell. It allows users to load and visualize IFC files using a python code.

## Features

- Load and visualize IFC files.
- Interactive 3D navigation.

## Setup Instructions

### Prerequisites

- Python 3.11
- Git

### Installation

1. **Clone the Repository:**

   ```bash
   git clone (https://github.com/Atharvack/Bim-Viewer.git)
   

Create and Activate a Virtual Environment:

   ```bash
      python -m venv ifc_viewer_env
      source ifc_viewer_env/bin/activate  # On Windows use `ifc_viewer_env\Scripts\activate`
   ```
Install Dependencies:
bash
pip install -r requirements.txt

[Install IfcOpenShell](https://docs.ifcopenshell.org/ifcopenshell-python/installation.html)

Run the Application:
bash
python main.py

Usage
Open an IFC file using the "File" menu.
Click on walls to view their properties.
Use mouse controls to rotate, pan, and zoom the model.
Results

Here are some results from the application:

![duplex_2](https://github.com/user-attachments/assets/9d1221ca-3e50-4d08-8712-76adcab1f09f)

![Duplex_1](https://github.com/user-attachments/assets/3f0fb8bc-6ffe-4488-aa57-fdc9eeacf8a8)

