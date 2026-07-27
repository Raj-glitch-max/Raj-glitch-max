#!/usr/bin/env python3
import sys
import os
import cv2
import numpy as np
from PIL import Image
from rembg import remove

def prep_photo(input_path="source-photo.jpg", output_path="source-prepped.png"):
    if not os.path.exists(input_path):
        print(f"Error: Input photo '{input_path}' not found.")
        sys.exit(1)
        
    print(f"Loading '{input_path}'...")
    img = Image.open(input_path)
    
    print("Removing background with rembg...")
    rembg_img = remove(img)  # RGBA PIL Image
    
    # Convert RGBA to numpy array
    rgba = np.array(rembg_img)
    rgb = rgba[:, :, :3]
    alpha = rgba[:, :, 3]
    
    # Convert RGB to grayscale
    gray = cv2.cvtColor(rgb, cv2.COLOR_RGB2GRAY)
    
    # Boost local contrast with CLAHE
    print("Boosting local contrast with OpenCV CLAHE...")
    clahe = cv2.createCLAHE(clipLimit=2.5, tileGridSize=(8, 8))
    clahe_gray = clahe.apply(gray)
    
    # Composite onto pure white background (255)
    print("Compositing onto white background...")
    alpha_norm = alpha.astype(float) / 255.0
    white_bg = np.ones_like(clahe_gray, dtype=float) * 255.0
    
    composited = (clahe_gray.astype(float) * alpha_norm) + (white_bg * (1.0 - alpha_norm))
    final_gray = np.clip(composited, 0, 255).astype(np.uint8)
    
    print(f"Saving prepped image to '{output_path}'...")
    Image.fromarray(final_gray).save(output_path)
    print("Photo prep complete!")

if __name__ == "__main__":
    path = sys.argv[1] if len(sys.argv) > 1 else "source-photo.jpg"
    prep_photo(path)
