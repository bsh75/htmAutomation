import pandas as pd
import xml.etree.ElementTree as ET

# Load the datasource file
tree = ET.parse('checking changes2\DS-preManHtgChange.txt')
root = tree.getroot()

# Create a DataFrame to store the data
data = []
columns = ['id']

# Iterate over each dataobject
for dataobject in root.findall('dataobject'):
    properties = dataobject.findall('property')
    data_object = {'id': dataobject.attrib['id']}

    # Iterate over each property of the dataobject
    for prop in properties:
        prop_name = prop.attrib['name']
        prop_value = prop.text

        # Add the property name to the columns if not already present
        if prop_name not in columns:
            columns.append(prop_name)

        # Add the property value to the data object dictionary
        data_object[prop_name] = prop_value

    # Append the data object to the list of data
    data.append(data_object)

# Create a DataFrame from the data
df = pd.DataFrame(data, columns=columns)

# Save the DataFrame to an Excel file
df.to_excel('datasource.xlsx', index=False)