import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
from functions import *

# Files
DISPLAYfile = 'checkingChanges2/after.htm'
DSfile = 'checkingChanges2/after.dsd'
BINDINGfile = 'checkingChanges2/after.xml'

# Folder name containing all the other files (location doesnt matter)
displayFolder = '2m-ahu2_files'

# Open and read the current file for processing
with open(DISPLAYfile, 'r') as file:
    html_content = file.read()

# Find all the checkbox elemets
check_boxes = find_checkbox_elements(html_content)
deleted_elements = []

for i in range(0, len(check_boxes)): #change to len(check_boxes)
    checkBox = check_boxes[i]
    checkBoxName = extract_checkbox_id(checkBox)
    print("CheckBox Deleted: ", checkBoxName)

    shape = find_next_available_shape_number(DISPLAYfile)
    print("New Shape Created: ", shape)
    
    deleted_elements.append(checkBox+'\n')
    infoDisplay, infoData = extract_checkbox_info(checkBox)
    CB_LEFT = infoData[0]
    CB_TOP = infoData[1]
    CB_bindingID = infoData[2] 
    print(infoData)

    CB_objectID, binding_to_delete = find_objectID(BINDINGfile, CB_bindingID)
    # print(binding_to_delete)

    pointName, DS_object_to_delete = get_point_name(DSfile, CB_objectID)
    print(DS_object_to_delete)

    HDXids = find_next_two_binding_ids(BINDINGfile)

    DOids = find_next_two_object_ids(DSfile)

    print("HDX: Deleted: {}, Added: {}\nDS: Deleted: {}, Added: {}".format(CB_bindingID, HDXids, CB_objectID, DOids))

    autoBoxHTM, autoBoxXML, autoBoxDSD = get_auto_box(shape, pointName, HDXids, DOids, CB_LEFT, CB_TOP, displayFolder)

    # Replacel the checkbox with Auto box 
    # replace_string_in_file(DISPLAYfile, checkBox, autoBoxHTM)
    # replace_string_in_file(BINDINGfile, binding_to_delete, autoBoxXML)
    # replace_string_in_file(DSfile, DS_object_to_delete, autoBoxDSD)
    # THIS WORKS FOR AUTOBOX ONLY ^^^
    
    relinquish_script_string, relinquish_body_string, MS_relinquish_binding, RC_relinquish_binding, MS_relinquish_dataS, RC_relinquish_dataS = get_relinquish(shape, pointName, HDXids, DOids, CB_LEFT, CB_TOP, displayFolder)
    DS_object_to_add = MS_relinquish_dataS + RC_relinquish_dataS
    binding_to_add = MS_relinquish_binding + RC_relinquish_binding

    insert_relinquish_script(DISPLAYfile, relinquish_script_string)
    replace_string_in_file(DISPLAYfile, checkBox, relinquish_body_string)
    search_substring_in_file(DISPLAYfile, checkBoxName)

    replace_string_in_file(DSfile, DS_object_to_delete, DS_object_to_add)
    search_substring_in_file(DSfile, 'id="{}"'.format(CB_objectID))

    replace_string_in_file(BINDINGfile, binding_to_delete, binding_to_add)
    search_substring_in_file(BINDINGfile, 'ID="{}"'.format(CB_bindingID))

print("Made {} replacements".format(i))