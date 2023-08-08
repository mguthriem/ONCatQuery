import pyoncat
import numpy as np
import matplotlib as plt
from ONCatTools import filterObj


#User credentials; requested from Peter Parker
CLIENT_ID = ""
CLIENT_SECRET = ""

########################################
########    INPUTS    ##################
########################################

#specify where output csv file will be written


#specify Facility and Instrument
facility = "SNS"
instrument = "SNAP" 

#specify limiting run numbers to search
min_run = 59940-30000#30000
max_run = 59940

filters = []
#build up a list of conditions to filter on here
#notes:
# 1) if a pv contains a float, you need to include a decimal otherwise script won't know it's a float!
# 2) all pvs are written in lower case 
#
# Existing filters are defined in ONCatTools.py. example usage is given below
#
# the gist is to append filter objects to the list `filters` building up all the conditions
# required. filter objects can test various conditions that depend on the nature of the variable being tested (be it a string, integer or float parmameter)
# filters.append(filterObj('title','contains','diam') )
# filters.append(filterObj('proton_charge','>',1e12))
# filters.append(filterObj('daslogs.optics','==',1))
# filters.append(filterObj('daslogs.det_arc1','~=',-90.0,1.0))
# filters.append(filterObj('daslogs.det_arc2','~=',90.0,1.0))
# filters.append(filterObj('daslogs.lambdarequest','~=',2.1,0.1))
#filters.append(filterObj('daslogs.bl3:det:th:bl:frequency','~=',60.0,0.1))

#set up outout here: 

#will output IPTS, Run number, Title, Duration and any additional items specified here
# in the list outputItems

out_folder = ""

out_fileName = ".csv"

outputItems = ['end_time',
               'total_counts']


########################################
########################################
########################################

oncat = pyoncat.ONCat(
    "https://oncat.ornl.gov",
    client_id=CLIENT_ID,
    client_secret=CLIENT_SECRET,
    flow=pyoncat.CLIENT_CREDENTIALS_FLOW,
)

# Define projectionList, the exhaustive list of metadata entries to filter on

projectionList = ["metadata.entry.title","indexed.run_number","experiment","metadata.entry.duration","size"]

for f in filters:
    f.item = f'metadata.entry.{f.item.lower()}'
    projectionList.append(f.item)

for item in outputItems:
    item = f'metadata.entry.{item}'
    if item not in projectionList:
        projectionList.append(item)

#replace all entries with lower case versions
# 
for item in projectionList:
     item = item.lower() 

print('\n Projection List:',projectionList,'\n')

print(f'\nAccessing database. Downloading {max_run-min_run+1} runs...\n')
datafiles = oncat.Datafile.list(
    facility=facility,
    instrument=instrument,
    ranges_q = "indexed.run_number:{}-{}".format(min_run, max_run),
    projection=projectionList
    )

print(datafiles[-1].nodes())
# print(f'found {len(datafiles)} starting runs for filtering')

#build header
header = "IPTS, Run Number, Title, Duration (min), Size (Gb)"
for item in outputItems:
        header = header + ',' + item 
output = header + '\n'

print(f'\nChecking {len(filters)} filter conditions...\n')

nMatches = 0
Warnings = 0
WarningCount = [0,0,0,0]
for data in datafiles:
    
    # loop through all datafiles and check that all filter conditions are met
    filterMatch = []
    for f in filters:
        # print(f'checking filter {f.item} of type:', type(data.get(f.item)))
        #data may be strings, int float or instances of a class called pyoncat.ONCatRepresentation 
        if isinstance(data.get(f.item),(str,int,float)):           
            filterMatch.append(f.checkMatch(data.get(f.item)))
        elif isinstance(data.get(f.item),pyoncat.ONCatRepresentation):
            # print(f'Checking if ref value: {f.item} with value {f.target}')
            # print('matches',data.get(f.item).average_value)
            filterMatch.append(f.checkMatch(data.get(f.item).average_value))
        else:
            Warnings = 1
            WarningDetails = f.item
            WarningCount[Warnings] += 1
    
    # print(filterMatch)

    if all(filterMatch) == True:
        nMatches += 1

        title =  data.get("metadata.entry.title").replace(","," ")
        title = title.replace(";"," ")
        run_number = data.get("indexed.run_number")
        ipts = data.get("experiment")
        duration = data.get("metadata.entry.duration")
        size = data.get("size")

        output = output + f'{ipts},{run_number},{title},{duration/60:.3f},{size/1e9:.3f}'
        for item in outputItems:
                # print(item,str(data.get(f'metadata.entry.{item}')),type(data.get(f'metadata.entry.{item}')))
                if isinstance(data.get(f'metadata.entry.{item}'),(str,int,float)):
                    # print('this is int,float or str:',data.get(f'metadata.entry.{item}'))
                    output = output + ',' + str(data.get(f'metadata.entry.{item}'))
                elif isinstance(data.get(f'metadata.entry.{item}'),pyoncat.ONCatRepresentation):
                    # print(f'looking for: metadata.entry.{item}')
                    # print('value',data.get(f'metadata.entry.{item}').average_value)
                    val = data.get(f'metadata.entry.{item}').average_value
                    output = output + ','+ f'{val:.3f}'
                else:
                    print(f'item {item} not found')
        output = output + '\n'
        # print(data["size"]/1e9)

if Warnings == 1:
    print(f'WARNING: filter item absent from run data {WarningDetails} in {WarningCount[1]} runs')

print(f'Found {nMatches} out of {max_run-min_run+1} entries matching all filters')
# print(output)
out_file = open(out_folder+out_fileName,'w+')
out_file.write(output)
out_file.close()
