def get_image_data(file_path:str):
    with open(file_path, 'rb') as file:
        image_data = file.read()
    
    return image_data

def save_image_data(file_path: str, image_data: bytes):
    with open(file_path, 'wb') as file:
        file.write(image_data)


if __name__ == "__main__":
    # Example usage:
    file_path = "TEST.jpg"
    image_data = get_image_data(file_path)
    save_image_data("TEST.png", image_data)