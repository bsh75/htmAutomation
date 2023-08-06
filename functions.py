import xml.etree.ElementTree as ET
import re
import shutil
import os

def extract_checkbox_id(checkbox_element):
    # Extract the id attribute value using regular expression
    id_match = re.search(r'id=([^ ]+)', checkbox_element)

    if id_match:
        id_value = id_match.group(1)
        return id_value
    else:
        return None

def find_next_three_binding_ids(xml_content):
    '''This should find the next two available binding ids for the new element'''
    # Parse the XML content
    root = ET.fromstring(xml_content)

    # Extract the binding IDs from the XML, ignoring non-integer 'ID' attributes
    binding_ids = []
    for binding in root.findall('binding'):
        binding_id_str = binding.attrib.get('ID')
        if binding_id_str is not None:
            try:
                binding_id = int(binding_id_str)
                binding_ids.append(binding_id)
            except ValueError:
                pass  # Ignore non-integer 'ID' attributes

    # Find the maximum binding ID
    max_id = max(binding_ids) if binding_ids else -1

    # Determine the next free binding ID
    next_ids = [max_id + 1, max_id + 2, max_id + 3]

    return next_ids

def find_next_three_object_ids(datasource_content):
    '''This should find the next two available maximum object ids for the new element'''
    dataobject_ids = re.findall(r'<dataobject id="(\d+)"', datasource_content)
    dataobject_ids = [int(id) for id in dataobject_ids]

    max_id = max(dataobject_ids) if dataobject_ids else 0
    next_available_ids = [max_id + 1, max_id + 2, max_id + 3]

    return next_available_ids

def find_next_available_shape_number(file_content):
    '''Finds the next 2 available shape numbers for auto and relinquish shapes'''
    pattern = r'shape(\d{3})'
    shape_numbers = [int(match.group(1)) for match in re.finditer(pattern, file_content)]
    
    # Find the next available number that is not present in the file
    for i in range(1, 1000):
        if i not in shape_numbers:
            next_number_formatted = f"{i:03}"  # Format the number with 3 digits
            return f"shape{next_number_formatted}"
    
    return None  # Return None if all possible numbers are taken

def find_next_available_shape_numbers(file_content):
    pattern = r'shape(\d{3})'
    shape_numbers = [int(match.group(1)) for match in re.finditer(pattern, file_content)]

    next_numbers = []
    # Find the next available numbers that are not present in the file
    for i in range(1, 1000):
        if i not in shape_numbers:
            next_number_formatted = f"{i:03}"  # Format the number with 3 digits
            next_numbers.append(f"shape{next_number_formatted}")
            if len(next_numbers) == 2:
                break

    return next_numbers[0], next_numbers[1]

def find_checkbox_elements(html_content):
    '''Finds all the check box elements and returns a list of them'''
    pattern = r'<SPAN[^>]*class=hsc\.checkbox[^>]*>.*?Checkbox</SPAN></SPAN>'
    checkbox_matches = re.findall(pattern, html_content, re.DOTALL)
    return checkbox_matches

def find_patterns_with_bindingIDs(hdx_binding_ids, html_content):
    pattern_textarea = r'<TEXTAREA\s+id=alpha\d+\s+[^>]* LEFT: ([\d.]+)(%|px)[^>]* TOP: ([\d.]+)(%|px)[^>]*HDXBINDINGID:(\d+)[^>]*>[^>]*</TEXTAREA>'
    pattern_textarea2 = r'<TEXTAREA\s+[^>]* TOP: ([\d.]+)(%|px)[^>]* LEFT: ([\d.]+)(%|px)[^>]*id=alpha\d+\s+[^>]*HDXBINDINGID:(\d+)[^>]*>[^>]*</TEXTAREA>'
    pattern_combobox = r'<SPAN\s+id=combobox\d+\s+[^>]* LEFT: ([\d.]+)(%|px)[^>]* TOP: ([\d.]+)(%|px)[^>]*HDXBINDINGID:(\d+)[^>]*>[^>]*</SPAN>'

    matches_textarea = re.findall(pattern_textarea, html_content, re.DOTALL)
    matches_textarea2 = re.findall(pattern_textarea2, html_content, re.DOTALL)
    matches_combobox = re.findall(pattern_combobox, html_content, re.DOTALL)

    # print(matches_textarea)
    # print(matches_combobox)

    found_patterns = []
    for match in matches_textarea:
        # print(f"MATCH: {match}")
        left_value, left_unit, top_value, top_unit, binding_id = match
        if binding_id in hdx_binding_ids:
            found_patterns.append([left_value+left_unit, top_value+top_unit, 'Auto'])
    
    for match in matches_textarea2:
        # print(f"MATCH: {match}")
        top_value, top_unit, left_value, left_unit,  binding_id = match
        if binding_id in hdx_binding_ids:
            found_patterns.append([left_value+left_unit, top_value+top_unit, 'Auto'])

    for match in matches_combobox:
        # print(f"MATCH: {match}")
        left_value, left_unit, top_value, top_unit, binding_id = match
        if binding_id in hdx_binding_ids:
            found_patterns.append([left_value+left_unit, top_value+top_unit, 'Combo'])
    if len(found_patterns) > 1:
        return None
    else:
        return found_patterns
    
def find_patterns_with_bindingIDs2(hdx_binding_ids, html_content):
    pattern_textarea = r'<TEXTAREA[^>]*id=alpha\d+\s+[^>]*HDXBINDINGID:\d[^>]*>[^>]*</TEXTAREA>'
    pattern_combobox = r'<SPAN[^>]*class=hsc.combo[^>]*HDXBINDINGID:\d[^>]*>[^>]*</SPAN>'

    matches_textarea = re.findall(pattern_textarea, html_content, re.DOTALL)
    matches_combobox = re.findall(pattern_combobox, html_content, re.DOTALL)
    # print(matches_textarea, matches_combobox)
    pattern_HDX = r'[^>]*HDXBINDINGID:(\d+)[^>]*'
    pattern_left = r'[^>]*\s+LEFT:\s+([\d.]+)(%|px)[^>]*'
    pattern_top = r'[^>]*\s+TOP:\s+([\d.]+)(%|px)[^>]*'
    # print(matches_textarea)
    # print(matches_combobox)

    found_patterns = []
    for match in matches_textarea:
        HDX_id = re.findall(pattern_HDX, match)
        # print(f"HDX_id in pattern: {HDX_id}")
        if HDX_id[0] in hdx_binding_ids:
            # print("Match found")
            left_value, left_unit = re.findall(pattern_left, match, re.DOTALL)[0]
            top_value, top_unit = re.findall(pattern_top, match, re.DOTALL)[0]
            # print(left_value, left_unit, top_value, top_unit)
            if (left_unit == 'px') and (top_unit == 'px'): 
                found_patterns.append([left_value+left_unit, top_value+top_unit, 'Auto'])

    for match in matches_combobox:
        HDX_id = re.findall(pattern_HDX, match)
        if HDX_id[0] in hdx_binding_ids:
            # print("Match found")
            left_value, left_unit = re.findall(pattern_left, match, re.DOTALL)[0]
            top_value, top_unit = re.findall(pattern_top, match, re.DOTALL)[0]
            # print(left_value, left_unit, top_value, top_unit)
            if (left_unit == 'px') and (top_unit == 'px'): 
                found_patterns.append([left_value+left_unit, top_value+top_unit, 'Auto'])
    
    return found_patterns

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

def adjust_position(position, amount):
    if position.endswith('px'):
        position_value = int(position[:-2])
        adjusted_value = position_value + amount
        adjusted_position = f"{adjusted_value}px"
    elif position.endswith('%'):
        position_value = float(position[:-1])
        adjusted_value = position_value + amount
        adjusted_position = f"{adjusted_value:.2f}%"
    else:
        # Invalid position format, return the original position
        return position
    
    return adjusted_position

def find_objectID(xml_content, target_id):
    '''Copys all the bindings from xml with binding id's in "target_ids" and finds the corresponding object id's'''
    pattern = r'<binding ID="(\d+)">(.*?)</binding>'
    binding_matches = re.findall(pattern, xml_content, re.DOTALL)
    for match in binding_matches:
        binding_id, binding_content = match
        # print(binding_id)
        if binding_id == target_id:
            deleted_binding = f'<binding ID="{binding_id}">{binding_content}</binding>'
            objectid_match = re.search(r'objectid="(\d+)"', binding_content)
            objectID = objectid_match.group(1)

    return objectID, deleted_binding

def find_binding_IDs(xml_content, object_ids):
    '''Copies all the bindings from xml with binding id's in "target_ids" and finds the corresponding object id's'''
    pattern = r'<binding ID="(\d+)">(.*?)</binding>'
    binding_matches = re.findall(pattern, xml_content, re.DOTALL)
    found_binding_IDs = []
    for match in binding_matches:
        binding_id, binding_content = match
        objectid_match = re.search(r'objectid="(\d+)"', binding_content)
        if objectid_match:
            objectID = objectid_match.group(1)
            if int(objectID) in object_ids:
                found_binding_IDs.append(binding_id)

    return found_binding_IDs

def get_point_name(datasource_content, target_id):
    '''Removes datasource dataobjects with objectid in "target_ids" and saves their '''
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
    return point_name, deleted_dataobject

def get_dataobject_ids_by_point_name(datasource_content, point_name):
    '''Finds all dataobject IDs with a given point_name in the datasource_content'''
    pattern = r'<dataobject id="(\d+)"(.*?)</dataobject>'
    dataobject_matches = re.findall(pattern, datasource_content, re.DOTALL)

    matching_ids = []
    for match in dataobject_matches:
        dataobject_id, dataobject_content = match

        # Extract the PointRefPointName
        point_name_match = re.search(r'<property name="PointRefPointName">(.*?)</property>', dataobject_content)
        if point_name_match:
            found_point_name = point_name_match.group(1)
            if found_point_name == point_name:
                matching_ids.append(int(dataobject_id))

    return matching_ids

def insert_relinquish_script(file_content, string):
    '''Inserts the relinquish control script at top of file'''
    for i, line in enumerate(file_content):
        if '<BODY' in line:
            file_content[i] = line.lstrip()  # Remove leading whitespace
            file_content.insert(i, string + '\n')
            break

    return file_content

def copy_folder(source_folder, destination_folder):
    try:
        # Extract the base folder name from the source path
        folder_name = os.path.basename(source_folder)
        
        # Create a new folder in the destination with the same name as the source folder
        destination_folder_path = os.path.join(destination_folder, folder_name)
        shutil.copytree(source_folder, destination_folder_path)
        
        print(f"Folder '{source_folder}' copied to '{destination_folder_path}' successfully.")
    except FileNotFoundError:
        print(f"Error: Source folder '{source_folder}' not found.")
    except FileExistsError:
        print(f"Error: Destination folder '{destination_folder_path}' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

def copy_file(source_file, destination_folder):
    try:
        # Extract the file name from the source path
        file_name = os.path.basename(source_file)

        # Create the destination path by joining the destination folder and the file name
        destination_file = os.path.join(destination_folder, file_name)

        # Copy the file to the destination folder
        shutil.copy(source_file, destination_file)

        print(f"File '{source_file}' copied to '{destination_file}' successfully.")
    except FileNotFoundError:
        print(f"Error: Source file '{source_file}' not found.")
    except FileExistsError:
        print(f"Error: Destination file '{destination_file}' already exists.")
    except Exception as e:
        print(f"An error occurred: {e}")

def find_files_in_folders(starting_directory, filename1, filename2):
    for root, _, files in os.walk(starting_directory):
        if filename1 in files and filename2 in files:
            file1_path = os.path.join(root, filename1)
            file2_path = os.path.join(root, filename2)
            return file1_path, file2_path

    return None, None

def find_folders_in_folders(starting_directory, foldername1, foldername2):
    for root, dirs, _ in os.walk(starting_directory):
        if foldername1 in dirs and foldername2 in dirs:
            folder1_path = os.path.join(root, foldername1)
            folder2_path = os.path.join(root, foldername2)
            return folder1_path, folder2_path

    return None, None

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
	end if</SCRIPT>'''

    r_slash = r"\r"
    relinquish_body_string = f'''
    <DIV tabIndex=-1 id={shape_name} class=hsc.shape.1 
    style="FONT-SIZE: 0px; TEXT-DECORATION: none; HEIGHT: 18px; FONT-FAMILY: Arial; WIDTH: 16px; POSITION: absolute; FONT-WEIGHT: 400; FONT-STYLE: normal; LEFT: {left}; TOP: {top}; BEHAVIOR: url(#HSCShapeLinkBehavior) url(#HDXVectorFactory#shapelink)" 
    hdxproperties="fillColorBlink:False;Height:18;lineColorBlink:False;Width:16;" 
    value = "1" src = ".\{display_file}{r_slash}elinquish_control.sha" parameters = 
    "Point?PointName:{pointName};" linkType = "embedded" globalscripts = "" 
    styleClass = "">
    <DIV tabIndex=-1 id={shape_name}_relinquish_group class=hvg.group.1 
    style="FONT-SIZE: 0pt; HEIGHT: 100%; WIDTH: 100%; POSITION: absolute; LEFT: 0%; TOP: 0%; BEHAVIOR: url(#HDXVectorFactory#group); VISIBILITY: hidden" 
    hdxproperties="fillColorBlink:False;Height:18;lineColorBlink:False;Width:16;"><TEXTAREA tabIndex=0 id={shape_name}_ModeState class=hsc.alpha.1 style="BORDER-TOP-STYLE: none; OVERFLOW: hidden; WORD-WRAP: normal; FONT-SIZE: 12pt; TEXT-DECORATION: none; HEIGHT: 100%; FONT-FAMILY: Arial; WIDTH: 100%; BORDER-BOTTOM-STYLE: none; POSITION: absolute; FONT-WEIGHT: 400; COLOR: #000000; FONT-STYLE: normal; TEXT-ALIGN: center; BORDER-RIGHT-STYLE: none; LEFT: 0%; BORDER-LEFT-STYLE: none; TOP: 0%; BEHAVIOR: url(#HDXAlphaBehavior) url(#BindingBehavior); VISIBILITY: hidden; BACKGROUND-COLOR: transparent; ROWS: 1" hdxproperties="fillColor:transparent;HDXBINDINGID:{HDXids[0]};lineColor:black;numericDisplayFormat:%.2f;textColor:#000000;">9999.99</TEXTAREA><TEXTAREA tabIndex=0 id={shape_name}_RelinquishControl class=hsc.alpha.1 style="BORDER-TOP-STYLE: none; OVERFLOW: hidden; WORD-WRAP: normal; FONT-SIZE: 12pt; TEXT-DECORATION: none; HEIGHT: 100%; FONT-FAMILY: Arial; WIDTH: 100%; BORDER-BOTTOM-STYLE: none; POSITION: absolute; FONT-WEIGHT: 400; COLOR: #000000; FONT-STYLE: normal; TEXT-ALIGN: center; BORDER-RIGHT-STYLE: none; LEFT: 0%; BORDER-LEFT-STYLE: none; TOP: 0%; BEHAVIOR: url(#HDXAlphaBehavior) url(#BindingBehavior); VISIBILITY: hidden; BACKGROUND-COLOR: transparent; ROWS: 1" hdxproperties="fillColor:transparent;HDXBINDINGID:{HDXids[1]};lineColor:black;numericDisplayFormat:%.2f;textColor:#000000;">9999.99</TEXTAREA>
    <DIV tabIndex=-1 id={shape_name}_relinquish_icon class=hsc.image.1 
    style="OVERFLOW: hidden; FONT-SIZE: 12pt; TEXT-DECORATION: none; HEIGHT: 100%; FONT-FAMILY: Arial; WIDTH: 100%; POSITION: absolute; FONT-WEIGHT: 400; FONT-STYLE: normal; LEFT: 0%; TOP: 0%; BEHAVIOR: url(#HDXVectorFactory#image)"
    hdxproperties="fillColorBlink:False;Height:18;lineColorBlink:False;Src:.\{display_file}{r_slash}elinquish_control_files{r_slash}elinquish_button.JPG;Width:16;" 
    shapesrc=".\{display_file}{r_slash}elinquish_control_files{r_slash}elinquish_button.JPG"></DIV></DIV></DIV>'''

    MS_relinquish_binding = f'''<binding ID="{HDXids[0]}"><dataobject ID="dso1" objectmodelid="datasource1" objecttype="HMIPage.Generic" objectid="{DOids[0]}"/><class ID="HSC.Alpha" refcount="1"/></binding>'''
    RC_relinquish_binding = f'''<binding ID="{HDXids[1]}"><dataobject ID="dso1" objectmodelid="datasource1" objecttype="HMIPage.Generic" objectid="{DOids[1]}"/><class ID="HSC.Alpha" refcount="1"/></binding>'''

    MS_relinquish_dataS = f'''<dataobject id="{DOids[0]}" type="HMIPage.Generic" format="propertybag"><property name="AddressFlags">0</property><property name="AddressType">0</property><property name="CalloutElement"></property><property name="ObjectType">0</property><property name="ParameterFormat">0</property><property name="PointRefFlags">0</property><property name="PointRefParamName">ModeState</property><property name="PointRefParamOffset">0</property><property name="PointRefPointName">{pointName}</property><property name="PresentationType">0</property><property name="SecurityLevel">2</property><property name="UpdatePeriod">0</property><property name="version">1.3</property></dataobject>'''
    RC_relinquish_dataS = f'''<dataobject id="{DOids[1]}" type="HMIPage.Generic" format="propertybag"><property name="AddressFlags">0</property><property name="AddressType">0</property><property name="CalloutElement"></property><property name="ObjectType">0</property><property name="ParameterFormat">0</property><property name="PointRefFlags">0</property><property name="PointRefParamName">RelinquishControl</property><property name="PointRefParamOffset">0</property><property name="PointRefPointName">{pointName}</property><property name="PresentationType">0</property><property name="SecurityLevel">3</property><property name="UpdatePeriod">0</property><property name="version">1.3</property></dataobject>'''

    return relinquish_script_string, relinquish_body_string, MS_relinquish_binding, RC_relinquish_binding, MS_relinquish_dataS, RC_relinquish_dataS

def get_auto_box(shape_name, pointName, HDXids, DOids, left, top, display_file):
    auto_box_body = f'''
    <DIV tabIndex=-1 id={shape_name} class="hsc.shape.1 hsc.shapeanimation.1" 
    style="FONT-SIZE: 0px; TEXT-DECORATION: none; HEIGHT: 16px; FONT-FAMILY: Arial; WIDTH: 24px; POSITION: absolute; Z-INDEX: 1; FONT-WEIGHT: 400; FONT-STYLE: normal; LEFT: {left}; TOP: {top}; BEHAVIOR: url(#HSCShapeLinkBehavior) url(#HSCShapeLinkBehavior#shapelinkanimator) url(#HDXFaceplateBehavior) url(#HDXVectorFactory#shapelink) url(#BindingBehavior)" 
    hdxproperties="fillColorBlink:False;HDXBINDINGID:{HDXids[2]};Height:16;lineColorBlink:False;Width:24;" 
    value = "1" src = ".\{display_file}\MBS_Hand-24Apr.sha" parameters = "" linkType 
    = "embedded" globalscripts = "" styleClass = "" numberOfShapesAnimated = "2">
	<DIV tabIndex=-1 id={shape_name}_textbox002 class=hvg.textbox.1 
	style="OVERFLOW: hidden; FONT-SIZE: 8pt; HEIGHT: 100%; FONT-FAMILY: Tw Cen MT Condensed; WIDTH: 100%; POSITION: absolute; Z-INDEX: 1; FONT-WEIGHT: normal; COLOR: #c0c0c0; FONT-STYLE: normal; TEXT-ALIGN: center; LEFT: 0%; TOP: 0%; BEHAVIOR: url(#HDXVectorFactory#text)" 
	hdxproperties="FillColor:#808080;fillColorBlink:False;FillStyle:0;Height:16;lineColorBlink:False;LineStyle:0;textColor:#c0c0c0;textColorBlink:False;TotalRotation:0;Width:24;" 
	HDX_LOCK="-1">Auto</DIV></DIV>'''
    
    auto_box_binding = f'''<binding ID="{HDXids[2]}"><dataobject ID="dso1" objectmodelid="datasource1" objecttype="HMIPage.Generic" objectid="{DOids[2]}"/><class ID="HSC.Shapelink" refcount="1"/></binding>'''

    auto_box_dataS = f'''<dataobject id="{DOids[2]}" type="HMIPage.Generic" format="propertybag"><property name="AddressFlags">1</property><property name="AddressType">0</property><property name="CalloutElement"></property><property name="ObjectType">0</property><property name="ParameterFormat">0</property><property name="PointRefFlags">0</property><property name="PointRefParamName">ModeState</property><property name="PointRefParamOffset">0</property><property name="PointRefPointName">{pointName}</property><property name="PresentationType">0</property><property name="SecurityLevel">0</property><property name="UpdatePeriod">0</property><property name="version">1.3</property></dataobject>'''

    return auto_box_body, auto_box_binding, auto_box_dataS
