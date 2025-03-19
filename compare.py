import cv2
import numpy as np
import logging




# Define grid parameters
GRID_CONFIG = {
    'origin_x': 33,      # Starting x-coordinate of the grid
    'origin_y': 60,      # Starting y-coordinate of the grid
    'sphere_width': 500, # Width of each sphere
    'sphere_height': 500,# Height of each sphere
    'x_spacing': 83,     # Horizontal spacing between spheres
    'y_spacing': 90,     # Vertical spacing between spheres
    'cols': 4,           # Number of columns in the grid
    'rows': 2            # Number of rows in the grid
}

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



lower_green = np.array([35, 0, 0])   
upper_green = np.array([85, 255, 255]) 

def extract_green_point(sphere, lower, upper):
    sphere_hsv = cv2.cvtColor(sphere, cv2.COLOR_RGB2HSV)
    green_mask = cv2.inRange(sphere_hsv, lower, upper)
    green_only = np.zeros_like(sphere)  
    green_only[green_mask > 0] = sphere[green_mask > 0]  
    return green_only, green_mask

def compare_green_points(mask1, mask2):
    """
    Compare two binary masks to find overlapping points.
    
    Args:
        mask1: First binary mask (numpy array)
        mask2: Second binary mask (numpy array)
        
    Returns:
        overlap_count: Number of overlapping points
        overlap_percentage: Percentage of overlap relative to total points
        overlap_mask: Binary mask showing only the overlapping points
    """
    # Ensure masks are binary (0 or 255)
    binary_mask1 = (mask1 > 0).astype(np.uint8) * 255
    binary_mask2 = (mask2 > 0).astype(np.uint8) * 255
    
    # Find overlapping points (logical AND)
    overlap_mask = cv2.bitwise_and(binary_mask1, binary_mask2)
    
    # Count points in each mask
    points1 = np.count_nonzero(binary_mask1)
    points2 = np.count_nonzero(binary_mask2)
    overlap_count = np.count_nonzero(overlap_mask)
    
    # Calculate overlap percentage
    total_unique_points = points1 + points2 - overlap_count
    if total_unique_points > 0:
        overlap_percentage = (overlap_count / total_unique_points) * 100
    else:
        overlap_percentage = 0
    
    return overlap_count, overlap_percentage, overlap_mask
def generate_composite_image(mask_a, mask_b, sphere_a, sphere_b, image_name, overlap_mask):
    # Create a visualization of the overlap
    
    # Create a composite image showing the overlap
    composite = np.zeros_like(sphere_a)
    
    # Convert binary masks to 3-channel for visualization
    mask_a_vis = np.zeros_like(sphere_a)
    mask_b_vis = np.zeros_like(sphere_b)
    overlap_vis = np.zeros_like(sphere_a)
    
    # Set colors for visualization (red for mask3, blue for mask5, green for overlap)
    mask_a_vis[mask_a > 0] = [255, 0, 0]  # Red for image 3 points
    mask_b_vis[mask_b > 0] = [0, 0, 255]  # Blue for image 5 points
    overlap_vis[overlap_mask > 0] = [0, 255, 0]  # Green for overlapping points
    
    # Combine the visualizations
    composite = cv2.addWeighted(mask_a_vis, 0.5, mask_b_vis, 0.5, 0)
    composite = cv2.addWeighted(composite, 0.7, overlap_vis, 1.0, 0)
    
    # Save the composite visualization
    cv2.imwrite(f"{image_name}_overlapped.png", composite)

def compare_spheres(spheres, green_masks, a, b):
    mask_a = green_masks[a]
    mask_b = green_masks[b]
    sphere_a = spheres[a]
    sphere_b = spheres[b]
    # Compare the masks
    overlap_count, overlap_percentage, overlap_mask = compare_green_points(mask_a, mask_b)
    
    # Print comparison results
    print(f"Number of green points in image {a}: {np.count_nonzero(mask_a > 0)}")
    print(f"Number of green points in image {b}: {np.count_nonzero(mask_b > 0)}")
    print(f"Number of overlapping points: {overlap_count}")
    print(f"Overlap percentage: {overlap_percentage:.2f}%")
    
    generate_composite_image(mask_a, mask_b, sphere_a, sphere_b, f"{a}_{b}", overlap_mask)

if __name__ == "__main__":
    
    # Load the BMP image
    image_path = "region2/region2_pole figure BCC.bmp"  
    image = cv2.imread(image_path)
    if image is None:
        raise FileNotFoundError(f"Could not load image at {image_path}")
    
    # Convert BGR to RGB
    image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    
    green_masks = []
    spheres = extract_spheres(image, GRID_CONFIG)
    shperes = spheres.copy()
    
    for i, item in enumerate(spheres):
        if i==7:
            continue
        
        green_only, green_mask = extract_green_point(item, lower_green, upper_green)
        green_masks.append(green_mask)
        
      
        output = item.copy()
        cv2.imwrite(f"output_{i}.png", output)
    
    
    a=6
    b=5
    compare_spheres(spheres, green_masks, a, b)
    
    
    