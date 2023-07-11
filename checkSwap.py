import re

filePath = 'abstract_BH/2m-ahu1.htm'

# Read the input HTML file
with open(filePath, 'r') as file:
    html_content = file.read()

# Define the replacement code
replacement_code = '''
<DIV tabIndex=-1 id=shape064 class="hsc.shape.1 hsc.shapeanimation.1"
style="FONT-SIZE: 0px; TEXT-DECORATION: none; HEIGHT: 16px; FONT-FAMILY: Arial; WIDTH: 24px; POSITION: absolute; FONT-WEIGHT: 400; FONT-STYLE: normal; LEFT: 318px; TOP: 471px; BEHAVIOR: url(#HSCShapeLinkBehavior) url(#HSCShapeLinkBehavior#shapelinkanimator) url(#HDXFaceplateBehavior) url(#HDXVectorFactory#shapelink) url(#BindingBehavior)"
hdxproperties="fillColorBlink:False;HDXBINDINGID:26;Height:16;lineColorBlink:False;Width:24;"
value = "1" src = ".\2m-ahu1_files\MBS_Hand-24Apr.sha" parameters = "" linkType
= "embedded" globalscripts = "" styleClass = "" numberOfShapesAnimated = "2">
<DIV tabIndex=-1 id=shape064_textbox002 class=hvg.textbox.1
style="OVERFLOW: hidden; FONT-SIZE: 8pt; HEIGHT: 100%; FONT-FAMILY: Tw Cen MT Condensed; WIDTH: 100%; POSITION: absolute; FONT-WEIGHT: normal; COLOR: #c0c0c0; FONT-STYLE: normal; TEXT-ALIGN: center; LEFT: 0%; TOP: 0%; BEHAVIOR: url(#HDXVectorFactory#text)"
HDX_LOCK="-1"
hdxproperties="FillColor:#808080;fillColorBlink:False;FillStyle:0;Height:16;lineColorBlink:False;LineStyle:0;textColor:#c0c0c0;textColorBlink:False;TotalRotation:0;Width:24;">Auto</DIV></DIV>
<DIV tabIndex=-1 id=shape036 class=hsc.shape.1
style="FONT-SIZE: 0px; TEXT-DECORATION: none; HEIGHT: 18px; FONT-FAMILY: Arial; WIDTH: 16px; POSITION: absolute; FONT-WEIGHT: 400; FONT-STYLE: normal; LEFT: 422px; TOP: 470px; BEHAVIOR: url(#HSCShapeLinkBehavior) url(#HDXVectorFactory#shapelink)"
hdxproperties="fillColorBlink:False;Height:18;lineColorBlink:False;Width:16;"
value = "1" src = ".\2m-ahu1_files\relinquish_control.sha" parameters =
"Point?PointName:2M-AHU1-FAN-SPD;" linkType = "embedded" globalscripts = ""
styleClass = "">
<DIV tabIndex=-1 id=shape036_relinquish_group class=hvg.group.1
style="FONT-SIZE: 0pt; HEIGHT: 100%; WIDTH: 100%; POSITION: absolute; LEFT: 0%; TOP: 0%; BEHAVIOR: url(#HDXVectorFactory#group); VISIBILITY: hidden"
hdxproperties="fillColorBlink:False;Height:18;lineColorBlink:False;Width:16;"><TEXTAREA tabIndex=0 id=shape036_ModeState class=hsc.alpha.1 style="BORDER-TOP-STYLE: none; OVERFLOW: hidden; WORD-WRAP: normal; FONT-SIZE: 12pt; TEXT-DECORATION: none; HEIGHT: 100%; FONT-FAMILY: Arial; WIDTH: 100%; BORDER-BOTTOM-STYLE: none; POSITION: absolute; FONT-WEIGHT: 400; COLOR: #000000; FONT-STYLE: normal; TEXT-ALIGN: center; BORDER-RIGHT-STYLE: none; LEFT: 0%; BORDER-LEFT-STYLE: none; TOP: 0%; BEHAVIOR: url(#HDXAlphaBehavior) url(#BindingBehavior); VISIBILITY: hidden; BACKGROUND-COLOR: transparent; ROWS: 1" hdxproperties="fillColor:transparent;HDXBINDINGID:51;lineColor:black;numericDisplayFormat:%.2f;textColor:#000000;">9999.99</TEXTAREA><TEXTAREA tabIndex=0 id=shape036_RelinquishControl class=hsc.alpha.1 style="BORDER-TOP-STYLE: none; OVERFLOW: hidden; WORD-WRAP: normal; FONT-SIZE: 12pt; TEXT-DECORATION: none; HEIGHT: 100%; FONT-FAMILY: Arial; WIDTH: 100%; BORDER-BOTTOM-STYLE: none; POSITION: absolute; FONT-WEIGHT: 400; COLOR: #000000; FONT-STYLE: normal; TEXT-ALIGN: center; BORDER-RIGHT-STYLE: none; LEFT: 0%; BORDER-LEFT-STYLE: none; TOP: 0%; BEHAVIOR: url(#HDXAlphaBehavior) url(#BindingBehavior); VISIBILITY: hidden; BACKGROUND-COLOR: transparent; ROWS: 1" hdxproperties="fillColor:transparent;HDXBINDINGID:54;lineColor:black;numericDisplayFormat:%.2f;textColor:#000000;">9999.99</TEXTAREA>
<DIV tabIndex=-1 id=shape036_relinquish_icon class=hsc.image.1
style="OVERFLOW: hidden; FONT-SIZE: 12pt; TEXT-DECORATION: none; HEIGHT: 100%; FONT-FAMILY: Arial; WIDTH: 100%; POSITION: absolute; FONT-WEIGHT: 400; FONT-STYLE: normal; LEFT: 0%; TOP: 0%; BEHAVIOR: url(#HDXVectorFactory#image)"
shapesrc=".\2m-ahu1_files\relinquish_control_files\relinquish_button.JPG"
hdxproperties="fillColorBlink:False;Height:18;lineColorBlink:False;Src:.\2m-ahu1_files\relinquish_control_files\relinquish_button.JPG;Width:16;"></DIV></DIV></DIV>
'''

# Find checkbox elements using regex pattern
pattern = r'<SPAN\s+tabIndex=-1\s+id=checkbox\d+\s+class=hsc\.checkbox\.1[^>]+>\s*<INPUT[^>]+>\s*<SPAN[^>]+>Checkbox<\/SPAN>\s*<\/SPAN>'
checkboxes = re.findall(pattern, html_content)

# Replace checkbox elements with the replacement code
for checkbox in checkboxes:
    html_content = html_content.replace(checkbox, replacement_code)

# Write the updated HTML content to a new file
with open('output.html', 'w') as file:
    file.write(html_content)