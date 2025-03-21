from utils import image
import os 
import logging
from dotenv import load_dotenv

logging.basicConfig(level=logging.INFO)

if __name__ == "__main__":

    # Load environment variables
    load_dotenv()
    main_image_path=os.getenv("MAIN_FILE")
    compared_image_paths=str(os.getenv("COMPARED_FILE")).split(",")
    
    # Load main image
    main_image = image.Image(main_image_path)
    logging.info(f"Loading Main Image: {main_image_path}")

    # Load compared images
    compared_images = []
    for compared_image_path in compared_image_paths:
        logging.info(f"Loading compared image: {compared_image_path}")
        compared_image = image.Image(compared_image_path)
        compared_images.append(compared_image)
    
    # Compare images
    for compared_image in compared_images:
        logging.info(f"Comparing {compared_image_path} with {main_image_path}")
        main_image.compare(compared_image)

