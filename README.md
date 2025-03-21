# AZtec Image Comparison Tool

A specialized tool for comparing pole figure images from the AZtec software, focusing on detecting and analyzing overlapping patterns between different crystallographic orientations.

## Overview

This project provides an object-oriented approach to analyze and compare spherical patterns in pole figure images. It detects blue spheres in images, extracts them, identifies green points within each sphere, and compares these points across different images to find overlaps. The tool supports region-based organization of data and multiple pole figure types (BCC, FCC, Sigma Direction, Sigma Plane).

## Features

- **Automatic Sphere Detection**: Identifies blue spheres in pole figure images
- **Green Point Extraction**: Isolates green points within each sphere using HSV color filtering
- **Overlap Analysis**: Compares spheres across different images to find matching patterns
- **Visual Output**: Generates composite images highlighting overlaps between different patterns
- **Organized Data Structure**: Uses object-oriented design with Image and Sphere classes
- **Region-Based Analysis**: Organizes data by regions for better sample management
- **Multiple Pole Figure Types**: Supports BCC, FCC, Sigma Direction, and Sigma Plane pole figures

## Project Structure

```
AZtec--image-comparison/
├── asset/                  # Source pole figure images
│   └── region1/            # Pole figures organized by region
│   └── region2/            # Each region contains BCC, FCC, and Sigma figures
│   └── region3/
├── debug_image/           # Debug visualization outputs
├── overlapped/            # Generated overlap comparison images
│   └── region1/            # Overlap results organized by region
│   └── region2/
│   └── region3/
├── scheme/                # Configuration and constants
├── unit_spheres/          # Extracted individual sphere images
│   └── pole figure BCC/    # Spheres organized by pole figure type
│   └── pole figure FCC/
│   └── pole figure sigma direction/
│   └── pole figure sigma plane/
├── utils/                 # Core functionality
│   ├── image.py           # Image class for handling whole images
│   └── sphere.py          # Sphere class for individual sphere analysis
├── .env                   # Environment variables for file paths and region settings
├── requirements.txt       # Project dependencies
├── run.py                 # Main execution script
└── README.md              # This file
```

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure the `.env` file with your region and image paths:
   ```
   REGION="region3"
   
   BCC="asset/${REGION}/${REGION}_pole figure BCC.bmp"
   FCC="asset/${REGION}/${REGION}_pole figure FCC.bmp"
   SIGMA_DIRECTION="asset/${REGION}/${REGION}_pole figure sigma direction.bmp"
   SIGMA_PLANE="asset/${REGION}/${REGION}_pole figure sigma plane.bmp"
   
   MAIN_FILE=${BCC}
   COMPARED_FILE=${FCC},${SIGMA_DIRECTION},${SIGMA_PLANE}
   ```

3. Run the analysis:
   ```
   python run.py
   ```

## How It Works

1. **Region Selection**: Set the desired region in the `.env` file
2. **Image Loading**: The tool loads the main image (typically BCC) and comparison images (FCC, Sigma Direction, Sigma Plane) specified in the `.env` file
3. **Sphere Detection**: Blue spheres are detected in each image using color thresholding and contour detection
4. **Sphere Extraction**: Individual spheres are extracted based on their centers and a specified diameter
5. **Green Point Analysis**: Green points within each sphere are identified using HSV color filtering
6. **Comparison**: Spheres from different images are compared to find overlapping green points
7. **Visualization**: Composite images are generated showing the overlaps with color coding:
   - Red: Points from the first sphere
   - Blue: Points from the second sphere
   - Green: Overlapping points
8. **Region-Based Organization**: All output files are organized by region for better data management

## Classes

### Image
Handles loading and processing of whole pole figure images, detecting blue spheres, and extracting individual spheres.

### Sphere
Represents an individual sphere extracted from an image, with methods for extracting green points and comparing with other spheres.

## Output

The tool generates several types of output:
- Debug images showing detected blue spheres
- Individual sphere images saved to the unit_spheres directory, organized by pole figure type
- Overlap comparison images showing matching patterns between different pole figures, organized by region
- Console output showing the number of green points in each sphere and overlap percentages

## Requirements

- Python 3.6+
- OpenCV (cv2)
- NumPy
- python-dotenv
