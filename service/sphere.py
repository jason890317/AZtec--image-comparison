import cv2
import numpy as np
import logging
from scheme.hue import LOWER_GREEN, UPPER_GREEN
import os

class Sphere:

    def __init__(self, image, name,center, diameter):
        self.image = image
        self.name = name
        self.green_mask = None
        self.green_only = None
        self.center = center
        self.diameter = diameter
        self._extract_green_point()

    def _extract_green_point(self):
        sphere_hsv = cv2.cvtColor(self.image, cv2.COLOR_RGB2HSV)
        green_mask = cv2.inRange(sphere_hsv, LOWER_GREEN, UPPER_GREEN)
        green_only = np.zeros_like(self.image)  
        green_only[green_mask > 0] = self.image[green_mask > 0] 
        self.green_mask = green_mask
        self.green_only = green_only
 

    def _compare_green_points(self, other_sphere):
        """
        Compare two binary masks to find overlapping points.
    
        Args:
            other_sphere: Second sphere
          
            
        Returns:
            overlap_count: Number of overlapping points
            overlap_percentage: Percentage of overlap relative to total points
            overlap_mask: Binary mask showing only the overlapping points
        """
        # Ensure masks are binary (0 or 255)
        binary_mask1 = (self.green_mask > 0).astype(np.uint8) * 255
        binary_mask2 = (other_sphere.green_mask > 0).astype(np.uint8) * 255
        
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

    def _generate_composite_image(self,other_sphere,overlap_mask):
        # Create a visualization of the overlap
        
        # Create a composite image showing the overlap
        composite = np.zeros_like(self.image)
        
        # Convert binary masks to 3-channel for visualization
        mask_a_vis = np.zeros_like(self.image)
        mask_b_vis = np.zeros_like(other_sphere.image)
        overlap_vis = np.zeros_like(self.image)
        
        # Set colors for visualization (red for mask3, blue for mask5, green for overlap)
        mask_a_vis[self.green_mask > 0] = [255, 0, 0]  # Red for image 3 points
        mask_b_vis[other_sphere.green_mask > 0] = [0, 0, 255]  # Blue for image 5 points
        overlap_vis[overlap_mask > 0] = [0, 255, 0]  # Green for overlapping points
        
        # Combine the visualizations
        composite = cv2.addWeighted(mask_a_vis, 0.5, mask_b_vis, 0.5, 0)
        composite = cv2.addWeighted(composite, 0.7, overlap_vis, 1.0, 0)
        
        # Save the composite visualization
        region=os.getenv("REGION")
        saved_dir = os.path.join("overlapped",region)
        os.makedirs(saved_dir, exist_ok=True)
        cv2.imwrite(f"{saved_dir}/{self.name[:-4]}_{other_sphere.name[:-4]}_overlapped.png", composite)

    def compare_spheres(self, other_sphere):
        # Compare the masks
        overlap_count, overlap_percentage, overlap_mask = self._compare_green_points(other_sphere)
        
        # Print comparison results
        print(f"Green Points in {self.name}: {np.count_nonzero(self.green_mask > 0)}")
        print(f"Green Points in {other_sphere.name}: {np.count_nonzero(other_sphere.green_mask > 0)}")
        print(f"Number of overlapping points: {overlap_count}")
        print(f"Overlap percentage: {overlap_percentage:.2f}%")
        if overlap_percentage > 0:
            self._generate_composite_image(other_sphere, overlap_mask)