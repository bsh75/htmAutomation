import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re

def extract_checkbox_id(checkbox_element):
    # Extract the id attribute value using regular expression
    id_match = re.search(r'id=([^ ]+)', checkbox_element)

    if id_match:
        id_value = id_match.group(1)
        return id_value
    else:
        return None
    
def search_substring_in_file(file_path, substring):
    try:
        with open(file_path, 'r') as file:
            file_content = file.read()
            if substring in file_content:
                print(f"YAY - The substring '{substring}' was found in the file.")
            else:
                print(f"YAY - The substring '{substring}' was not found in the file.")
    except FileNotFoundError:
        print(f"File '{file_path}' not found.")

def find_next_two_binding_ids(xml_file):
    '''This should find the next two available binding ids for the new element'''

    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extract the binding IDs from the XML
    binding_ids = [int(binding.attrib['ID']) for binding in root.findall('binding')]

    # Find the maximum binding ID
    max_id = max(binding_ids) if binding_ids else -1

    # Determine the next free binding ID
    next_ids = [max_id + 1, max_id + 2]

    return next_ids

def find_next_two_object_ids(DS_file):
    '''This should find the next two available maximum object ids for the new element'''
    with open(DS_file, 'r') as file:
        datasource_content = file.read()

    dataobject_ids = re.findall(r'<dataobject id="(\d+)"', datasource_content)
    dataobject_ids = [int(id) for id in dataobject_ids]

    max_id = max(dataobject_ids) if dataobject_ids else 0
    next_available_ids = [max_id + 1, max_id + 2]

    return next_available_ids
# THESE ARE THE SAME JUST ONE FINDS LARGEST NUMBERS, OTHER FINDS NESTED FREE ONES
def find_next_free_object_ids(DS_file):
    '''This should find the next two available object ids for the new element'''
    with open(DS_file, 'r') as file:
        datasource_content = file.read()

    dataobject_ids = re.findall(r'<dataobject id="(\d+)"', datasource_content)
    dataobject_ids = set(map(int, dataobject_ids))  # Convert to set for efficient lookup

    next_available_ids = []
    current_id = 1
    while len(next_available_ids) < 2:
        if current_id not in dataobject_ids:
            next_available_ids.append(current_id)
        current_id += 1

    return next_available_ids

def find_next_available_shape_number(Dfile):
    with open(Dfile, 'r') as file:
        file_content = file.read()

    pattern = r'shape(\d{3})'
    shape_numbers = [int(match.group(1)) for match in re.finditer(pattern, file_content)]
    
    # Find the next available number that is not present in the file
    for i in range(1, 1000):
        if i not in shape_numbers:
            next_number_formatted = f"{i:03}"  # Format the number with 3 digits
            return f"shape{next_number_formatted}"
    
    return None  # Return None if all possible numbers are taken

def find_checkbox_elements(html_content):
    '''Finds all the check box elements and returns a list of them'''
    pattern = r'<SPAN[^>]*class=hsc\.checkbox[^>]*>.*?Checkbox</SPAN></SPAN>'
    checkbox_matches = re.findall(pattern, html_content, re.DOTALL)
    return checkbox_matches

def extract_checkbox_info(checkbox_content):
    '''Extracts all the relevant information from a given checkbox: [LEFT, TOP, HDXid]'''
    left_match = re.search(r'LEFT:\s*([\d.]+)(%|px)', checkbox_content)
    top_match = re.search(r'TOP:\s*([\d.]+)(%|px)', checkbox_content)
    binding_id_match = re.search(r'HDXBINDINGID:\s*(\d+)', checkbox_content)

    infoDisplay = ""
    infoData = []

    if left_match and top_match:
        left = f"{left_match.group(1)}{left_match.group(2)}"
        top = f"{top_match.group(1)}{top_match.group(2)}"
        coordinates = f"LEFT: {left}\tTOP: {top}"
        infoData = [left, top]

        if binding_id_match:
            binding_id = binding_id_match.group(1)
            coordinates += f"\tHDXBINDINGID: {binding_id}"
            infoData.append(binding_id)
        infoDisplay = coordinates

    elif binding_id_match:
        binding_id = binding_id_match.group(1)
        infoDisplay = f"HDXBINDINGID: {binding_id}"
        infoData = [binding_id]
    return infoDisplay, infoData

def extract_and_copy_checkboxes(html_file):
    '''Finds all the check box elements and extracts all the relevant information about them as a list of [[LEFT, TOP, HDXid], ...]'''
    with open(html_file, 'r') as file:
        html_content = file.read()

    checkbox_matches = find_checkbox_elements(html_content)
    deleted_elements = []
    allInfo = []
    for match in checkbox_matches:
        deleted_elements.append(match+'\n')
        infoDisplay, infoData = extract_checkbox_info(match)
        allInfo.append(infoData)
        print(infoDisplay)

    with open('deletedElements.txt', 'w') as file:
        for element in deleted_elements:
            file.write(f"{element}\n")

    return allInfo


def find_and_copy_bindings(xml_file, target_ids):
    '''Copys all the bindings from xml with binding id's in "target_ids" and finds the corresponding object id's'''
    with open(xml_file, 'r') as file:
        xml_content = file.read()

    pattern = r'<binding ID="(\d+)">(.*?)</binding>'
    binding_matches = re.findall(pattern, xml_content, re.DOTALL)

    deleted_bindings = []
    associated_objectids = []

    for match in binding_matches:
        binding_id, binding_content = match
        if binding_id in target_ids:
            deleted_bindings.append(binding_content + '</binding>')

            objectid_match = re.search(r'objectid="(\d+)"', binding_content)
            if objectid_match:
                associated_objectids.append(objectid_match.group(1))

    with open('deletedBindings.txt', 'w') as file:
        for binding in deleted_bindings:
            file.write(f"{binding}\n")

    if associated_objectids:
        print(f"The associated objectids are: {', '.join(associated_objectids)}")

    return associated_objectids

def find_objectID(xml_file, target_id):
    '''Copys all the bindings from xml with binding id's in "target_ids" and finds the corresponding object id's'''
    with open(xml_file, 'r') as file:
        xml_content = file.read()

    pattern = r'<binding ID="(\d+)">(.*?)</binding>'
    binding_matches = re.findall(pattern, xml_content, re.DOTALL)

    for match in binding_matches:
        binding_id, binding_content = match
        if binding_id == target_id:
            deleted_binding = f'<binding ID="{binding_id}">{binding_content}</binding>'
            objectid_match = re.search(r'objectid="(\d+)"', binding_content)
            objectID = objectid_match.group(1)

    with open('deletedBindings.txt', 'w') as file:
        file.write(f"{deleted_binding}\n")

    return objectID, deleted_binding

def find_and_copy_dataobjects(datasource_file, target_ids):
    '''Finds all datasource dataobjects with objectid in "target_ids" and copys them'''
    with open(datasource_file, 'r') as file:
        datasource_content = file.read()

    pattern = r'<dataobject id="(\d+)"(.*?)</dataobject>'
    dataobject_matches = re.findall(pattern, datasource_content, re.DOTALL)

    deleted_dataobjects = []

    for match in dataobject_matches:
        dataobject_id, dataobject_content = match
        if dataobject_id in target_ids:
            deleted_dataobjects.append(f"<dataobject id=\"{dataobject_id}\"{dataobject_content}")
            # Extract the PointRefPointName
            point_name_match = re.search(r'<property name="PointRefPointName">(.*?)</property>', dataobject_content)
            if point_name_match:
                point_name = point_name_match.group(1)
                print(f"Deleted dataobject ID: {dataobject_id}\tPointFefPointName: {point_name}")

    with open('deletedDataS.txt', 'w') as file:
        for dataobject in deleted_dataobjects:
            file.write(f"{dataobject}\n")

    return len(deleted_dataobjects)

def get_point_name(datasource_file, target_id):
    '''Removes datasource dataobjects with objectid in "target_ids" and saves their '''
    with open(datasource_file, 'r') as file:
        datasource_content = file.read()

    pattern = r'<dataobject id="(\d+)"(.*?)</dataobject>'
    dataobject_matches = re.findall(pattern, datasource_content, re.DOTALL)


    for match in dataobject_matches:
        dataobject_id, dataobject_content = match
        if dataobject_id == target_id:
            deleted_dataobject = f"<dataobject id=\"{dataobject_id}\"{dataobject_content}</dataobject>"
            # Extract the PointRefPointName
            point_name_match = re.search(r'<property name="PointRefPointName">(.*?)</property>', dataobject_content)
            if point_name_match:
                point_name = point_name_match.group(1)

    with open('deletedDataS.txt', 'w') as file:
        file.write(f"{deleted_dataobject}\n")

    return point_name, deleted_dataobject

def insert_relinquish_script(file_path, string):
    with open(file_path, 'r') as file:
        file_content = file.readlines()

    for i, line in enumerate(file_content):
        if '<BODY' in line:
            file_content[i] = line.lstrip()  # Remove leading whitespace
            file_content.insert(i, string + '\n')
            break

    with open(file_path, 'w') as file:
        file.writelines(file_content)

def replace_string_in_file(file_path, old_string, new_string):
    with open(file_path, 'r') as file:
        file_content = file.read()

    # Replace the old string with the new string
    updated_content = file_content.replace(old_string, new_string)

    with open(file_path, 'w') as file:
        file.write(updated_content)

# shape_name = 'shape033'
# display_name = '2m-ahu2'
# left = 601
# top = 492
# pointName = '2M-AHU2-CV'
# HDXids = [52, 54]

def get_relinquish(shape_name, pointName, HDXids, DOids, left, top, display_file):
    '''Gets the string sections that correspond to the relinquish control element and embedds the relevant information'''

    relinquish_script_string = f'''
	<SCRIPT language=VBScript for={shape_name}_relinquish_group defer event=onclick>on error resume next
	{shape_name}_RelinquishControl.value = 1</SCRIPT>
	<SCRIPT language=VBScript for={shape_name}_ModeState defer event=onupdate>on error resume next
	if me.value <> "Auto" then
		{shape_name}_relinquish_group.style.visibility = "visible"
	else
		{shape_name}_relinquish_group.style.visibility = "hidden"
	end if</SCRIPT>
	'''
    r_slash = r"\r"
    relinquish_body_string = f'''
    <DIV tabIndex=-1 id={shape_name} class=hsc.shape.1 
    style="FONT-SIZE: 0px; TEXT-DECORATION: none; HEIGHT: 18px; FONT-FAMILY: Arial; WIDTH: 16px; POSITION: absolute; FONT-WEIGHT: 400; FONT-STYLE: normal; LEFT: {left}; TOP: {top}; BEHAVIOR: url(#HSCShapeLinkBehavior) url(#HDXVectorFactory#shapelink)" 
    hdxproperties="fillColorBlink:False;Height:18;lineColorBlink:False;Width:16;" 
    value = "1" src = ".\{display_file}_files{r_slash}elinquish_control.sha" parameters = 
    "Point?PointName:{pointName};" linkType = "embedded" globalscripts = "" 
    styleClass = "">
    <DIV tabIndex=-1 id={shape_name}_relinquish_group class=hvg.group.1 
    style="FONT-SIZE: 0pt; HEIGHT: 100%; WIDTH: 100%; POSITION: absolute; LEFT: 0%; TOP: 0%; BEHAVIOR: url(#HDXVectorFactory#group); VISIBILITY: hidden" 
    hdxproperties="fillColorBlink:False;Height:18;lineColorBlink:False;Width:16;"><TEXTAREA tabIndex=0 id={shape_name}_ModeState class=hsc.alpha.1 style="BORDER-TOP-STYLE: none; OVERFLOW: hidden; WORD-WRAP: normal; FONT-SIZE: 12pt; TEXT-DECORATION: none; HEIGHT: 100%; FONT-FAMILY: Arial; WIDTH: 100%; BORDER-BOTTOM-STYLE: none; POSITION: absolute; FONT-WEIGHT: 400; COLOR: #000000; FONT-STYLE: normal; TEXT-ALIGN: center; BORDER-RIGHT-STYLE: none; LEFT: 0%; BORDER-LEFT-STYLE: none; TOP: 0%; BEHAVIOR: url(#HDXAlphaBehavior) url(#BindingBehavior); VISIBILITY: hidden; BACKGROUND-COLOR: transparent; ROWS: 1" hdxproperties="fillColor:transparent;HDXBINDINGID:{HDXids[0]};lineColor:black;numericDisplayFormat:%.2f;textColor:#000000;">9999.99</TEXTAREA><TEXTAREA tabIndex=0 id={shape_name}_RelinquishControl class=hsc.alpha.1 style="BORDER-TOP-STYLE: none; OVERFLOW: hidden; WORD-WRAP: normal; FONT-SIZE: 12pt; TEXT-DECORATION: none; HEIGHT: 100%; FONT-FAMILY: Arial; WIDTH: 100%; BORDER-BOTTOM-STYLE: none; POSITION: absolute; FONT-WEIGHT: 400; COLOR: #000000; FONT-STYLE: normal; TEXT-ALIGN: center; BORDER-RIGHT-STYLE: none; LEFT: 0%; BORDER-LEFT-STYLE: none; TOP: 0%; BEHAVIOR: url(#HDXAlphaBehavior) url(#BindingBehavior); VISIBILITY: hidden; BACKGROUND-COLOR: transparent; ROWS: 1" hdxproperties="fillColor:transparent;HDXBINDINGID:{HDXids[1]};lineColor:black;numericDisplayFormat:%.2f;textColor:#000000;">9999.99</TEXTAREA>
    <DIV tabIndex=-1 id={shape_name}_relinquish_icon class=hsc.image.1 
    style="OVERFLOW: hidden; FONT-SIZE: 12pt; TEXT-DECORATION: none; HEIGHT: 100%; FONT-FAMILY: Arial; WIDTH: 100%; POSITION: absolute; FONT-WEIGHT: 400; FONT-STYLE: normal; LEFT: 0%; TOP: 0%; BEHAVIOR: url(#HDXVectorFactory#image)"
    hdxproperties="fillColorBlink:False;Height:18;lineColorBlink:False;Src:.\{display_file}_files{r_slash}elinquish_control_files{r_slash}elinquish_button.JPG;Width:16;" 
    shapesrc=".\{display_file}_files{r_slash}elinquish_control_files{r_slash}elinquish_button.JPG"></DIV></DIV></DIV>
	'''

    MS_relinquish_binding = f'''<binding ID="{HDXids[0]}"><dataobject ID="dso1" objectmodelid="datasource1" objecttype="HMIPage.Generic" objectid="{DOids[0]}"/><class ID="HSC.Alpha" refcount="1"/></binding>'''
    RC_relinquish_binding = f'''<binding ID="{HDXids[1]}"><dataobject ID="dso1" objectmodelid="datasource1" objecttype="HMIPage.Generic" objectid="{DOids[1]}"/><class ID="HSC.Alpha" refcount="1"/></binding>'''

    MS_relinquish_dataS = f'''<dataobject id="{DOids[0]}" type="HMIPage.Generic" format="propertybag"><property name="AddressFlags">0</property><property name="AddressType">0</property><property name="CalloutElement"></property><property name="ObjectType">0</property><property name="ParameterFormat">0</property><property name="PointRefFlags">0</property><property name="PointRefParamName">ModeState</property><property name="PointRefParamOffset">0</property><property name="PointRefPointName">{pointName}</property><property name="PresentationType">0</property><property name="SecurityLevel">2</property><property name="UpdatePeriod">0</property><property name="version">1.3</property></dataobject>'''
    RC_relinquish_dataS = f'''<dataobject id="{DOids[1]}" type="HMIPage.Generic" format="propertybag"><property name="AddressFlags">0</property><property name="AddressType">0</property><property name="CalloutElement"></property><property name="ObjectType">0</property><property name="ParameterFormat">0</property><property name="PointRefFlags">0</property><property name="PointRefParamName">RelinquishControl</property><property name="PointRefParamOffset">0</property><property name="PointRefPointName">{pointName}</property><property name="PresentationType">0</property><property name="SecurityLevel">3</property><property name="UpdatePeriod">0</property><property name="version">1.3</property></dataobject>'''

    return relinquish_script_string, relinquish_body_string, MS_relinquish_binding, RC_relinquish_binding, MS_relinquish_dataS, RC_relinquish_dataS

def get_auto_box(shape_name, pointName, HDXids, DOids, left, top, display_file):
    auto_box_body = f'''
    <DIV tabIndex=-1 id={shape_name} class="hsc.shape.1 hsc.shapeanimation.1" 
    style="FONT-SIZE: 0px; TEXT-DECORATION: none; HEIGHT: 16px; FONT-FAMILY: Arial; WIDTH: 24px; POSITION: absolute; FONT-WEIGHT: 400; FONT-STYLE: normal; LEFT: {left}; TOP: {top}; BEHAVIOR: url(#HSCShapeLinkBehavior) url(#HSCShapeLinkBehavior#shapelinkanimator) url(#HDXFaceplateBehavior) url(#HDXVectorFactory#shapelink) url(#BindingBehavior)" 
    hdxproperties="fillColorBlink:False;HDXBINDINGID:{HDXids[0]};Height:16;lineColorBlink:False;Width:24;" 
    value = "1" src = ".\{display_file}_files\MBS_Hand-24Apr.sha" parameters = "" linkType 
    = "embedded" globalscripts = "" styleClass = "" numberOfShapesAnimated = "2">
	<DIV tabIndex=-1 id={shape_name}_textbox002 class=hvg.textbox.1 
	style="OVERFLOW: hidden; FONT-SIZE: 8pt; HEIGHT: 100%; FONT-FAMILY: Tw Cen MT Condensed; WIDTH: 100%; POSITION: absolute; FONT-WEIGHT: normal; COLOR: #c0c0c0; FONT-STYLE: normal; TEXT-ALIGN: center; LEFT: 0%; TOP: 0%; BEHAVIOR: url(#HDXVectorFactory#text)" 
	hdxproperties="FillColor:#808080;fillColorBlink:False;FillStyle:0;Height:16;lineColorBlink:False;LineStyle:0;textColor:#c0c0c0;textColorBlink:False;TotalRotation:0;Width:24;" 
	HDX_LOCK="-1">Auto</DIV></DIV>
    '''
    
    auto_box_binding = f'''<binding ID="{HDXids[0]}"><dataobject ID="dso1" objectmodelid="datasource1" objecttype="HMIPage.Generic" objectid="{DOids[0]}"/><class ID="HSC.Shapelink" refcount="1"/></binding>'''

    auto_box_dataS = f'''<dataobject id="{DOids[0]}" type="HMIPage.Generic" format="propertybag"><property name="AddressFlags">1</property><property name="AddressType">0</property><property name="CalloutElement"></property><property name="ObjectType">0</property><property name="ParameterFormat">0</property><property name="PointRefFlags">0</property><property name="PointRefParamName">ModeState</property><property name="PointRefParamOffset">0</property><property name="PointRefPointName">{pointName}</property><property name="PresentationType">0</property><property name="SecurityLevel">0</property><property name="UpdatePeriod">0</property><property name="version">1.3</property></dataobject>'''

    return auto_box_body, auto_box_binding, auto_box_dataS


# Example usage
# html_file = 'checkingChanges2/afterChange.htm'
# info = extract_and_copy_checkboxes(html_file)
# print(f"{len(info)} Checkbox elements extracted and removed. Deleted elements saved in deletedElements.txt.")

# HDXIDs = [item[2] for item in info]
# bindingFile = 'checkingChanges2/afterChangeBindings.xml'
# objectIDs = find_and_copy_bindings(bindingFile, HDXIDs)

# datasourceFile = 'checkingChanges2/afterChangeDS.dsd'
# objectsFound = find_and_copy_dataobjects(datasourceFile, objectIDs)

# # Example usage
# xml_file = 'checkingChanges2/afterChangeBindings.xml'  # Replace with your XML binding file
# next_free_id = find_next_free_binding_id(xml_file)
# print(f"The next free binding ID is: {next_free_id}")