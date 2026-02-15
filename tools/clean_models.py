import os

file_path = 'items/models.py'

try:
    with open(file_path, 'rb') as f:
        content = f.read()

    if b'\x00' in content:
        print("Found null bytes. Cleaning...")
        clean_content = content.replace(b'\x00', b'')
        
        # Verify it decodes
        try:
            text = clean_content.decode('utf-8')
            # Write back
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(text)
            print("Successfully cleaned items/models.py")
        except UnicodeDecodeError as e:
            print(f"Error decoding cleaned content: {e}")
    else:
        print("No null bytes found.")

except Exception as e:
    print(f"An error occurred: {e}")
