import os

def remove_PV_from_file(new_file_path):
    try:
        # Read the contents of the file
        with open(new_file_path, "r") as f:
            file_content = f.read()

        # Replace the desired strings in the file content
        file_content = file_content.replace(">PV<", ">PresentValue<")
        file_content = file_content.replace(">OP<", ">PresentValue<")
        file_content = file_content.replace(">SP<", ">PresentValue<")
        file_content = file_content.replace(">MD<", ">ModeState<")

        # Write the modified content back to the file
        with open(new_file_path, "w") as f:
            f.write(file_content)

        print(f"Modified file: {new_file_path}")
    except FileNotFoundError:
        print(f"The file '{new_file_path}' doesn't exist. Continuing with other operations...")
