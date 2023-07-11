shape_name = 'shape033'
display_name = '2m-ahu2'

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

left = 601
top = 492
PointRefPointName = '2M-AHU2-CV'
HDXids = [52, 54]

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