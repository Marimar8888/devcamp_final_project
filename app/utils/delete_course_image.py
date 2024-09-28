import os

def delete_course_image(image_path):
    image_filename = os.path.basename(image_path)
    full_image_path = os.path.join('app', 'static', 'uploads', image_filename)

    if os.path.exists(full_image_path):
        os.remove(full_image_path)
        print(f"Deleted image: {full_image_path}")
    else:
        print(f"File does not exist: {full_image_path}")