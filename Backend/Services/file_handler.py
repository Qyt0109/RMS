def file_to_bytes(file_path: str) -> bytes:
    try:
        with open(file_path, 'rb') as file:
            file_bytes = file.read()
        return file_bytes
    except FileNotFoundError:
        print(f"Error: File not found - {file_path}")
        return None
    except Exception as e:
        print(f"Error reading file: {e}")
        return None

def bytes_to_file(file_path: str, byte_data: bytes) -> bool:
    try:
        with open(file_path, 'wb') as file:
            file.write(byte_data)
        print(f"File saved: {file_path}")
        return True
    except Exception as e:
        print(f"Error saving file: {e}")
        return False