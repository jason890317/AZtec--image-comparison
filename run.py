from utils import compare
from utils import pre_process

if __name__ == "__main__":
    
    # Count blue balls in the FCC pole figure
    image_path = "asset/region2/region2_pole figure sigma direction.bmp"
    rows, cols, total = pre_process.count_blue_sphere(image_path, debug=True)
    print(f"Blue balls in the image: {total}")
    print(f"Arranged in {rows} rows and {cols} columns")
    
