"""
python3 -m venv venv
source venv/bin/activate
python3 -m pip install gradio pillow
"""

import gradio as gr
import os
import uuid
from PIL import Image

# Directory to store uploaded images
UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)
                                                                                                                                                                            
# Service 1: Save image and return UID                                                                                                                                      
def save_image_with_uid(image: Image.Image):                                                                                                                                
    uid = str(uuid.uuid4())                                                                                                                                                 
    image_path = os.path.join(UPLOAD_DIR, f"{uid}.png")
    image.save(image_path)
    return f"Image stored successfully.\nYour UID is:\n{uid}"

# Service 2: Delete image based on UID
def delete_image_by_uid(uid: str):
    image_path = os.path.join(UPLOAD_DIR, f"{uid}.png")
    if os.path.exists(image_path):
        os.remove(image_path)
        return f"Image with UID {uid} has been deleted."
    else:
        return f"No image found with UID {uid}."

# Interfaces
upload_interface = gr.Interface(
    fn=save_image_with_uid,
    inputs=gr.Image(type="pil"),
    outputs="text",
    title="Upload Image To Include In Training Dataset",
    description="Submit an image anonymously. A unique ID will be returned. You must have permission to share this image."
)

delete_interface = gr.Interface(
    fn=delete_image_by_uid,
    inputs=gr.Text(label="Enter UID"),
    outputs="text",
    title="Delete Image by UID from Training Database",
    description="Remove a previously submitted image by providing its UID."
)

# Launch both interfaces in a tabbed layout
app = gr.TabbedInterface(
    interface_list=[upload_interface, delete_interface],
    tab_names=["Submit Image For Training", "Delete Image From Database"]
)

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0",server_port=8084)
