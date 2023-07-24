import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
from functions import *

# Files
graphic = '2m-ahu3'
displayFolder = f'{graphic}_files'
DISPLAYfile = f'abstract_BH/{graphic}.htm'
DSfile = f'abstract_BH/{displayFolder}/DS_datasource1.dsd' # abstract_BH\2m-ahu3_files\DS_datasource1.dsd
BINDINGfile = f'abstract_BH/{displayFolder}/Bindings.xml'

# Folder name containing all the other files (location doesnt matter)

# Open and read the current file for processing
with open(DISPLAYfile, 'r') as file:
    html_content = file.read()

# Find all the checkbox elemets
check_boxes = find_checkbox_elements(html_content)
deleted_elements = []
shapes_added = []

for i in range(0, len(check_boxes)): #change to len(check_boxes)
    # Get checkbox to replace
    checkBox = check_boxes[i]
    checkBoxName = extract_checkbox_id(checkBox)
    # print("CheckBox Deleted: ", checkBoxName)

    # Find new names for created shapes for Autobox and Relinquish
    shapes = find_next_available_shape_numbers(DISPLAYfile)
    shapeAuto = shapes[0]
    shapeRelinq = shapes[1]
    # print("New Shapes Created: ", shapeAuto, shapeRelinq)
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
    print(infoData)

    # Get find the binding object
    CB_objectID, binding_to_delete = find_objectID(BINDINGfile, CB_bindingID)
    # print(binding_to_delete)

    # Find the datasource object and corresponding point name
    pointName, DS_object_to_delete = get_point_name(DSfile, CB_objectID)
    # print(DS_object_to_delete)

    # Find the next available binding and object IDs
    HDXids = find_next_three_binding_ids(BINDINGfile)
    DOids = find_next_three_object_ids(DSfile)
    print("HDX: Deleted: {}, Added: {}\nDS: Deleted: {}, Added: {}".format(CB_bindingID, HDXids, CB_objectID, DOids))

    # Get new code elements for each file
    autoBoxHTM, autoBoxXML, autoBoxDSD = get_auto_box(shapeAuto, pointName, HDXids, DOids, auto_left, auto_top, displayFolder)
    relinquish_script_string, relinquish_body_string, MS_relinquish_binding, RC_relinquish_binding, MS_relinquish_dataS, RC_relinquish_dataS = get_relinquish(shapeRelinq, pointName, HDXids, DOids, relinquish_left, relinquish_top, displayFolder)
    
    # Combine the relinquish and auto elements for each file
    HTM_elements_to_add = relinquish_body_string + autoBoxHTM
    DS_objects_to_add = MS_relinquish_dataS + RC_relinquish_dataS + autoBoxDSD
    bindings_to_add = MS_relinquish_binding + RC_relinquish_binding + autoBoxXML

    # HTM file changes
    insert_relinquish_script(DISPLAYfile, relinquish_script_string)
    replace_string_in_file(DISPLAYfile, checkBox, HTM_elements_to_add)
    search_substring_in_file(DISPLAYfile, checkBoxName)

    # Binding file changes
    replace_string_in_file(BINDINGfile, binding_to_delete, bindings_to_add)
    search_substring_in_file(BINDINGfile, 'ID="{}"'.format(CB_bindingID))

    # Datasource file changes
    replace_string_in_file(DSfile, DS_object_to_delete, DS_objects_to_add)
    search_substring_in_file(DSfile, 'id="{}"'.format(CB_objectID))

    shapes_added.append(shapes)

print("New Shapes: {}".format(shapes_added))

print("Made {} replacements".format(i))