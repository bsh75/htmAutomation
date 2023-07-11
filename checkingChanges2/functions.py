import xml.etree.ElementTree as ET
from bs4 import BeautifulSoup
import re

def find_next_free_binding_id(xml_file):
    # Parse the XML file
    tree = ET.parse(xml_file)
    root = tree.getroot()

    # Extract the binding IDs from the XML
    binding_ids = [int(binding.attrib['ID']) for binding in root.findall('binding')]

    # Find the maximum binding ID
    max_id = max(binding_ids) if binding_ids else -1

    # Determine the next free binding ID
    next_id = max_id + 1

    return next_id

def find_checkbox_elements(html_content):
    pattern = r'<SPAN[^>]*class=hsc\.checkbox[^>]*>.*?Checkbox</SPAN></SPAN>'
    checkbox_matches = re.findall(pattern, html_content, re.DOTALL)
    return checkbox_matches

def extract_checkbox_info(checkbox_content):
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

def find_and_copy_dataobjects(datasource_file, target_ids):
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


# shape_name = 'shape033'
# display_name = '2m-ahu2'
# left = 601
# top = 492
# PointRefPointName = '2M-AHU2-CV'
# HDXids = [52, 54]

def get_relinquish(shape_name, PointRefPointName, HDXids, left, top, display_name):
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
	relinquish_body_string = f'''
	<DIV tabIndex=-1 id={shape_name} class=hsc.shape.1 
	style="FONT-SIZE: 0px; TEXT-DECORATION: none; HEIGHT: 18px; FONT-FAMILY: Arial; WIDTH: 16px; POSITION: absolute; FONT-WEIGHT: 400; FONT-STYLE: normal; LEFT: {left}; TOP: {top}; BEHAVIOR: url(#HSCShapeLinkBehavior) url(#HDXVectorFactory#shapelink)" 
	hdxproperties="fillColorBlink:False;Height:18;lineColorBlink:False;Width:16;" 
	value = "1" src = ".\{display_name}_files\relinquish_control.sha" parameters = 
	"Point?PointName:{PointRefPointName};" linkType = "embedded" globalscripts = "" 
	styleClass = "">
		<DIV tabIndex=-1 id={shape_name}_relinquish_group class=hvg.group.1 
		style="FONT-SIZE: 0pt; HEIGHT: 100%; WIDTH: 100%; POSITION: absolute; LEFT: 0%; TOP: 0%; BEHAVIOR: url(#HDXVectorFactory#group); VISIBILITY: hidden" 
		hdxproperties="fillColorBlink:False;Height:18;lineColorBlink:False;Width:16;">
		
		<TEXTAREA tabIndex=0 id={shape_name}_ModeState class=hsc.alpha.1 style="BORDER-TOP-STYLE: none; OVERFLOW: hidden; WORD-WRAP: normal; FONT-SIZE: 12pt; TEXT-DECORATION: none; HEIGHT: 100%; FONT-FAMILY: Arial; WIDTH: 100%; BORDER-BOTTOM-STYLE: none; POSITION: absolute; FONT-WEIGHT: 400; COLOR: #000000; FONT-STYLE: normal; TEXT-ALIGN: center; BORDER-RIGHT-STYLE: none; LEFT: 0%; BORDER-LEFT-STYLE: none; TOP: 0%; BEHAVIOR: url(#HDXAlphaBehavior) url(#BindingBehavior); VISIBILITY: hidden; BACKGROUND-COLOR: transparent; ROWS: 1" hdxproperties="fillColor:transparent;HDXBINDINGID:{HDXids[0]};lineColor:black;numericDisplayFormat:%.2f;textColor:#000000;">9999.99</TEXTAREA>
		
		<TEXTAREA tabIndex=0 id={shape_name}_RelinquishControl class=hsc.alpha.1 style="BORDER-TOP-STYLE: none; OVERFLOW: hidden; WORD-WRAP: normal; FONT-SIZE: 12pt; TEXT-DECORATION: none; HEIGHT: 100%; FONT-FAMILY: Arial; WIDTH: 100%; BORDER-BOTTOM-STYLE: none; POSITION: absolute; FONT-WEIGHT: 400; COLOR: #000000; FONT-STYLE: normal; TEXT-ALIGN: center; BORDER-RIGHT-STYLE: none; LEFT: 0%; BORDER-LEFT-STYLE: none; TOP: 0%; BEHAVIOR: url(#HDXAlphaBehavior) url(#BindingBehavior); VISIBILITY: hidden; BACKGROUND-COLOR: transparent; ROWS: 1" hdxproperties="fillColor:transparent;HDXBINDINGID:{HDXids[1]};lineColor:black;numericDisplayFormat:%.2f;textColor:#000000;">9999.99</TEXTAREA>
		
			<DIV tabIndex=-1 id={shape_name}_relinquish_icon class=hsc.image.1 
			style="OVERFLOW: hidden; FONT-SIZE: 12pt; TEXT-DECORATION: none; HEIGHT: 100%; FONT-FAMILY: Arial; WIDTH: 100%; POSITION: absolute; FONT-WEIGHT: 400; FONT-STYLE: normal; LEFT: 0%; TOP: 0%; BEHAVIOR: url(#HDXVectorFactory#image)" 
			hdxproperties="fillColorBlink:False;Height:18;lineColorBlink:False;Src:.\2m-ahu2_files\relinquish_control_files\relinquish_button.JPG;Width:16;" 
			shapesrc=".\{display_name}_files\relinquish_control_files\relinquish_button.JPG"></DIV>
		</DIV>
	</DIV>
	'''
	return relinquish_script_string, relinquish_body_string

# Example usage
html_file = 'checkingChanges2/afterChange.htm'
info = extract_and_copy_checkboxes(html_file)
print(f"{len(info)} Checkbox elements extracted and removed. Deleted elements saved in deletedElements.txt.")

HDXIDs = [item[2] for item in info]
bindingFile = 'checkingChanges2/afterChangeBindings.xml'
objectIDs = find_and_copy_bindings(bindingFile, HDXIDs)

datasourceFile = 'checkingChanges2/afterChangeDS.dsd'
objectsFound = find_and_copy_dataobjects(datasourceFile, objectIDs)

for element in info
# # Example usage
# xml_file = 'checkingChanges2/afterChangeBindings.xml'  # Replace with your XML binding file
# next_free_id = find_next_free_binding_id(xml_file)
# print(f"The next free binding ID is: {next_free_id}")