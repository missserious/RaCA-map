from csv import reader
from csv import writer
from pathlib import Path


## DATA
## [rowLocation[0], rowLocation[1], rowLocation[2], rowPedons[0], rowPedons[5], rowPedons[8], rowPedons[9], rowPedons[10]]
## RacaID | lat | long | upedonid | rcasiteid | "SOCstock5" | "SOCstock30" | "SOCstock100"


# locations
with open("RaCa_general_location.csv", "r") as csv_file:
    csv_reader = reader(csv_file)
    listLocations = list(csv_reader) # list of lists


# pedons
with open("RaCA_SOC_pedons.csv", "r") as csv_file:
    csv_reader = reader(csv_file)
    listPedons = list(csv_reader) # list of lists

# delete header
del listLocations[0]
del listPedons[0]

#counter = 0
#counter02 = 0
finalList = []  # store matched data

# iterate and match
for rowLocation in listLocations:
    #print(rowLocation[0])
    flag = False
    for rowPedons in listPedons:
        ## check for matchID
        if rowLocation[0] == rowPedons[5]:
            # add location without pedons
            tmpListe = [rowLocation[0], rowLocation[1], rowLocation[2], rowPedons[0], rowPedons[5], rowPedons[8], rowPedons[9], rowPedons[10]]
            #counter = counter + 1
            finalList.append(tmpListe)
            flag = True
            break

    if not flag:
        # add location without pedons
        tmpListe = [rowLocation[0], rowLocation[1], rowLocation[2], float("NaN"), float("NaN"), float("NaN"), float("NaN"), float("NaN")]
        #counter02 = counter02 + 1
        finalList.append(tmpListe)


#print(counter)
#print(counter02)

#print(len(finalList))
#for element in finalList:
#    print(element)


# create and write csv file
myfile = Path("RaCA_matchedData.csv")
myfile.touch(exist_ok=True)
file = open(myfile, 'w')

with file:
    writer = writer(file)
    writer.writerow(["RacaID", "lat", "long", "upedonid", "rcasiteid", "SOCstock5", "SOCstock30", "SOCstock100"])
    for row in finalList:
        writer.writerow(row)
file.close()


# create geojson file
myfile = Path("data.js")
myfile.touch(exist_ok=True)
file = open(myfile, 'w')

counter03 = 0

# write geojson file
file.write('var myPoints = [{' + '\n')
for row in finalList:
    counter03 = counter03 + 1
    file.write('    "type": "Feature",' + '\n')
    file.write('    "properties": {' + '\n')
    file.write('        "racaID": "' + row[0] + '",' + '\n')
    file.write('        "upedonid": "' + str(row[3]) + '",' + '\n')
    file.write('        "SOCstock5": "' + str(row[5]) + '",' + '\n')
    file.write('        "SOCstock30": "' + str(row[6]) + '",' + '\n')
    file.write('        "SOCstock100": "' + str(row[7]) + '",' + '\n')
    file.write('    },' + '\n')
    file.write('    "geometry": {' + '\n')
    file.write('        "type": "Point",' + '\n')
    file.write('        "coordinates": [' + str(row[2]) + ', ' + str(row[1]) + ']' + '\n')
    file.write('    }' + '\n')
    # check >> End of File >>  --- }];
    if counter03 != len(finalList):
        file.write('}, {' + '\n')
    else:
        file.write('}];')
file.close()



# colored as to the amount of 'SOCstock30' they contain >> have a look at the values
listSOCstock30 = []

# hack >> filter nan and NA
for element in finalList:
    if isinstance(element[6], str) and element[6] != 'NA':
        listSOCstock30.append(float(element[6]))

print("min Value: " + str(min(listSOCstock30)))
print("max Value: " + str(max(listSOCstock30)))
