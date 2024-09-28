import os
from werkzeug.utils import secure_filename

def save_file(file, upload_folder):
    if not file or file.filename == '':
        return None, None

    if not allowed_file(file.filename):
        return None, 'File type not allowed.'

    filename = secure_filename(file.filename)
    file_path = os.path.join(upload_folder, filename)

    print(f"Saving file to: {file_path}")

    try:
        file.save(file_path)
        return filename, None
    except Exception as e:
        return None, str(e)

def allowed_file(filename):
    allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in allowed_extensions