# eventhive/utils/qr_utils.py

import qrcode
import os

def generate_qr_code(data, user_id, event_id, app_instance):
    """
    Generates a QR code for a user's event registration.
    
    :param data: The unique data to encode (e.g., a confirmation string).
    :param user_id: The ID of the user.
    :param event_id: The ID of the event.
    :param app_instance: The current Flask app instance to get the path.
    :return: The filename of the generated QR code.
    """
    # Define the filename for the QR code image
    filename = f"event{event_id}_user{user_id}.png"
    
    # Define the path to save the QR code image
    # It will be saved in the 'static/qr_codes/' folder
    qr_code_dir = os.path.join(app_instance.root_path, 'static', 'qr_codes')
    
    # Create the directory if it doesn't exist
    os.makedirs(qr_code_dir, exist_ok=True)
    
    filepath = os.path.join(qr_code_dir, filename)

    # Generate the QR code image
    img = qrcode.make(data)
    img.save(filepath)
    
    return filename