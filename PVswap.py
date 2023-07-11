import os

def process_file(file_path):
    # Read the contents of the file
    with open(file_path, "r") as f:
        file_content = f.read()

    # Replace the desired strings in the file content
    file_content = file_content.replace(">PV<", ">PresentValue<")
    file_content = file_content.replace(">OP<", ">PresentValue<")
    file_content = file_content.replace(">SP<", ">PresentValue<")
    file_content = file_content.replace(">MD<", ">ModeState<")

    # Write the modified content back to the file
    with open(file_path, "w") as f:
        f.write(file_content)

    print(f"Modified file: {file_path}")

file = 'abstract_BH/2m-ahu1_files/DS_datasource1.dsd'

process_file(file)

# # Define the directory path
# directory = "abstract_BH"

# # Iterate through all folders and files in the directory
# for root, dirs, files in os.walk(directory):
#     for file in files:
#         # Check if the file starts with "DS_datasource"
#         if file.startswith("DS_datasource1.dsd"):
#             # Construct the file path
#             file_path = os.path.join(root, file)

#             # Process the file
#             process_file(file_path)