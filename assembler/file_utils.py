def read_file(file_name) -> list:
    try:
        with open(file_name, "r") as f:
            return f.readlines()
    except FileNotFoundError:
        print(f"Error: File {file_name} not found")
        exit()
