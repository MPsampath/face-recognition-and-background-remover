# import sys
# import json
# import io
# import cv2
# from PIL import Image
# import os

# # Check for required dependencies
# def check_requirements():
#     missing_requirements = []
    
#     try:
#         from rembg import remove
#     except ImportError:
#         missing_requirements.append("rembg")
    
#     try:
#         from PIL import Image, ImageEnhance
#     except ImportError:
#         missing_requirements.append("Pillow (PIL)")
    
#     if missing_requirements:
#         # JSON error response if requirements are missing
#         print(json.dumps({
#             "status": "error",
#             "message": f"Missing required dependencies: {', '.join(missing_requirements)}. Please install them and try again."
#         }))
#         sys.exit(1)

# # Load the input image
# def load_image(input_path):
#     with open(input_path, 'rb') as input_file:
#         return input_file.read()

# # Remove the background from the image data
# def remove_background(image_data):
#     from rembg import remove
#     return remove(image_data)

# # Detecting human face is include or not
# def face_detection(image_path, save_path, top_padding=300, bottom_padding=200, side_padding=120):

#     # Step 1: Load the image
#     img = cv2.imread(image_path)
#     print(img)
#     if img is None:
#         print(json.dumps({
#             "status": "error",
#             "message": "Image not found or cannot be opened"
#         }))
#         return
    
#     # Convert to grayscale for face detection
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
#     # Load the face detector (Haar Cascade)
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
#     # Detect faces
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10)
    
#     if len(faces) > 0:
#         # Assume the first detected face is the one to crop
#         x, y, w, h = faces[0]
#         # print(x, y, w, h,img.shape)
#         # Step 2: Expand the bounding box to include the body (specific padding for different parts)
#         top = max(y - top_padding, 0)  # Add padding above for hair
#         bottom = min(y + h + bottom_padding, img.shape[0])  # Add padding below for chin
#         left = max(x - side_padding, 0)  # Add padding to the left for ear
#         right = min(x + w + side_padding, img.shape[1])  # Add padding to the right for ear
        
#         # Step 3: Crop the image based on the expanded bounding box
#         cropped_img = img[top:bottom, left:right]

#         # Step 4: Save the cropped image
#         cv2.imwrite(save_path, cropped_img)

#         print(json.dumps({
#             "status": "success",
#             "message": "Image cropped and saved successfully"
#         }))
#         return cropped_img
        
#     else:
#         print(json.dumps({
#             "status": "error",
#             "message": "No face detected"
#         }))
#         sys.exit(1)

# # Function to add the face to a canvas
# def add_face_to_canvas(face_path, output_path, canvas_size=(450, 530)):
#     # Load the face image (assumed to be a transparent PNG)
#     face_img = Image.open(io.BytesIO(face_path)).convert("RGBA")
#     # print(face_img)
#     top_edge =  find_top_edge(face_img)
   
#     # Get the pixel data
#     pixels = face_img.load()
    
#     width, height = face_img.size

    
#     face_img = enhance_contrast(face_img, factor=1.2)
#     # Resize the face image to fit within the canvas size
#     canvas_width, canvas_height = canvas_size
#     face_width, face_height = face_img.size
    
#     # Calculate the resizing ratio
#     width_ratio = canvas_width / face_width
#     height_ratio = canvas_height / face_height
#     resize_ratio = min(width_ratio, height_ratio)  # Maintain the aspect ratio
    
#     # Resize the face image while maintaining the aspect ratio
#     new_width = int(face_width * resize_ratio)
#     new_height = int(face_height * resize_ratio)
#     resized_face_img = face_img.resize((new_width, new_height), Image.Resampling.LANCZOS)
    
#     # Create a blank canvas (white background) with the same size as the desired canvas
#     canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))  # RGBA for transparency
#     # Calculate the position to center the face image on the canvas
#     x_position = (canvas_width - new_width) // 2  # Center horizontally
#     y_position = (canvas_height -new_height- top_edge) // 4 # Adjust for top edge distance (can tweak this)
#     print(canvas_width, new_width,canvas_height, new_height,x_position, y_position)
    
#     # Place the resized face image on the canvas
#     canvas.paste(resized_face_img, (x_position, y_position), resized_face_img)  # The third argument is the mask for transparency
    
#     # Save the final image
#     save_image(canvas, output_path)
#     # print(f"Image saved as {output_path}")
# # Enhance the contrast of the image
# def enhance_contrast(image, factor=1.2):
#     from PIL import ImageEnhance
#     enhancer = ImageEnhance.Contrast(image)
#     return enhancer.enhance(factor)

# def find_top_edge(img):
    
#     # Get the pixel data
#     pixels = img.load()

#     # Iterate through the pixels of the top row (y = 0)
#     width, height = img.size
#     for y in range(height):
#         r, g, b, a = pixels[width/2, y]  # Get the pixel at (x, 0)
        
#         # Check if the pixel is not transparent (a != 0) or not the background color
#         if a != 0:  # This checks for transparency
#             # print(f"Top edge found at (x=0, y={y}) with pixel value (R={r}, G={g}, B={b}, A={a})")
#             return y  # Return the x-coordinate of the first non-transparent pixel
#     return None

# # Save the processed image
# def save_image(image, output_path):
#     image.save(output_path, format="PNG")

# def process_image(input_path,output_path):
    
#     face_detection(input_path,output_path)

#     image_data = load_image(output_path)
#     # print(image_data)
#     baground_removed_image = remove_background(image_data)

#     add_face_to_canvas(baground_removed_image,output_path)


# if __name__ == "__main__":
#     # Check all requirements before proceeding
#     check_requirements()
   
#     if len(sys.argv) != 3:
#         print(json.dumps({"status": "error", "message": "Usage: python face_recognition.py <input_folder_path> <output_folder_path>"}))
#         sys.exit(1)
 
#     input_folder = sys.argv[1]
#     output_folder = sys.argv[2]
#     process_image(input_folder, output_folder)
    # if not os.path.exists(output_folder):
    #     os.makedirs(output_folder)
 
    # supported_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")
 
    # count = 1
    # for filename in os.listdir(input_folder):
    #     if filename.lower().endswith(supported_extensions):
    #         input_path = os.path.join(input_folder, filename)
           
    #         base_name = os.path.splitext(filename)[0]
    #         output_filename = f"{base_name}_{count}.png"
    #         output_path = os.path.join(output_folder, output_filename)
 
    #         try:
    #             print(f"Processing: {input_path}")
    #             process_image(input_path, output_path)
    #             print(f"Done: {output_path}")
    #             count += 1
    #         except Exception as e:
    #             print(json.dumps({
    #                 "status": "error",
    #                 "message": f"Error processing {filename}: {str(e)}"
    #             }))
























# def check_requirements():
#     missing_requirements = []
   
#     try:
#         from rembg import remove
#     except ImportError:
#         missing_requirements.append("rembg")
   
#     try:
#         from PIL import Image, ImageEnhance
#     except ImportError:
#         missing_requirements.append("Pillow (PIL)")
   
#     if missing_requirements:
#         # JSON error response if requirements are missing
#         print(json.dumps({
#             "status": "error",
#             "message": f"Missing required dependencies: {', '.join(missing_requirements)}. Please install them and try again."
#         }))
#         sys.exit(1)
 
# # Load the input image
# def load_image(input_path):
#     with open(input_path, 'rb') as input_file:
#         return input_file.read()
 
# # Remove the background from the image data
# def remove_background(image_data):
#     from rembg import remove
#     return remove(image_data)
 
# # Detecting human face is include or not
# def face_detection(image_path, save_path, face_expand_ratio=2.0):
#     import numpy as np
 
#     # Step 1: Load the image
#     img = cv2.imread(image_path)
#     if img is None:
#         print(json.dumps({
#             "status": "error",
#             "message": "Image not found or cannot be opened"
#         }))
#         sys.exit(1)
   
#     gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
 
#     face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
#     faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10)
 
#     if len(faces) == 0:
#         print(json.dumps({
#             "status": "error",
#             "message": "No face detected"
#         }))
#         sys.exit(1)
 
#     # Get first face and expand
#     x, y, w, h = faces[0]
 
#     # Expand the box by a ratio
#     center_x = x + w // 2
#     center_y = y + h // 2
#     max_dim = int(max(w, h) * face_expand_ratio)
 
#     left = max(center_x - max_dim // 2, 0)
#     top = max(center_y - max_dim // 2, 0)
#     right = min(center_x + max_dim // 2, img.shape[1])
#     bottom = min(center_y + max_dim // 2, img.shape[0])
 
#     # Crop the expanded region
#     cropped_img = img[top:bottom, left:right]
 
#     # Save cropped face+head+shoulder
#     cv2.imwrite(save_path, cropped_img)
 
#     print(json.dumps({
#         "status": "success",
#         "message": "Face-centered image cropped successfully"
#     }))
#     return save_path
 
 
# # Function to add the face to a canvas
# def add_face_to_canvas(face_path, output_path, canvas_size=(450, 530), vertical_padding=20):
#     from PIL import Image
#     import numpy as np
#     import cv2
 
#     face_img = Image.open(face_path).convert("RGBA")
#     canvas_width, canvas_height = canvas_size
 
#     # Convert to numpy array and grayscale
#     open_cv_img = np.array(face_img)
#     alpha_channel = open_cv_img[..., 3]
   
#     # Get non-transparent bounding box (content area after background removal)
#     coords = cv2.findNonZero(alpha_channel)
#     x, y, w, h = cv2.boundingRect(coords)
 
#     # Crop to non-transparent region
#     cropped = face_img.crop((x, y, x + w, y + h))
 
#     # Resize keeping hair-chin area and padding in mind
#     available_height = canvas_height - (2 * vertical_padding)
#     resize_ratio = min(canvas_width / w, available_height / h)
 
#     new_width = int(w * resize_ratio)
#     new_height = int(h * resize_ratio)
#     resized_img = cropped.resize((new_width, new_height), Image.Resampling.LANCZOS)
 
#     # Create transparent canvas
#     canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
 
#     # Center horizontally and vertically (with equal top/bottom gap from content)
#     x_offset = (canvas_width - new_width) // 2
#     y_offset = (canvas_height - new_height) // 2
 
#     canvas.paste(resized_img, (x_offset, y_offset), resized_img)
#     canvas.save(output_path, format="PNG")
#     print(f"Final centered image saved to {output_path}")
 
 
 
 
# # Save the processed image
# def save_image(image, output_path):
#     image.save(output_path, format="PNG")
 
# def process_image(input_path,output_path):
   
#     face_detection(input_path, output_path)
 
#     image_data = load_image(output_path)
#     background_removed_data = remove_background(image_data)
#     face_image = Image.open(io.BytesIO(background_removed_data)).convert("RGBA")
 
#     # Save temporarily to disk to reuse existing `add_face_to_canvas`
#     temp_path = output_path.replace(".png", "_nobg.png")
#     face_image.save(temp_path)
 
#     # Final centered output
#     add_face_to_canvas(temp_path, output_path)
 
#     # Optionally remove temp
#     os.remove(temp_path)
 
# if __name__ == "__main__":
#     # Check all requirements before proceeding
#     check_requirements()
   
#     if len(sys.argv) != 3:
#         print(json.dumps({"status": "error", "message": "Usage: python face_recognition.py <input_folder_path> <output_folder_path>"}))
#         sys.exit(1)
 
#     input_folder = sys.argv[1]
#     output_folder = sys.argv[2]
 
#     if not os.path.exists(output_folder):
#         os.makedirs(output_folder)
 
#     supported_extensions = (".jpg", ".jpeg", ".png", ".bmp", ".tiff")
 
#     count = 1
#     for filename in os.listdir(input_folder):
#         if filename.lower().endswith(supported_extensions):
#             input_path = os.path.join(input_folder, filename)
           
#             base_name = os.path.splitext(filename)[0]
#             output_filename = f"{base_name}_{count}.png"
#             output_path = os.path.join(output_folder, output_filename)
 
#             try:
#                 print(f"Processing: {input_path}")
#                 process_image(input_path, output_path)
#                 print(f"Done: {output_path}")
#                 count += 1
#             except Exception as e:
#                 print(json.dumps({
#                     "status": "error",
#                     "message": f"Error processing {filename}: {str(e)}"
#                 }))











import sys
import json
import io
import cv2
from PIL import Image, ImageEnhance
import numpy as np

def check_requirements():
    missing_requirements = []
    try:
        from rembg import remove
    except ImportError:
        missing_requirements.append("rembg")
    try:
        from PIL import Image
    except ImportError:
        missing_requirements.append("Pillow")
    if missing_requirements:
        print(json.dumps({
            "status": "error",
            "message": f"Missing dependencies: {', '.join(missing_requirements)}"
        }))
        sys.exit(1)

def face_detection(image_path, top_padding=300, bottom_padding=200, side_padding=120):
    img = cv2.imread(image_path)
    if img is None:
        print(json.dumps({
            "status": "error",
            "message": "Image not found or cannot be opened"
        }))
        sys.exit(1)

    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=10)

    if len(faces) == 0:
        print(json.dumps({
            "status": "error",
            "message": "No face detected"
        }))
        sys.exit(1)

    x, y, w, h = faces[0]
    top = max(y - top_padding, 0)
    bottom = min(y + h + bottom_padding, img.shape[0])
    left = max(x - side_padding, 0)
    right = min(x + w + side_padding, img.shape[1])
    cropped_img = img[top:bottom, left:right]
    return cropped_img

def remove_background_from_array(image_array):
    from rembg import remove
    _, buffer = cv2.imencode('.png', image_array)
    image_bytes = buffer.tobytes()
    return remove(image_bytes)

def enhance_contrast(image, factor=1.2):
    enhancer = ImageEnhance.Contrast(image)
    return enhancer.enhance(factor)

def find_top_edge(img):
    pixels = img.load()
    width, height = img.size
    for y in range(height):
        r, g, b, a = pixels[width // 2, y]
        if a != 0:
            return y
    return 0

def add_face_to_canvas(face_bytes, output_path, canvas_size=(450, 530)):
    face_img = Image.open(io.BytesIO(face_bytes)).convert("RGBA")
    top_edge = find_top_edge(face_img)
    face_img = enhance_contrast(face_img, factor=1.2)

    canvas_width, canvas_height = canvas_size
    face_width, face_height = face_img.size
    resize_ratio = min(canvas_width / face_width, canvas_height / face_height)
    new_width = int(face_width * resize_ratio)
    new_height = int(face_height * resize_ratio)
    resized_face_img = face_img.resize((new_width, new_height), Image.Resampling.LANCZOS)

    canvas = Image.new("RGBA", canvas_size, (0, 0, 0, 0))
    x_position = (canvas_width - new_width) // 2
    y_position = (canvas_height - new_height - top_edge) // 4
    canvas.paste(resized_face_img, (x_position, y_position), resized_face_img)
    
    # Save to stdout as binary
    canvas.save(sys.stdout.buffer, format="PNG")


def process_image(input_path, output_path):
    cropped_img = face_detection(input_path)
    bg_removed_bytes = remove_background_from_array(cropped_img)
    add_face_to_canvas(bg_removed_bytes, output_path)
    print(json.dumps({
        "status": "success",
        "message": "Image processed and saved successfully"
    }))

if __name__ == "__main__":
    check_requirements()
    if len(sys.argv) != 3:
        print(json.dumps({
            "status": "error",
            "message": "Usage: python face_recognition.py <input_path> <output_path>"
        }))
        sys.exit(1)

    input_path = sys.argv[1]
    output_path = sys.argv[2]
    process_image(input_path, output_path)
