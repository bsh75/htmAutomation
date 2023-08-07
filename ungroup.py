import re
import math

def extract_group_elements(html_content, checkbox_in_matters):
    # Find all opening <DIV> tags with 'tabIndex=-1' and 'id=group' attributes
    opening_div_pattern = r'<DIV[^>]*class='
    opening_div_matches = re.findall(opening_div_pattern, html_content)
    
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
                nested_div_flag += 1
            if html_content[i:i+6] == '</DIV>':
                nested_div_flag -= 1
                # Check if we have found the closing </DIV> for the current opening <DIV>
                if nested_div_flag == 0:
                    group_content = html_content[start_index:i+6]
                    if checkbox_in_matters:
                        if ('id=checkbox' in group_content):
                            group_content_list.append(group_content)
                            elements = group_content + '\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n'
                            extracted_group_elements.append(elements)
                    else:
                        group_content_list.append(group_content)
                        elements = group_content + '\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n'
                        extracted_group_elements.append(elements)

                    break
    return group_content_list

def format_for_sub(list, PARAM, unit):
    return [f"{PARAM}: {each}{unit}" for each in list]

def multiple_substitutions(string, to_replace, to_substitute):
    # Perform substitutions using the lists, order should be preserved
    for i in range(len(to_replace)):
        string = string.replace(to_replace[i], to_substitute[i], 1)

    return string

def remove_tags(string):
    # Find the index of the first '>' and last '</DIV>'
    first_gt_index = string.find('>') + 1
    last_div_index = string.rfind('</DIV>')

    # Extract the substring between the first '>' and last '</DIV>'
    result = string[first_gt_index:last_div_index]

    return result

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

def format_for_sub2(value, PARAM, unit):
    new_string = f"{PARAM}: {str(value)}{unit}"
    return new_string

def modify_group2(group):
    """Modifies all the elements in a group except for those that are within a nested group"""

    # Patterns to find all the desired parameters
    height_pattern = r' HEIGHT:\s*([\d.]+)\s*(%|px)'
    width_pattern = r' WIDTH:\s*([\d.]+)\s*(%|px)'
    left_pattern = r' LEFT:\s*([\d.]+)\s*(%|px)'
    top_pattern = r' TOP:\s*([\d.]+)\s*(%|px)'

    # The first ones found are the parent ones (belonging to the group being processed)
    HEIGHT = re.search(height_pattern, group).group()
    WIDTH = re.search(width_pattern, group).group()
    LEFT = re.search(left_pattern, group).group()
    TOP = re.search(top_pattern, group).group()
    
    # Check for subgroups and to remove from what is being modified (exclude 1st as it is original group)
    subgroups = extract_group_elements(group, checkbox_in_matters=False)[1:]

    subgroups_removed = []
    if len(subgroups) > 0:
        for i in range(0, len(subgroups)):
            if subgroups[i] in group:
                group = group.replace(subgroups[i], f'\n\nPLACEHOLDERs FOR SUBGROUPs\n\n')
                subgroups_removed.append(subgroups[i])
        items_being_modified = group
    else:
        items_being_modified = group

    # Get all the heights of objects in groups that are not in subgroups
    all_heights = [match[0] for match in (re.findall(height_pattern, items_being_modified))]
    all_widths = [match[0] for match in (re.findall(width_pattern, items_being_modified))]
    all_lefts = [match[0] for match in (re.findall(left_pattern, items_being_modified))]
    all_tops = [match[0] for match in (re.findall(top_pattern, items_being_modified))]

    # For all these objects, convert % into px
    for i in range(1, len(all_heights)):
        old_height = all_heights[i]
        old_width = all_widths[i]
        old_left = all_lefts[i]
        old_top = all_tops[i]

        new_height = format_for_sub2(mod_height_width(old_height, HEIGHT), PARAM='HEIGHT', unit='px')
        new_width = format_for_sub2(mod_height_width(old_width, WIDTH), 'WIDTH', 'px')
        new_left = format_for_sub2(mod_left_top(old_left, WIDTH, LEFT), 'LEFT', 'px')
        new_top = format_for_sub2(mod_left_top(old_top, HEIGHT, TOP), 'TOP', 'px')

        old_height = format_for_sub2(old_height, 'HEIGHT', '%')
        old_width = format_for_sub2(old_width, 'WIDTH', '%')
        old_left = format_for_sub2(old_left, 'LEFT', '%')
        old_top = format_for_sub2(old_top, 'TOP', '%')

        items_being_modified = multiple_substitutions(items_being_modified, [old_height, old_width, old_left, old_top], [new_height, new_width, new_left, new_top])


    # For each of the subgroups, convert the first parameters from % to px
    if len(subgroups) > 0:
        for subgroup in subgroups_removed:
            subgroup_HEIGHT = re.findall(height_pattern, subgroup)[0][0]
            subgroup_WIDTH = re.findall(width_pattern, subgroup)[0][0]
            subgroup_LEFT = re.findall(left_pattern, subgroup)[0][0]
            subgroup_TOP = re.findall(top_pattern, subgroup)[0][0]

            new_subgroup_height = format_for_sub2(mod_height_width(subgroup_HEIGHT, HEIGHT), PARAM='HEIGHT', unit='px')
            new_subgroup_width = format_for_sub2(mod_height_width(subgroup_WIDTH, WIDTH), 'WIDTH', 'px')
            new_subgroup_left = format_for_sub2(mod_left_top(subgroup_LEFT, WIDTH, LEFT), 'LEFT', 'px')
            new_subgroup_top = format_for_sub2(mod_left_top(subgroup_TOP, HEIGHT, TOP), 'TOP', 'px')

            subgroup_HEIGHT = format_for_sub2(subgroup_HEIGHT, 'HEIGHT', '%')
            subgroup_WIDTH = format_for_sub2(subgroup_WIDTH, 'WIDTH', '%')
            subgroup_LEFT = format_for_sub2(subgroup_LEFT, 'LEFT', '%')
            subgroup_TOP = format_for_sub2(subgroup_TOP, 'TOP', '%')

            subgroup = multiple_substitutions(subgroup, [subgroup_HEIGHT, subgroup_WIDTH, subgroup_LEFT, subgroup_TOP], [new_subgroup_height, new_subgroup_width, new_subgroup_left, new_subgroup_top])

           # now with the nested group having its position changed, we can swap it back for our placeholder so that the items_being_modified is now the fully modified group
            items_being_modified = items_being_modified.replace('PLACEHOLDERs FOR SUBGROUPs', subgroup, 1)

    new_group_trimmed = remove_tags(items_being_modified)
    return new_group_trimmed

def remove_groups2(html_content):
    """Removes the grouping related to checkbox elements"""
    # Find all groups in hmtl_content (including nested) that contain a checkbox
    all_groups = extract_group_elements(html_content, checkbox_in_matters=True)
    # print("ALL GROUPS _____________\n", all_groups, '\n\n')
    while len(all_groups) > 0:
        group_to_change = all_groups[0]
        new_group = modify_group2(group_to_change)
        html_content = html_content.replace(group_to_change, new_group)
        all_groups = extract_group_elements(html_content, checkbox_in_matters=True)
        
    return html_content
