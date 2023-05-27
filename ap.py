from datetime import datetime

date_string = "2023-5-27"
format_string = "%Y-%m-%d"

datetime_obj = datetime.strptime(date_string, format_string)

print(str(datetime_obj)[0:10])
