import os
from PIL import Image
import face_recognition
from tkinter import Tk, filedialog

def center_and_crop_image(input_path, output_path, target_dimensions):
    image = face_recognition.load_image_file(input_path)
    face_locations = face_recognition.face_locations(image)

    if not face_locations:
        print(f"No face detected in {input_path}")
        return

    top, right, bottom, left = face_locations[0]

    # Calculate the center coordinates of the face
    center_x = (left + right) // 2
    center_y = (top + bottom) // 2

    # Calculate the cropping box coordinates
    crop_left = max(center_x - target_dimensions[0] // 2, 0)
    crop_top = max(center_y - target_dimensions[1] // 2, 0)
    crop_right = min(crop_left + target_dimensions[0], image.shape[1])
    crop_bottom = min(crop_top + target_dimensions[1], image.shape[0])

    # Crop the image
    cropped_image = image[crop_top:crop_bottom, crop_left:crop_right]

    # Resize the cropped image to 512x512 pixels
    resized_image = Image.fromarray(cropped_image).resize((512, 512), Image.LANCZOS)

    # Save the resized image
    output_image_path = os.path.join(output_path, os.path.basename(input_path))
    resized_image.save(output_image_path)
    print(f"Saved cropped and resized image to {output_image_path}")

def process_images(input_folder, output_folder, target_dimensions):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(input_folder):
        if filename.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
            input_path = os.path.join(input_folder, filename)
            center_and_crop_image(input_path, output_folder, target_dimensions)

def select_folder():
    root = Tk()
    root.withdraw()
    folder_selected = filedialog.askdirectory(title="Select Input Folder")
    root.destroy()
    return folder_selected

if __name__ == "__main__":
    # Let the user select the input folder
    input_folder = select_folder()

    if not input_folder:
        print("No folder selected. Exiting.")
    else:
        # Set the target dimensions for the cropped images (width, height)
        target_dimensions = (512, 512)

        # Set the output folder as a subfolder named "cropped_images" within the selected input folder
        output_folder = os.path.join(input_folder, "cropped_images")

        process_images(input_folder, output_folder, target_dimensions)
