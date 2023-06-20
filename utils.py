import datetime


def convert_detail_source(string):
    
    x = string.split('\'source\': \'')
    x = x[1].split('\'}')
    source = x[0]
    
    return source


def convert_detail_time(string):
    
    x = string.split('), ')
    x = x[0].split(', ')
    time = datetime.time(int(x[-2]), int(x[-1]))
    
    return time.strftime("%H:%M")
    