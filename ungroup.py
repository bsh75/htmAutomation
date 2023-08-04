import re
import math

from bs4 import BeautifulSoup

def find_grouped_elements(htm_content):
    soup = BeautifulSoup(htm_content, 'html.parser')
    grouped_elements = []

    for div_tag in soup.find_all('div'):
        if div_tag.find('div'):
            # If the current <DIV> tag contains nested <DIV> tags, skip it
            continue

        # Get the content inside the <DIV> tag as a string
        div_content = str(div_tag)

        # Add the content to the list of grouped elements
        grouped_elements.append(div_content)

    return grouped_elements

def extract_group_elements(html_content):
    # Find all opening <DIV> tags with 'tabIndex=-1' and 'id=group' attributes
    opening_div_pattern = r'<DIV[^>]*id='
    opening_div_matches = re.findall(opening_div_pattern, html_content)
    # print(opening_div_matches)
    # Initialize a list to store the extracted group elements
    extracted_group_elements = []
    group_content_list = []

    # Loop through the opening <DIV> matches
    for match in opening_div_matches:
        start_index = html_content.find(match)

        # Initialize a flag to keep track of nested <DIV> elements
        nested_div_flag = 0

        # Find the corresponding closing </DIV> for the current opening <DIV>
        for i in range(start_index, len(html_content)):
            if html_content[i:i+5] == '<DIV ':
                # print("+1: ", nested_div_flag)
                nested_div_flag += 1
            if html_content[i:i+6] == '</DIV>':
                # print("-1: ", nested_div_flag)
                nested_div_flag -= 1
                # Check if we have found the closing </DIV> for the current opening <DIV>
                if nested_div_flag == 0:
                    group_content = html_content[start_index:i+6]
                    # print('\n\n', group_content, '\n\n')
                    if 'id=checkbox' in group_content:
                        group_content_list.append(group_content)
                        elements = group_content + '\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n'
                        extracted_group_elements.append(elements)
                    break

    # Print the number of sections found
    num_sections_found = len(extracted_group_elements)
    # print(f"Number of sections found: {num_sections_found}")

    return group_content_list

def format_for_sub(value, PARAM, unit):
    new_string = f"{PARAM}: {str(value)}{unit}"
    return new_string

def multiple_substitutions(string, list_of_old, list_of_new):
    # Perform substitutions using the lists
    for i in range(len(list_of_old)):
        string = string.replace(list_of_old[i], list_of_new[i])

    return string

def remove_tags(string):
    # Find the index of the first '>' and last '</DIV>'
    first_gt_index = string.find('>') + 1
    last_div_index = string.rfind('</DIV>')

    # Extract the substring between the first '>' and last '</DIV>'
    result = string[first_gt_index:last_div_index]

    return result

def find_single_number(text):
    # The regular expression to find numbers (both integers and floats)
    pattern = r"\b\d+(\.\d+)?\b"

    matches = re.findall(pattern, text)
    if len(matches) == 1:
        return float(matches[0]) if "." in matches[0] else int(matches[0])
    else:
        return None
    
# def mod_height_width(old_value, parent_string):
#     """Modifies the height or width based on parent groups dimensions"""
#     parent_value = int(re.search(r'\d+', parent_string).group())
#     new_value = round(float(old_value)/100 * parent_value)
#     return new_value

# def mod_left_top(old_value, parent_thickness_string, parent_location_string):
#     """Modifies the left or top value based on parent dimensions and locatoin"""
#     parent_location_value = int(re.search(r'\d+', parent_location_string).group())
#     parent_thickness_value = int(re.search(r'\d+', parent_thickness_string).group())
#     new_value = round(float(old_value)/100 * parent_thickness_value) + parent_location_value
#     return new_value

def mod_height_width(old_value, parent_string):
    """Modifies the height or width based on parent groups dimensions"""
    parent_value = int(re.search(r'\d+', parent_string).group())
    new_value = round(float(old_value)/100 * parent_value)
    return new_value

def mod_left_top(old_value, parent_thickness_string, parent_location_string):
    """Modifies the left or top value based on parent dimensions and locatoin"""
    parent_location_value = int(re.search(r'\d+', parent_location_string).group())
    parent_thickness_value = int(re.search(r'\d+', parent_thickness_string).group())
    new_value = round(float(old_value)/100 * parent_thickness_value) + parent_location_value
    return new_value

def multiply_list(numbers):
    result = 1
    for num in numbers:
        result *= num
    return result

def get_parent_parameters(element, htm_contents, current_position_params):
    """"""
    heights_list = [float(current_position_params[1][:-1])/100]
    widths_list = [float(current_position_params[0][:-1])/100]
    tops_list = [1]
    lefts_list = [1]

    element_start_index = htm_contents.find(element)
    units = '%'
    n = 0
    while '%' == units:
        n += 1
        htm_reversed = htm_contents[:element_start_index][::-1]
        closing = '>VID/<'
        opening = 'VID<'
        counter = 1

        end_of_closing = 0

        for i in range(0, len(htm_reversed)):
            if htm_reversed[i:i+6] == closing:
                counter += 1
                end_of_closing = len(htm_reversed) - i
            if htm_reversed[i:i+4] == opening:
                counter -= 1
                start_of_opening = len(htm_reversed) - (i+4)
            if counter == 0:
                break
        
        group = htm_contents[start_of_opening:end_of_closing]
        element_start_index = start_of_opening

        height_pattern = r'HEIGHT:\s*([\d.]+)\s*(%|px)'
        width_pattern = r'WIDTH:\s*([\d.]+)\s*(%|px)'
        left_pattern = r'LEFT:\s*([\d.]+)\s*(%|px)'
        top_pattern = r'TOP:\s*([\d.]+)\s*(%|px)'

        HEIGHT = re.search(height_pattern, group).group()
        WIDTH = re.search(width_pattern, group).group()
        LEFT = re.search(left_pattern, group).group()
        TOP = re.search(top_pattern, group).group()
        # print(HEIGHT, WIDTH, LEFT, TOP)

        if '%' in LEFT:
            # print(current_left, current_top)
            parent_height = float(HEIGHT[len('HEIGHT '):-1])/100
            parent_width = float(WIDTH[len('WIDTH '):-1])/100
            parent_left = float(LEFT[len('LEFT '):-1])/100
            parent_top = float(TOP[len('TOP '):-1])/100
            heights_list.append(parent_width)
            widths_list.append(parent_height)
            tops_list.append(parent_top)
            lefts_list.append(parent_left)

        elif 'px' in LEFT:
            # print(f"Group Left: {LEFT}, Group Top: {TOP}")
            # print(f"Width multiplier: {widths_list}\nHeight multipliers: {heights_list}\nTop Multipliers: {tops_list}\nLeft multipliers: {lefts_list}")
            parent_height = int(HEIGHT[len('HEIGHT '):-2])
            parent_width = int(WIDTH[len('WIDTH '):-2])
            parent_left = int(LEFT[len('LEFT '):-2])
            parent_top = int(TOP[len('TOP '):-2])

            heights_list.append(1)
            widths_list.append(1)
            global_top = parent_top # or 0 check with 1 at start of list
            global_left = parent_left
            for i in range(1, n):
                global_top += tops_list[-i]*multiply_list(heights_list[-i:])*parent_height
                global_left += lefts_list[-i]*multiply_list(widths_list[-i:])*parent_width

            # global_left = round(multiply_list(widths_list) * parent_width + multiply_list(lefts_list) * parent_left)
            # global_top = round(multiply_list(heights_list) * parent_height + multiply_list(tops_list) * parent_top)

            current_position_params = [f'{int(round(global_left, 0))}px', f'{int(round(global_top, 0))}px']
            units = 'px'
            print("SHOULD BE FINAL PARAMS ___: ", current_position_params)
    return current_position_params

    # matches = list(re.finditer(pattern, htm_to_search, re.MULTILINE))
    # print(matches)

def modify_group(group):
    # Modifies all the elements in a group except for those that are within a nested group
    height_pattern = r'HEIGHT:\s*([\d.]+)\s*(%|px)'
    width_pattern = r'WIDTH:\s*([\d.]+)\s*(%|px)'
    left_pattern = r'LEFT:\s*([\d.]+)\s*(%|px)'
    top_pattern = r'TOP:\s*([\d.]+)\s*(%|px)'
    
    # get all the parent values
    HEIGHT = re.search(height_pattern, group).group()
    WIDTH = re.search(width_pattern, group).group()
    LEFT = re.search(left_pattern, group).group()
    TOP = re.search(top_pattern, group).group()
    # print(f'Parent values: {HEIGHT}, {WIDTH}, {LEFT}, {TOP}')
    error = False

  
    # print(HEIGHT)
    # Check if '%' is in HEIGHT, WIDTH, LEFT, or TOP
    if '%' in HEIGHT or '%' in WIDTH or '%' in LEFT or '%' in TOP:
        # print(f"Percentage found in at least one of HEIGHT, WIDTH, LEFT, or TOP of group:\n--------------------------------\n{group}\n-----------------------------------\n")
        error = True

    # Check for subgroups and remove the subgroup from what we are modifying
    subgroups = extract_group_elements(group)
    if len(subgroups) > 1:
        subgroup = subgroups[1]
        items_being_modified = group.replace(subgroup, '\n\nPLACEHOLDER FOR SUBGROUP\n\n')
    else:
        items_being_modified = group

    # print(items_being_modified)
    all_heights = [match for match in (re.findall(height_pattern, items_being_modified))]
    all_widths = [match[0] for match in (re.findall(width_pattern, items_being_modified))]
    all_lefts = [match[0] for match in (re.findall(left_pattern, items_being_modified))]
    all_tops = [match[0] for match in (re.findall(top_pattern, items_being_modified))]

    # print(all_heights)

    for i in range(1, len(all_heights)):
        old_height = all_heights[i][0]
        old_width = all_widths[i][0]
        old_left = all_lefts[i][0]
        old_top = all_tops[i][0]

        new_height = format_for_sub(mod_height_width(old_height, HEIGHT), PARAM='HEIGHT', unit='px')
        new_width = format_for_sub(mod_height_width(old_width, WIDTH), 'WIDTH', 'px')
        new_left = format_for_sub(mod_left_top(old_left, WIDTH, LEFT), 'LEFT', 'px')
        new_top = format_for_sub(mod_left_top(old_top, HEIGHT, TOP), 'TOP', 'px')

        old_height = format_for_sub(old_height, 'HEIGHT', '%')
        old_width = format_for_sub(old_width, 'WIDTH', '%')
        old_left = format_for_sub(old_left, 'LEFT', '%')
        old_top = format_for_sub(old_top, 'TOP', '%')

        # print(f'subbing out: {old_height}, {old_width}, {old_left}, {old_top}, and subbing in: {new_height}, {new_width}, {new_left}, {new_top}')
        
        items_being_modified = multiple_substitutions(items_being_modified, [old_height, old_width, old_left, old_top], [new_height, new_width, new_left, new_top])


    # If there is a subgroup then still want to modify the first item (the nested group)
    if len(subgroups) > 1:
        subgroup_HEIGHT = re.findall(height_pattern, subgroup)[0][0]
        subgroup_WIDTH = re.findall(width_pattern, subgroup)[0][0]
        subgroup_LEFT = re.findall(left_pattern, subgroup)[0][0]
        subgroup_TOP = re.findall(top_pattern, subgroup)[0][0]
        
        # print(HEIGHT)
        # print(subgroup_HEIGHT)

        new_subgroup_height = format_for_sub(mod_height_width(subgroup_HEIGHT, HEIGHT), PARAM='HEIGHT', unit='px')
        new_subgroup_width = format_for_sub(mod_height_width(subgroup_WIDTH, WIDTH), 'WIDTH', 'px')
        new_subgroup_left = format_for_sub(mod_left_top(subgroup_LEFT, WIDTH, LEFT), 'LEFT', 'px')
        new_subgroup_top = format_for_sub(mod_left_top(subgroup_TOP, HEIGHT, TOP), 'TOP', 'px')

        subgroup_HEIGHT = format_for_sub(subgroup_HEIGHT, 'HEIGHT', '%')
        subgroup_WIDTH = format_for_sub(subgroup_WIDTH, 'WIDTH', '%')
        subgroup_LEFT = format_for_sub(subgroup_LEFT, 'LEFT', '%')
        subgroup_TOP = format_for_sub(subgroup_TOP, 'TOP', '%')

        # print(f'SUBGROUP: subbing out: {subgroup_HEIGHT}, {subgroup_WIDTH}, {subgroup_LEFT}, {subgroup_TOP}, and subbing in: {new_subgroup_height}, {new_subgroup_width}, {new_subgroup_left}, {new_subgroup_top}')

        subgroup = multiple_substitutions(subgroup, [subgroup_HEIGHT, subgroup_WIDTH, subgroup_LEFT, subgroup_TOP], [new_subgroup_height, new_subgroup_width, new_subgroup_left, new_subgroup_top])

        # now with the nested group having its position changed, we can swap it back for our placeholder so that the items_being_modified is now the fully modified group
        items_being_modified = group.replace('PLACEHOLDER FOR SUBGROUP', subgroup)

    # # print(re.search(r'\d+', HEIGHT).group())
    
    # modded_heights = [str(round(float(height)/100 * int(re.search(r'\d+', HEIGHT).group()))) for height in all_heights]
    # modded_widths = [str(round(float(width)/100 * int(re.search(r'\d+', WIDTH).group()))) for width in all_widths]
    # modded_lefts = [str(round(float(left)/100 * int(re.search(r'\d+', WIDTH).group()) + int(re.search(r'\d+', LEFT).group()))) for left in all_lefts]
    # modded_tops = [str(round(float(top)/100 * int(re.search(r'\d+', HEIGHT).group()) + int(re.search(r'\d+', TOP).group()))) for top in all_tops]

    # sub_in_heights = format_for_sub(modded_heights, 'HEIGHT', 'px')
    # sub_in_widths = format_for_sub(modded_widths, 'WIDTH', 'px')
    # sub_in_lefts = format_for_sub(modded_lefts, 'LEFT', 'px')
    # sub_in_tops = format_for_sub(modded_tops, 'TOP', 'px')
    # sub_in = sub_in_heights + sub_in_widths + sub_in_lefts + sub_in_tops
    
    # sub_out_heights = format_for_sub(all_heights, 'HEIGHT', '%')
    # sub_out_widths = format_for_sub(all_widths, 'WIDTH', '%')
    # sub_out_lefts = format_for_sub(all_lefts, 'LEFT', '%')
    # sub_out_tops = format_for_sub(all_tops, 'TOP', '%')
    # sub_out = sub_out_heights + sub_out_widths + sub_out_lefts + sub_out_tops

    # new_group = multiple_substitutions(group, sub_out, sub_in)
    new_group_trimmed = remove_tags(items_being_modified)

    return new_group_trimmed, error

def remove_groups(html_content):
    """Removes the grouping related to checkbox elements"""
    # Find all groups in hmtl_content (including nested) that contain a checkbox
    all_groups = extract_group_elements(html_content)
    error = False
    print(f'Num of groups found: {len(all_groups)}')
    # print(all_groups)
    while len(all_groups) > 0:
        group_to_change = all_groups[0]
        new_group, error = modify_group(group_to_change)
        html_content = html_content.replace(group_to_change, new_group)
        all_groups = extract_group_elements(html_content)
        
    return html_content, error
