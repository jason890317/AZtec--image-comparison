import cv2
import numpy as np
from scheme.hue import LOWER_BLUE, UPPER_BLUE
from scheme.image import DEBUG_PATH, SPHERE_DIAMETER
from service.sphere import Sphere
import logging
import os


class Image:

    def __init__(self, image_path):
        # Direct assignment for efficiency
        self.image_path = image_path
        self.image = cv2.imread(image_path)
        if self.image is None:
            raise FileNotFoundError(f"Could not load image at {image_path}")
        
        # Pre-compute HSV version for faster color operations
        self.hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
        self.rows = 0
        self.cols = 0
        self.total_count = 0
        self.centers = []
        self.spheres = []
        self.count_blue_sphere()
        self.extract_spheres_by_centers(SPHERE_DIAMETER)

    def count_blue_sphere(self, debug=True):
        """
        Count the number of blue balls in the image and determine rows and columns.
        
        Args:
            image_path: Path to the image file
            debug: If True, save debug images
            
        Returns:
            rows: Number of rows of blue balls
            cols: Number of columns of blue balls
            total_count: Total number of blue balls detected
        """
        # Use pre-computed HSV image for better efficiency
        hsv = self.hsv
        
        # Create mask for blue color
        blue_mask = cv2.inRange(hsv, LOWER_BLUE, UPPER_BLUE)
        
        # Apply morphological operations to clean up the mask
        kernel = np.ones((5, 5), np.uint8)
        blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_OPEN, kernel)
        blue_mask = cv2.morphologyEx(blue_mask, cv2.MORPH_CLOSE, kernel)
        
        # Find contours of blue balls
        contours, _ = cv2.findContours(blue_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by size to eliminate noise
        min_area = 5000  # Adjust based on the size of the blue balls
        valid_contours = [cnt for cnt in contours if cv2.contourArea(cnt) > min_area]
        
        # Get centers of all blue balls
        centers = []
        for cnt in valid_contours:
            M = cv2.moments(cnt)
            if M["m00"] != 0:
                cx = int(M["m10"] / M["m00"])
                cy = int(M["m01"] / M["m00"])
                centers.append((cx, cy))
        
        # If no centers found, return 0 for all values
        if not centers:
            return 0, 0, 0
        
        # Sort centers by y-coordinate (row)
        # Define custom sorting function that considers both x and y coordinates within 10 of each other as the same
        def custom_sort_key(item):
            # Round both coordinates to nearest 10 to group similar values
            group_x = item[0] // 10 * 10
            group_y = item[1] // 10 * 10
            return (group_x, group_y)
            
        # Apply custom sorting directly
        sorted_centers = sorted(centers.copy(), key=custom_sort_key)

        centers.sort(key=lambda p: p[1])
        
        # Determine rows by clustering y-coordinates
        y_coords = [p[1] for p in centers]
        y_clusters = []
        current_cluster = [y_coords[0]]
        
        # Threshold for considering points to be in the same row
        row_threshold = 30  # Adjust based on spacing
        
        for y in y_coords[1:]:
            if abs(y - current_cluster[-1]) < row_threshold:
                current_cluster.append(y)
            else:
                y_clusters.append(current_cluster)
                current_cluster = [y]
        
        if current_cluster:
            y_clusters.append(current_cluster)
        
        rows = len(y_clusters)
        
        # For each row, determine the number of columns
        cols_per_row = []
        for i, cluster in enumerate(y_clusters):
            # Get points in this row
            row_points = [p for p in centers if p[1] in cluster]
            # Sort by x-coordinate
            row_points.sort(key=lambda p: p[0])
            cols_per_row.append(len(row_points))
        
        # The number of columns is the maximum number of points in any row
        cols = max(cols_per_row) if cols_per_row else 0
        
        # Total count of blue balls
        total_count = len(centers)
        
        # Create debug visualization if requested
        if debug:
            debug_img = self.image.copy()  # More efficient than re-reading from disk
            # Draw contours
            cv2.drawContours(debug_img, valid_contours, -1, (0, 255, 0), 2)
            # Draw centers
            for center in centers:
                cv2.circle(debug_img, center, 5, (0, 0, 255), -1)
            # Save debug image
            cv2.imwrite(DEBUG_PATH, debug_img)
        
        self.rows = rows
        self.cols = cols
        self.total_count = total_count
        self.centers = sorted_centers


    # Extract spheres using vectorized operations where possible
    def extract_spheres_by_centers(self, diameter):
        """Extract spheres from image based on center coordinates and diameter.
        
        Args:
            centers: List of (x, y) tuples representing sphere centers
            diameter: Diameter of the spheres in pixels (can be an int or a list of ints)
            
        Returns:
            List of Sphere objects
        """
        spheres = []
        
        # Handle both single diameter and list of diameters
        if isinstance(diameter, int):
            diameters = [diameter] * len(self.centers)
        else:
            diameters = diameter
            
        for i, (cx, cy) in enumerate(self.centers):
            # Calculate the bounding box
            radius = diameters[i] // 2
            x_start = max(0, cx - radius)
            y_start = max(0, cy - radius)
            x_end = min(self.image.shape[1], cx + radius)
            y_end = min(self.image.shape[0], cy + radius)
            
            # Extract the sphere
            sphere_image = self.image[y_start:y_end, x_start:x_end]
            
            # Create Sphere object
            sphere_name = f"{os.path.basename(self.image_path).split(' ')[-1][:-4]}_{i}.png"
            sphere_obj = Sphere(sphere_image, sphere_name, (cx, cy), diameters[i])
            spheres.append(sphere_obj)
            
            # Create directory for saving sphere images if it doesn't exist
            save_dir = os.path.join("unit_spheres", os.path.basename(self.image_path)[:-4])
            os.makedirs(save_dir, exist_ok=True)
            
            # Save sphere image
            save_path = os.path.join(save_dir, sphere_obj.name)
            cv2.imwrite(save_path, sphere_image)
        self.spheres = spheres
        return spheres
    
    def compare(self, other_image):
        for sphere in self.spheres:
            for other_sphere in other_image.spheres:
                sphere.compare_spheres(other_sphere)
