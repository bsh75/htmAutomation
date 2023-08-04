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

# Example usage:
htm_content = '''
<DIV>
    This is a grouped element.
    <DIV>
        This is a nested grouped element.
    </DIV>
</DIV>
<DIV>
    Another grouped element.
</DIV>
'''

grouped_elements = find_grouped_elements(htm_content)
print(grouped_elements)
