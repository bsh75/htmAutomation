def copy_file(source_file, destination_file):
    with open(source_file, 'r') as source:
        content = source.read()

    with open(destination_file, 'w') as destination:
        destination.write(content)

# copyFrom = 'checkingChanges2/2m-ahu2 - preManHtgChange.htm'
# copyTo = 'checkingChanges2/afterChange.htm'
# copyFromB = 'checkingChanges2/2m-ahu2 Bindings - preChange.xml'
# copyToB = 'checkingChanges2/afterChangeBindings.xml'
# copyFromB = 'checkingChanges2/DS-preManHtgChange.dsd'
# copyToD = 'checkingChanges2/afterChangeDS.dsd'


copyFrom = 'checkingChanges2/before.htm'
copyTo = 'checkingChanges2/after.htm'
copyFromB = 'checkingChanges2/before.xml'
copyToB = 'checkingChanges2/after.xml'
copyFromD = 'checkingChanges2/before.dsd'
copyToD = 'checkingChanges2/after.dsd'


copy_file(copyFrom, copyTo)

copy_file(copyFromB, copyToB)

copy_file(copyFromD, copyToD)
# r = r'\r'
# string = f'this is a string with {r} preserved'
# print(string)