import csv
import numpy as np
import matplotlib.pyplot as plt
import os
from tqdm import tqdm
from skimage.measure import moments_central, moments_normalized, moments
from PIL import Image

def normalize_iats(iats):
    """Normalize IATs to 0-255 range"""
    iats = np.array(iats)
    # Avoid division by zero
    if np.max(iats) - np.min(iats) == 0:
        return np.zeros_like(iats)
    return 255 * (iats - np.min(iats)) / (np.max(iats) - np.min(iats))

def create_colored_image(iats, img_size=16, output_dir=None, idx=None):
    """
    Create colored image from IATs and optionally save it
    Returns: image matrix and saves PNG if output_dir specified
    """
    # Normalize and reshape
    norm_iats = normalize_iats(iats)
    img_matrix = norm_iats.reshape((img_size, img_size))
    
    # Create colored image using matplotlib colormap
    plt.figure(figsize=(2, 2))
    plt.imshow(img_matrix, cmap='viridis')  # Using viridis colormap
    plt.axis('off')
    
    # Save if output directory specified
    if output_dir and idx is not None:
        os.makedirs(output_dir, exist_ok=True)
        output_path = os.path.join(output_dir, f'iat_image_{idx}.png')
        plt.savefig(output_path, bbox_inches='tight', pad_inches=0)
        plt.close()
    
    return img_matrix

def extract_features(image_matrix):
    """Extract the 8 features from an image matrix"""
    features = []
    
    # Convert to grayscale if needed (though our matrix should already be 2D)
    if len(image_matrix.shape) == 3:
        gray_image = np.mean(image_matrix, axis=2)
    else:
        gray_image = image_matrix
    
    # 1. Mean gray value
    features.append(np.mean(gray_image))
    
    # 2. Standard deviation
    features.append(np.std(gray_image))
    
    # 3. Mode (most frequent value)
    hist, bin_edges = np.histogram(gray_image.flatten(), bins=256)
    features.append(bin_edges[np.argmax(hist)])
    
    # 4. Center of mass (spatial moments)
    # Calculate raw moments
    m = moments(gray_image, order=1)
    # Center coordinates (x, y)
    cy, cx = m[0, 1] / m[0, 0], m[1, 0] / m[0, 0]  # Note: moments returns (y,x)
    features.extend([cx, cy])
    
    # 5. Integrated density (sum of pixel values)
    features.append(np.sum(gray_image))
    
    # 6. Median
    features.append(np.median(gray_image))
    
    # 7. Skewness (3rd standardized moment)
    mean = np.mean(gray_image)
    std = np.std(gray_image)
    if std > 0:
        skewness = np.mean((gray_image - mean)**3) / (std**3)
    else:
        skewness = 0
    features.append(skewness)
    
    # 8. Kurtosis (4th standardized moment)
    if std > 0:
        kurtosis = np.mean((gray_image - mean)**4) / (std**4)
    else:
        kurtosis = 0
    features.append(kurtosis)
    
    return features

def main():
    input_csv = r'C:\Users\okore\OneDrive\Desktop\Inno_Courses\PROJECTS\OT\ML\Output\iat_data.csv'
    output_csv = r'C:\Users\okore\OneDrive\Desktop\Inno_Courses\PROJECTS\OT\ML\Output\image_features.csv'
    image_output_dir = r'C:\Users\okore\OneDrive\Desktop\Inno_Courses\PROJECTS\OT\ML\Output'  # Directory to save visualizations
    
    # Read IAT data and create images
    with open(input_csv, 'r') as infile, open(output_csv, 'w', newline='') as outfile:
        reader = csv.reader(infile)
        writer = csv.writer(outfile)
        
        # Read header and write new header
        header = next(reader)
        feature_header = [
            'label', 'mean_gray', 'std_dev', 'mode', 
            'center_x', 'center_y', 'integrated_density', 
            'median', 'skewness', 'kurtosis'
        ]
        writer.writerow(feature_header)
        
        # Process each row
        for idx, row in enumerate(tqdm(reader, desc="Creating images")):
            label = int(row[0])
            iats = list(map(float, row[1:]))
            
            # Create colored image
            img_matrix = create_colored_image(
                iats, 
                output_dir=image_output_dir, 
                idx=idx
            )
            
            # Extract features from the image matrix
            features = extract_features(img_matrix)
            
            # Write to output CSV
            writer.writerow([label] + features)

if __name__ == "__main__":
    main()