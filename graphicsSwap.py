import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import os
from functions import *
from ungroup import remove_groups2
import math
from PVswap import remove_PV_from_file

# Folders containing graphics
originals_folder = 'Untouched abstract'
new_folder = 'abstract_BH/abstract_CPOupgradeWorking'

# Get a list of all files in the directory
files = os.listdir(originals_folder)

# Filter the list to include only .htm files
htm_files = [file for file in files if file.endswith(".htm")]
num_files = len(htm_files)
num_checkboxes = 0
pointNames = {}
files_changed = []
files_to_check = []
double_grouping_suspected = []

# Global params
autoAdjustor = 0 # Shifts the autobox by 7 pixels
BOX_to_Auto = -26
BOX_to_Relinq = 76

#################JUST ONE#################
htm_files = ['PCR1old.htm', 'misc-fansold,htm', '2m-fans.htm', 'misc-fans.htm']
#################JUST ONE#################

# Find a path to relinquish and MBS_hand folders to copy into other support folders
relinquish_folder, MBS_hand_folder = find_folders_in_folders(originals_folder, 'relinquish_control_files', 'MBS_Hand-24Apr_files')
relinquish_shape_file, MBS_hand_shape_file = find_files_in_folders(originals_folder, 'relinquish_control.sha', 'MBS_Hand-24Apr.sha')
# Now iterate through the .htm files
for htm_file in htm_files:
    graphic = htm_file[0:-4]
    displayFolder = f'{graphic}_files'
    DISPLAYfile_o = f'{originals_folder}/{graphic}.htm'
    support_folder_o = f'{originals_folder}/{displayFolder}'
    DSfile_o = f'{support_folder_o}/DS_datasource1.dsd'
    BINDINGfile_o = f'{support_folder_o}/Bindings.xml'

    new_DISPLAYfile = f'{new_folder}/{graphic}.htm'
    support_folder = f'{new_folder}/{displayFolder}'
    new_DSfile_path = f'{support_folder}/DS_datasource1.dsd'
    new_BINDINGfile_path = f'{support_folder}/Bindings.xml'

    # Open and read the current files for processing
    with open(DISPLAYfile_o, 'r') as file:
        htm_contents_g = file.read()
    # Removes the grouping involved with the checkbox elements
    htm_contents = remove_groups2(htm_contents_g)
    with open("play.htm", "w") as f:
        f.write(htm_contents)

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

        pointNames[graphic] = []
        # Check if the correct supporting files are in the original support folder and add them to new support folder if not
        if 'relinquish_control_files' not in os.listdir(support_folder_o):
            print("\nSHOULD BE COPYING RELINQ FOR", graphic)
            copy_file(source_file=relinquish_shape_file, destination_folder=support_folder)
            copy_folder(source_folder=relinquish_folder, destination_folder=support_folder)
        if 'MBS_Hand-24Apr_files' not in os.listdir(support_folder_o):
            print("\nSHOULD BE COPYING MBS FOR", graphic)
            copy_file(source_file=MBS_hand_shape_file, destination_folder=support_folder)
            copy_folder(source_folder=MBS_hand_folder, destination_folder=support_folder)

        deleted_elements = []
        shapes_added = []

        for i in range(0, len(check_boxes)): #change to len(check_boxes)
            # Get checkbox to replace
            checkBox = check_boxes[i]
            checkBoxName = extract_checkbox_id(checkBox)

            # Find new names for created shapes for Autobox and Relinquish
            shapeAuto, shapeRelinq = find_next_available_shape_numbers(htm_contents)
            deleted_elements.append(checkBox+'\n')
            
            # Get important information from checkbox element
            infoDisplay, infoData = extract_checkbox_info(checkBox)
            CB_LEFT = infoData[0]
            CB_TOP = infoData[1]
            CB_bindingID = infoData[2]

            # Get find the binding object
            CB_objectID, binding_to_delete = find_objectID(b_contents, CB_bindingID)

            # Find the datasource object and corresponding point name
            pointName, DS_object_to_delete = get_point_name(ds_contents, CB_objectID)
            pointNames[graphic].append(pointName)
            
            # Now reverse process to find the position of other objects with the same point name
            other_object_IDs_same_point = get_dataobject_ids_by_point_name(ds_contents, pointName)
            other_binding_IDs = find_binding_IDs(b_contents, other_object_IDs_same_point)
            coordinates_list = find_patterns_with_bindingIDs2(other_binding_IDs, htm_contents)

            # If there is no coordinates the position must be determined off the checkbox position
            if len(coordinates_list) == 0:
                auto_left = adjust_position(CB_LEFT, 0)
                auto_top = adjust_position(CB_TOP, 4)
                relinquish_left = adjust_position(CB_LEFT, 102)
                relinquish_top = adjust_position(CB_TOP, 4)
                if graphic not in files_to_check:
                    files_to_check.append(graphic)

            # If there are coordinates, find the closest one to the checkbox to position from
            elif len(coordinates_list) > 0:
                first = True
                for pattern in coordinates_list:
                    patternL, patternT, pattern_type = pattern
                    L_diff = int(patternL[:-2]) - int(CB_LEFT[:-2]) + BOX_to_Auto
                    T_diff =  int(patternT[:-2]) - int(CB_TOP[:-2])
                    diff_score = math.sqrt(L_diff**2 + T_diff**2)
                    if first:
                        closest_L = patternL
                        closest_T = patternT
                        diff_score_best = diff_score
                        first = False
                    elif diff_score < diff_score_best:
                        closest_L = patternL
                        closest_T = patternT
                        diff_score_best = diff_score
                
                # TOP should be +1, AutoL should be - 26, RelL should be + 76 from other element.
                auto_left = adjust_position(closest_L, BOX_to_Auto+autoAdjustor)
                auto_top = adjust_position(closest_T, 1)
                relinquish_left = adjust_position(closest_L, BOX_to_Relinq)
                relinquish_top = adjust_position(closest_T, 1)

            if '-RT' in pointName:
                auto_left = adjust_position(auto_left, 18-autoAdjustor)
                relinquish_left = adjust_position(relinquish_left, 31)

            if pointName.endswith('-SP') and 'setpoints' in graphic:
                relinquish_left = adjust_position(relinquish_left, 112)

            # if pointName.endswith('AD'):
            #     # shift both items right a few pixels

            # Find the next available binding and object IDs
            HDXids = find_next_three_binding_ids(b_contents)
            DOids = find_next_three_object_ids(ds_contents)

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
            with open(new_BINDINGfile_path, 'w', encoding='utf-8') as new_B_file:
                new_B_file.write(b_contents)

            # Datasource file changes
            ds_contents = ds_contents.replace(DS_object_to_delete, DS_objects_to_add)
            with open(new_DSfile_path, 'w', encoding='utf-8') as new_DS_file:
                new_DS_file.write(ds_contents)

            shapes_added.append((shapeAuto, shapeRelinq))

    # Each datasource file also needs to have all mentions of PV MD OP SP swapped
    remove_PV_from_file(new_DSfile_path)


for file in files_changed:
    print(file)

print(f"A total of {num_checkboxes} checkboxes adjusted from {len(files_changed)}/{num_files} files changed")
print(f"Shoud have a look at {len(files_to_check)} files: {files_to_check}")
print(f"Double grouping suspected in {len(double_grouping_suspected)} files: {double_grouping_suspected}")
print(f"Pointnames changed: {pointNames}")