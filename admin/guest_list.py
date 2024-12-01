#imports
import pandas as pd
from io import BytesIO
from admin import pull_booking, encod
from flask import make_response


# function to download list of people booked for event
def download_list(table_name):
    
    #pull recrods and salt
    data, salt = pull_booking.pull_records(table_name)

    #create empty dict
    data_dict = {}

    #loop through data & decrypt it
    #populate dict
    for record in data:
        for item in record:
            data_dict.update({
                item[0]:{
                    'name':encod.decrypt_data(salt, item[1]) + " " + encod.decrypt_data(salt, item[2]),
                    'phone': encod.decrypt_data(salt, item[4]),
                    'spaces': item[5]
                }
            })
    df = pd.DataFrame.from_dict(data_dict)


    #create output and writer
    output = BytesIO()
    writer = pd.ExcelWriter(output)

    #export df to excel
    df.to_excel(writer, index=False, header=False, sheet_name='Guest List')
    #set width for columns
    writer.sheets['Guest List'].autofit()
    writer.close()
    excel_file = make_response(output.getvalue())

    # Defining correct excel headers
    excel_file.headers["Content-Disposition"] = "attachment; filename=Guest List.xlsx"
    excel_file.headers["Content-type"] = "application/x-xls"

    
    # Finally return response
    return excel_file

