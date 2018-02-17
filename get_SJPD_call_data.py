"""
This program scrapes the SJPD website to get all 9-11 call info and stores
it to a csv file.
"""

import requests
import csv

page_number = 0
while page_number < 350:
    # Make an API call and store the response
    url = ('http://api.data.sanjoseca.gov/api/v2/datastreams/911-CALL-DATA/data.' +
            'json/?auth_key=2d9e6941aa11612cdba6ed774b550cc051326a78&limit=1000' +
            '&page=' + str(page_number))
    page_number += 1

    r = requests.get(url)
    # Display the "Status Code" of the page - "200" is good
    print(str(page_number), " Status code:", r.status_code)

    # Store API response in json format as a variable
    response_dict = r.json()

    arr = response_dict['result']['fArray']

    columns = []
    counter = 0
    while counter < len(arr):
        rows = []
        counter2 = 0
        while counter2 < 16:
            if counter >= len(arr):
                print('Oh shit')
                print(counter)
                print(len(arr))
            else:
                cur_cell = arr[counter]
                rows.append(arr[counter]['fStr'])
            counter2 += 1
            counter += 1        
        columns.append(rows)

    column_titles = columns[0]
    #print(column_titles)

    with open('911_call_data.csv','a') as call_data:
        data_writer = csv.writer(call_data)
        for row in columns:
            data_writer.writerow(row)




    





