from utils import image
from scheme.image import SPHERE_DIAMETER
if __name__ == "__main__":
    
    # Count blue balls in the FCC pole figure
    image_path = "asset/region2/region2_pole figure FCC.bmp"
    image_a = image.Image(image_path)
    image_a.count_blue_sphere(debug=True)
    image_a.extract_spheres_by_centers(SPHERE_DIAMETER)
    print(f"Blue balls in the image: {image_a.total_count}")
    print(f"Arranged in {image_a.rows} rows and {image_a.cols} columns")
    
