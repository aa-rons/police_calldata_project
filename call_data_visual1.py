import csv
from collections import Counter
import pygal


filename = '911_call_data.csv'

with open(filename,'r') as f:
    reader = csv.reader(f)
    header_row = next(reader)

    
# -------- Get all possible Call Types -------------
    possibleCallTypes = []
    allCallsByType = []
    tempList = []
    for row in reader:
        tempList.append(row)
        # value [7] in each row contains the 'call type'
        call_type = row[7]
        # To sort by large/small volume we must get a count for each call type
        allCallsByType.append(call_type)
        # Get all individual call types
        if call_type not in possibleCallTypes:
            possibleCallTypes.append(call_type)

    # Store only high volume call types -------------------- - - - - - - - 
    call_type_counted = Counter(allCallsByType)
    high_volume_calltype = []  #  <----- This is the array we are pulling from
    for calltype, count in call_type_counted.items():
        if count > 3500:
            high_volume_calltype.append(calltype)

# ------------------ ------------ --------------------            
    # store all call types (A-Z) with index number
    callTypeIndeces = {}

    for call_type, type_index in enumerate(sorted(high_volume_calltype)): 
        callTypeIndeces[type_index] = call_type

    # Creating/Initializing Final Outcome of all reports by type.
    reportTakenCounts = []
    noReportTakenCounts = []
    ticketArrestCounts = []
    otherCounts = []

    # ----- Initialize all counters -------------
    for callType, callIndex in callTypeIndeces.items():
        #print("Initiating call type index: ", callType, callIndex)
        reportTakenCounts.append(0)
        noReportTakenCounts.append(0)
        ticketArrestCounts.append(0)
        otherCounts.append(0)

    report_taken_codes = ['F','O','R']
    no_report_taken_codes = ['DUPNCAN','DUP','CAN','U','NR','N','G']
    ticket_arrest_made_codes = ['A','B','C','D','E']
    other_codes = ['H','M','P','T']

    

    for row2 in tempList:
        dispositionCode = row2[8]
        callType = row2[7]

        #print(dispositionCode)
        if dispositionCode in report_taken_codes: # 
            if callType in callTypeIndeces:
                callTypeIndex = callTypeIndeces[callType]
                if callTypeIndex is not None:
                    reportTakenCounts[callTypeIndex] += 1

        elif dispositionCode in no_report_taken_codes: # 
            if callType in callTypeIndeces:
                callTypeIndex = callTypeIndeces[callType]
                if callTypeIndex is not None:
                    noReportTakenCounts[callTypeIndex] += 1

        elif dispositionCode in ticket_arrest_made_codes: # 
            if callType in callTypeIndeces:
                callTypeIndex = callTypeIndeces[callType]
                if callTypeIndex is not None:
                    ticketArrestCounts[callTypeIndex] += 1

        elif dispositionCode in other_codes: # 
            if callType in callTypeIndeces:
                callTypeIndex = callTypeIndeces[callType]
                if callTypeIndex is not None:
                    otherCounts[callTypeIndex] += 1




# ----------------------- MAKE VISUAL CHART --------------------------
line_chart = pygal.StackedBar(width= 2200, height = 800, x_label_rotation = 30, 
                            x_title = 'Call Type', y_title = 'Call Volume',
                            fontsize = 30)
line_chart.x_labels = map(str , high_volume_calltype)
line_chart.title = ("Most Common 911 Calls by Type: Nov. 2017 - Jan. 2018")
line_chart.add('No Report',  noReportTakenCounts)
line_chart.add('Report Taken', reportTakenCounts)
line_chart.add('Ticket or Arrest', ticketArrestCounts)
line_chart.add('Other', otherCounts)
line_chart.render_to_file("NewStackedBar.svg")

