# AZtec Image Comparison Tool

A specialized tool for comparing pole figure images from the AZtec software, focusing on detecting and analyzing overlapping patterns between different crystallographic orientations.

## Overview

This project provides an object-oriented approach to analyze and compare spherical patterns in pole figure images. It detects blue spheres in images, extracts them, identifies green points within each sphere, and compares these points across different images to find overlaps.

## Features

- **Automatic Sphere Detection**: Identifies blue spheres in pole figure images
- **Green Point Extraction**: Isolates green points within each sphere using HSV color filtering
- **Overlap Analysis**: Compares spheres across different images to find matching patterns
- **Visual Output**: Generates composite images highlighting overlaps between different patterns
- **Organized Data Structure**: Uses object-oriented design with Image and Sphere classes

## Project Structure

```
AZtec--image-comparison/
├── asset/                  # Source pole figure images
├── debug_image/           # Debug visualization outputs
├── overlapped/            # Generated overlap comparison images
├── scheme/                # Configuration and constants
├── unit_spheres/          # Extracted individual sphere images
├── utils/                 # Core functionality
│   ├── image.py           # Image class for handling whole images
│   └── sphere.py          # Sphere class for individual sphere analysis
├── .env                   # Environment variables for file paths
├── requirements.txt       # Project dependencies
├── run.py                 # Main execution script
└── README.md              # This file
```

## Setup

1. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

2. Configure the `.env` file with paths to your images:
   ```
   MAIN_FILE="path/to/main/image.bmp"
   COMPARED_FILE="path/to/compare1.bmp,path/to/compare2.bmp"
   ```

3. Run the analysis:
   ```
   python run.py
   ```

## How It Works

1. **Image Loading**: The tool loads the main image and comparison images specified in the `.env` file
2. **Sphere Detection**: Blue spheres are detected in each image using color thresholding and contour detection
3. **Sphere Extraction**: Individual spheres are extracted based on their centers and a specified diameter
4. **Green Point Analysis**: Green points within each sphere are identified using HSV color filtering
5. **Comparison**: Spheres from different images are compared to find overlapping green points
6. **Visualization**: Composite images are generated showing the overlaps with color coding:
   - Red: Points from the first sphere
   - Blue: Points from the second sphere
   - Green: Overlapping points

## Classes

### Image
Handles loading and processing of whole pole figure images, detecting blue spheres, and extracting individual spheres.

### Sphere
Represents an individual sphere extracted from an image, with methods for extracting green points and comparing with other spheres.

## Output

The tool generates several types of output:
- Debug images showing detected blue spheres
- Individual sphere images saved to the unit_spheres directory
- Overlap comparison images showing matching patterns between different pole figures

## Requirements

- Python 3.6+
- OpenCV (cv2)
- NumPy
- python-dotenv
