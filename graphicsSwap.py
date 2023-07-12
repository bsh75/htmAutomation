import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re
from functions import *

# Files
DISPLAYfile = 'checkingChanges2/afterChange.htm'
DSfile = 'checkingChanges2/afterChangeDS.dsd'
BINDINGfile = 'checkingChanges2/afterChangeBindings.xml'

# Folder name containing all the other files (location doesnt matter)
displayFolder = '2m-ahu2_files'

# Open and read the current file for processing
with open(DISPLAYfile, 'r') as file:
    html_content = file.read()

# Find all the checkbox elemets
check_boxes = find_checkbox_elements(html_content)
deleted_elements = []

for i in range(0, 1): #change to len(check_boxes)
    checkBox = check_boxes[i]

    shape = find_next_available_shape_number(html_content)

    deleted_elements.append(checkBox+'\n')
    infoDisplay, infoData = extract_checkbox_info(checkBox)
    CB_LEFT = infoData[0]
    CB_TOP = infoData[1]
    CB_bindingID = infoData[2] 

    CB_objectID, binding_to_delete = find_objectID(BINDINGfile, CB_bindingID)

    pointName, DS_object_to_delete = get_point_name(DSfile, CB_objectID)

    HDXids = find_next_two_binding_ids(BINDINGfile)

    DOids = find_next_two_object_ids(DSfile)

    relinquish_script_string, relinquish_body_string, MS_relinquish_binding, RC_relinquish_binding, MS_relinquish_dataS, RC_relinquish_dataS = get_relinquish(shape, pointName, HDXids, DOids, CB_LEFT, CB_TOP, displayFolder)
