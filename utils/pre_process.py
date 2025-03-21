import cv2
import numpy as np
from scheme.hue import LOWER_BLUE, UPPER_BLUE


def count_blue_sphere(image_path, debug=False):
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
    # Load the image
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not load image at {image_path}")
    
    # Convert to HSV for better color detection
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    
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
        debug_img = cv2.imread(image_path)
        # Draw contours
        cv2.drawContours(debug_img, valid_contours, -1, (0, 255, 0), 2)
        # Draw centers
        for center in centers:
            cv2.circle(debug_img, center, 5, (0, 0, 255), -1)
        # Save debug image
        cv2.imwrite("debug_image/blue_balls_debug.png", debug_img)
    
    return rows, cols, total_count



# Extract spheres using vectorized operations where possible
def extract_spheres(image, config):
    """Extract spheres from image based on grid configuration.
    
    Args:
        image: RGB image containing the spheres
        config: Dictionary with grid parameters
        
    Returns:
        List of extracted sphere images
    """
    spheres = []
    
    for col in range(config['cols']):
        for row in range(config['rows']):
            # Calculate coordinates for current sphere
            x_start = config['origin_x'] + col * (config['sphere_width'] + config['x_spacing'])
            y_start = config['origin_y'] + row * (config['sphere_height'] + config['y_spacing'])
            x_end = x_start + config['sphere_width']
            y_end = y_start + config['sphere_height']
            
            # Extract the sphere
            sphere = image[y_start:y_end, x_start:x_end]
            spheres.append(sphere)
    
    return spheres

def extract_green_point(sphere, lower, upper):
    sphere_hsv = cv2.cvtColor(sphere, cv2.COLOR_RGB2HSV)
    green_mask = cv2.inRange(sphere_hsv, lower, upper)
    green_only = np.zeros_like(sphere)  
    green_only[green_mask > 0] = sphere[green_mask > 0]  
    return green_only, green_mask