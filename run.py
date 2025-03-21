from utils import image

if __name__ == "__main__":
    
    # Count blue balls in the FCC pole figure
    image_path = "asset/region2/region2_pole figure sigma direction.bmp"
    image_a = image.Image(image_path)
    image_a.count_blue_sphere(debug=True)
    print(f"Blue balls in the image: {image_a.total_count}")
    print(f"Arranged in {image_a.rows} rows and {image_a.cols} columns")
    
