def allowed_file(filename, extensions):
    """Helper function to check if a file is the correct file extension

        Args:
            filename (string): filename as a string
            extensions (list): The list of accepted file extensions

        Returns:
            bool: True if filename is accepted
        """
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in extensions

def validate_upload_file(files, extensions):
    """Helper function to check if an uploaded file is valid

        Args:
            files (list): The list of file objects from the post request
            extensions (list): The list of accepted file extensions

        Returns:
            File: The file object if success or None
            string: An error string if failed or None
        """


    # check if the post request has the file part
    if 'file' not in files:
        return None, 'No file part.'

    # get the file
    file = files['file']

    # if user does not select file, browser also
    # submit an empty part without filename
    if file.filename == '':
        return None, 'No selected file.'

    #check for allowed extensions
    if file:
        if allowed_file(file.filename, extensions):
            return file, None
        else:
            ext_str = ",".join(extensions)
            return None, 'Invalid file format. File must be of type {}'.format(ext_str)
