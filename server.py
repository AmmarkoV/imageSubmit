"""
python3 -m venv venv
source venv/bin/activate
python3 -m pip install gradio pillow
"""

import gradio as gr
import os
import uuid
from PIL import Image


#----------------------------------------------------------------------
#                  Gradio UI Translation Layer
#----------------------------------------------------------------------
def file_exists(path):
    return os.path.exists(path)

#If a file greek exists, trigger translation
GREEK_MENU=False
if (file_exists("greek")):
  GREEK_MENU=True

menuT = dict()
#----------------------------------------------------------------------
menuT["Upload Image To Include In Training Dataset"]="Ανέβασμα εικόνας για προσθήκη στα δεδομένα εκπαίδευσης"
menuT["Submit an image anonymously. A unique ID will be returned. You must have permission to share this image."]="Υποβάλετε μια εικόνα ανώνυμα. Θα σας επιστραφεί ένα μοναδικό αναγνωριστικό. Πρέπει να έχετε άδεια για να κοινοποιήσετε αυτήν την εικόνα."
menuT["Image"]="Εικόνα Εισόδου"
menuT["Output"]="Έξοδος"
menuT["Enter UID"]="Είσοδος αναγνωριστικού UID"
menuT["Delete Image by UID from Training Database"]="Διαγραφή εικόνας με αναγνωριστικό UID από την βάση δεδομένων εκπαίδευσης"
menuT["Submit Image For Training"]="Υποβολή εικόνας στο σετ εκπαίδευσης"
menuT["Delete Image From Database"]="Διαγραφή εικόνας από την βάση δεδομένων"
menuT["Clear"]="Καθαρισμός πεδίων"

menuT["Image stored successfully.\nYour UID is:\n"]="Η εικόνα προστέθηκε επιτυχώς.\nΤο αναγνωριστικό UID σας είναι:\n"
menuT["Deleted Image with UID"]="Διεγράφη η εικόνα με αναγνωριστικό"
menuT["No image found with UID"]="Δεν βρέθηκε εικόνα με το αναγνωριστικό"
menuT["Remove a previously submitted image by providing its UID."]="Διαγραφή μιας εικόνας δίνοντας το αναγνωριστικό UID της."

menuT["Submit Image For Training"]="Προσθήκη εικόνας στα δεδομένα εκπαίδευσης"
menuT["Delete Image From Database"]="Διαγραφή εικόνας από τα δεδομένα εκπαίδευσης"

#---------------------------------------------------------------------- 
def t(inputString):
 global GREEK_MENU
 if (GREEK_MENU):
  global menuT
  return menuT[inputString]
 return inputString
#---------------------------------------------------------------------- 

# Directory to store uploaded images
UPLOAD_DIR = "uploaded_images"
os.makedirs(UPLOAD_DIR, exist_ok=True)
                                                                                                                                                                            
# Service 1: Save image and return UID                                                                                                                                      
def save_image_with_uid(image: Image.Image):                                                                                                                                
    uid = str(uuid.uuid4())                                                                                                                                                 
    image_path = os.path.join(UPLOAD_DIR, f"{uid}.png")
    image.save(image_path)
    l = t("Image stored successfully.\nYour UID is:\n")
    return f"{l} {uid}"

# Service 2: Delete image based on UID
def delete_image_by_uid(uid: str):
    image_path = os.path.join(UPLOAD_DIR, f"{uid}.png")
    if os.path.exists(image_path):
        os.remove(image_path)
        l = t("Deleted Image with UID")
        return f"{l} {uid}."
    else:
        l = t("No image found with UID")
        return f"{l} {uid}."

# Interfaces
upload_interface = gr.Interface(
    fn=save_image_with_uid,
    inputs=gr.Image(label=t("Image"),type="pil"),
    outputs=gr.Text(label=t("Output")),  # Custom output label
    title=t("Upload Image To Include In Training Dataset"),
    description=t("Submit an image anonymously. A unique ID will be returned. You must have permission to share this image."),
    submit_btn=t("Submit Image For Training"),  # Translated submit
    clear_btn=t("Clear"),                        # Translated clear
)

delete_interface = gr.Interface(
    fn=delete_image_by_uid,
    inputs=gr.Text(label=t("Enter UID")),
    outputs=gr.Text(label=t("Output")),  # Custom output label
    title=t("Delete Image by UID from Training Database"),
    description=t("Remove a previously submitted image by providing its UID."),
    submit_btn=t("Delete Image From Database"),
    clear_btn=t("Clear"),
)

# Launch both interfaces in a tabbed layout
app = gr.TabbedInterface(
    interface_list=[upload_interface, delete_interface],
    tab_names=[t("Submit Image For Training"), t("Delete Image From Database")]
)

if __name__ == "__main__":
    app.launch(server_name="0.0.0.0",server_port=8084)
