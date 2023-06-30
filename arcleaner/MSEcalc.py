from PIL import Image
import numpy as np
Image.MAX_IMAGE_PIXELS = 100000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000

def calculate_mse_loss(original_image_path, edited_image_path):
    # Load original image
    original_image = Image.open(original_image_path)
    original_image = original_image.resize((width, height))  # Replace width and height with desired dimensions
    original_array = np.array(original_image)

    # Load edited image
    edited_image = Image.open(edited_image_path)
    edited_image = edited_image.resize((width, height))  # Replace width and height with desired dimensions
    edited_array = np.array(edited_image)

    # Ensure both images have the same dimensions
    if original_array.shape != edited_array.shape:
        raise ValueError("Images have different dimensions.")

    # Calculate pixel-wise difference and squared error
    diff = original_array - edited_array
    squared_error = np.square(diff)

    # Compute MSE loss
    mse_loss = np.mean(squared_error)

    return mse_loss
    
# Example usage
original_path = input("Enter the original file path: ")
edited_path = input("Enter the edited file path: ")
width = 256  # Replace with desired width
height = 256  # Replace with desired height
mse_loss = calculate_mse_loss(original_path, edited_path)
print(f"MSE Loss: {mse_loss}")
