import hashlib

def hash_string(input_string) -> str:
    """ Hash string input """
    # Create a new hashlib object with the SHA-256 algorithm
    hash_object = hashlib.sha256()
    # Update the hash with the input string
    hash_object.update(input_string.encode('utf-8'))
    # Get the hexadecimal representation of the hash
    hash_value = hash_object.hexdigest()
    return hash_value

if __name__ == "__main__":
    # Example usage:
    input_str = "Hello"
    hashed_str = hash_string(input_str)
    print(f"The SHA-256 hash of '{input_str}' is: {hashed_str}")
