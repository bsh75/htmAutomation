import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import os
from functions import *
from ungroup import remove_groups

# Folders containing graphics
originals_folder = 'Untouched abstract'
new_folder = 'abstract_BH/abstract_CPOupgradeWorking'

# Get a list of all files in the directory
files = os.listdir(originals_folder)

# Filter the list to include only .htm files
htm_files = [file for file in files if file.endswith(".htm")]
num_files = len(htm_files)
num_checkboxes = 0
files_changed = []

#################JUST ONE#################
# htm_files = ['2m-ahu5.htm']
#################JUST ONE#################

# Now iterate through the .htm files
for htm_file in htm_files:
    graphic = htm_file[0:-4]
    displayFolder = f'{graphic}_files'
    DISPLAYfile_o = f'{originals_folder}/{graphic}.htm'
    DSfile_o = f'{originals_folder}/{displayFolder}/DS_datasource1.dsd'
    BINDINGfile_o = f'{originals_folder}/{displayFolder}/Bindings.xml'

    new_DISPLAYfile = f'{new_folder}/{graphic}.htm'
    new_DSfile = f'{new_folder}/{displayFolder}/DS_datasource1.dsd'
    new_BINDINGfile = f'{new_folder}/{displayFolder}/Bindings.xml'

    # Open and read the current files for processing
    with open(DISPLAYfile_o, 'r') as file:
        htm_contents_g = file.read()
    # Removes the grouping involved with the checkbox elements
    htm_contents = remove_groups(htm_contents_g)
    # Finds all the checkbox elemets
    check_boxes = find_checkbox_elements(htm_contents)
    num_checkboxes += len(check_boxes)

    if len(check_boxes) == 0:
        print(f"NO CHECKBOXES FOUND in {graphic}")
    else:
        print(f"{len(check_boxes)} Checkboxes found in {graphic}")
        try:
            with open(DSfile_o, 'r') as dsfile:
                ds_contents = dsfile.read()
        except FileNotFoundError:
            print(f"File {DSfile_o} not found. Skipping....")
            continue
    
        with open(BINDINGfile_o, 'r') as bfile:
            b_contents = bfile.read()

        files_changed.append(graphic)

        deleted_elements = []
        shapes_added = []

        for i in range(0, len(check_boxes)): #change to len(check_boxes)
            # Get checkbox to replace
            checkBox = check_boxes[i]
            checkBoxName = extract_checkbox_id(checkBox)
            # print(f"Checkbox Name: {checkBoxName}")
            # if 'Man' in checkBoxName:
            #     print('Mancheck, continue')
            #     continue

            # Find new names for created shapes for Autobox and Relinquish
            shapeAuto, shapeRelinq = find_next_available_shape_numbers(htm_contents)
            deleted_elements.append(checkBox+'\n')
            
            # Get important information from checkbox element
            infoDisplay, infoData = extract_checkbox_info(checkBox)
            CB_LEFT = infoData[0]
            CB_TOP = infoData[1]
            auto_left = adjust_position(CB_LEFT, 0)
            auto_top = adjust_position(CB_TOP, 4)
            relinquish_left = adjust_position(CB_LEFT, 102)
            relinquish_top = adjust_position(CB_TOP, 4)
            CB_bindingID = infoData[2] 

            # Get find the binding object
            CB_objectID, binding_to_delete = find_objectID(b_contents, CB_bindingID)

            # Find the datasource object and corresponding point name
            pointName, DS_object_to_delete = get_point_name(ds_contents, CB_objectID)

            # Find the next available binding and object IDs
            HDXids = find_next_three_binding_ids(b_contents)
            DOids = find_next_three_object_ids(ds_contents)
            # print("HDX: Deleted: {}, Added: {}\tDS: Deleted: {}, Added: {}".format(CB_bindingID, HDXids, CB_objectID, DOids))

            # Get new code elements for each file
            autoBoxHTM, autoBoxXML, autoBoxDSD = get_auto_box(shapeAuto, pointName, HDXids, DOids, auto_left, auto_top, displayFolder)
            relinquish_script_string, relinquish_body_string, MS_relinquish_binding, RC_relinquish_binding, MS_relinquish_dataS, RC_relinquish_dataS = get_relinquish(shapeRelinq, pointName, HDXids, DOids, relinquish_left, relinquish_top, displayFolder)
            
            # Combine the relinquish and auto elements for each file
            HTM_elements_to_add = relinquish_body_string + autoBoxHTM
            DS_objects_to_add = MS_relinquish_dataS + RC_relinquish_dataS + autoBoxDSD
            bindings_to_add = MS_relinquish_binding + RC_relinquish_binding + autoBoxXML

            # HTM file changes
            htm_contents = insert_relinquish_script(htm_contents, relinquish_script_string)
            htm_contents = htm_contents.replace(checkBox, HTM_elements_to_add)
            with open(new_DISPLAYfile, 'w', encoding='utf-8') as new_file:
                new_file.write(htm_contents)

            # Binding file changes
            b_contents = b_contents.replace(binding_to_delete, bindings_to_add)
            with open(new_BINDINGfile, 'w', encoding='utf-8') as new_B_file:
                new_B_file.write(b_contents)

            # Datasource file changes
            ds_contents = ds_contents.replace(DS_object_to_delete, DS_objects_to_add)
            with open(new_DSfile, 'w', encoding='utf-8') as new_DS_file:
                new_DS_file.write(ds_contents)

            shapes_added.append((shapeAuto, shapeRelinq))

        print("New Shapes: {}".format(shapes_added))

for file in files_changed:
    print(file)

print(f"A total of {num_checkboxes} checkboxes adjusted from {len(files_changed)}/{num_files} files changed")