import re
import math

def extract_group_elements_from_file(html_content):
    # Find all opening <DIV> tags with 'tabIndex=-1' and 'id=group' attributes
    opening_div_pattern = r'<DIV\s+tabIndex=-1\s+id=group\d{3}'
    opening_div_matches = re.findall(opening_div_pattern, html_content)
    print(opening_div_matches)

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
                    if 'id=checkbox' in group_content:
                        group_content_list.append(group_content)
                        elements = group_content + '\n^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^\n'
                        extracted_group_elements.append(elements)
                    break

    # Print the number of sections found
    num_sections_found = len(extracted_group_elements)
    print(f"Number of sections found: {num_sections_found}")

    return group_content_list

def format_for_sub(list, PARAM, unit):
    return [f"{PARAM}: {each}{unit}" for each in list]

def multiple_substitutions(string, to_replace, to_substitute):
    # Perform substitutions using the lists
    for i in range(len(to_replace)):
        string = string.replace(to_replace[i], to_substitute[i])

    return string

def remove_tags(string):
    # Find the index of the first '>' and last '</DIV>'
    first_gt_index = string.find('>') + 1
    last_div_index = string.rfind('</DIV>')

    # Extract the substring between the first '>' and last '</DIV>'
    result = string[first_gt_index:last_div_index]

    return result

def modify_group(group):
    # get all the parent values
    HEIGHT = re.search(r'HEIGHT:\s*([\d.]+)(%|px)', group).group()
    WIDTH = re.search(r'WIDTH:\s*([\d.]+)(%|px)', group).group()
    LEFT = re.search(r'LEFT:\s*([\d.]+)(%|px)', group).group()
    TOP = re.search(r'TOP:\s*([\d.]+)(%|px)', group).group()

    # Check if '%' is in HEIGHT, WIDTH, LEFT, or TOP
    if '%' in HEIGHT or '%' in WIDTH or '%' in LEFT or '%' in TOP:
        print("Percentage found in at least one of HEIGHT, WIDTH, LEFT, or TOP.")

    all_heights = re.findall(r'HEIGHT:\s*([\d.]+)%', group)
    all_widths = re.findall(r'WIDTH:\s*([\d.]+)%', group)
    all_lefts = re.findall(r'LEFT:\s*([\d.]+)%', group)
    all_tops = re.findall(r'TOP:\s*([\d.]+)%', group)

    # print(re.search(r'\d+', HEIGHT).group())

    modded_heights = [str(round(float(height)/100 * int(re.search(r'\d+', HEIGHT).group()))) for height in all_heights]
    modded_widths = [str(round(float(width)/100 * int(re.search(r'\d+', WIDTH).group()))) for width in all_widths]
    modded_lefts = [str(round(float(left)/100 * int(re.search(r'\d+', WIDTH).group()) + int(re.search(r'\d+', LEFT).group()))) for left in all_lefts]
    modded_tops = [str(round(float(top)/100 * int(re.search(r'\d+', HEIGHT).group()) + int(re.search(r'\d+', TOP).group()))) for top in all_tops]

    sub_in_heights = format_for_sub(modded_heights, 'HEIGHT', 'px')
    sub_in_widths = format_for_sub(modded_widths, 'WIDTH', 'px')
    sub_in_lefts = format_for_sub(modded_lefts, 'LEFT', 'px')
    sub_in_tops = format_for_sub(modded_tops, 'TOP', 'px')
    sub_in = sub_in_heights + sub_in_widths + sub_in_lefts + sub_in_tops
    
    sub_out_heights = format_for_sub(all_heights, 'HEIGHT', '%')
    sub_out_widths = format_for_sub(all_widths, 'WIDTH', '%')
    sub_out_lefts = format_for_sub(all_lefts, 'LEFT', '%')
    sub_out_tops = format_for_sub(all_tops, 'TOP', '%')
    sub_out = sub_out_heights + sub_out_widths + sub_out_lefts + sub_out_tops

    new_group = multiple_substitutions(group, sub_out, sub_in)
    new_group_trimmed = remove_tags(new_group)

    return new_group_trimmed

# Example usage:
input_file = 'input.htm'  # Replace with the name of your input HTML file
output_file = 'output.htm'  # Replace with the desired output file name

with open(input_file, 'r') as file:
    html_content = file.read()

all_groups = extract_group_elements_from_file(html_content)

all_separated_groups = []

for group in all_groups:
    all_separated_groups.append(modify_group(group))

new_html_content = multiple_substitutions(html_content, all_groups, all_separated_groups)

# Write the extracted group elements to the output file
with open(output_file, 'w') as file:
    file.write(new_html_content)