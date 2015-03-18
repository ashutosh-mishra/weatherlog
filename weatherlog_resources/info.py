# -*- coding: utf-8 -*-


# This file defines the functions for getting the info.


# Import datetime for date calculations.
import datetime
# Import collections.Counter for getting the mode of the data.
from collections import Counter

# Import the dataset functions.
import weatherlog_resources.datasets as datasets
# Import the calculation functions.
import weatherlog_resources.calculations as calculations


def general_info(data, units):
    """Gets the general info."""
    
    # Get the date data.
    date_data = datasets.get_column(data, 0)
    date_first = date_data[0]
    date_last = date_data[len(date_data) - 1]
    date_first2 = datetime.datetime.strptime(date_first, "%d/%m/%Y")
    date_last2 = datetime.datetime.strptime(date_last, "%d/%m/%Y")
    date_num = (date_last2 - date_first2).days + 1
    day_num = len(data)
    
    # Get the temperature data.
    temp_data = datasets.convert_float(datasets.get_column(data, 1))
    temp_low = min(temp_data)
    temp_high = max(temp_data)
    temp_avg = calculations.mean(temp_data)
    
    # Get the precipitation data.
    prec_data1, prec_data2 = datasets.split_list(datasets.get_column(data, 2))
    prec_data1 = datasets.convert_float(datasets.none_to_zero(prec_data1))
    try:
        prec_low = min(prec_data1)
        prec_high = max(prec_data1)
        prec_avg = calculations.mean(prec_data1)
    except:
        prec_low = "None"
        prec_high = "None"
        prec_avg = "None"
    
    # Get the wind data.
    wind_data1, wind_data2 = datasets.split_list(datasets.get_column(data, 3))
    wind_data1 = datasets.convert_float(datasets.none_to_zero(wind_data1))
    try:
        wind_low = min(wind_data1)
        wind_high = max(wind_data1)
        wind_avg = calculations.mean(wind_data1)
    except:
        wind_low = "None"
        wind_high = "None"
        wind_avg = "None"
    
    # Get the humidity data.
    humi_data = datasets.convert_float(datasets.get_column(data, 4))
    humi_low = min(humi_data)
    humi_high = max(humi_data)
    humi_avg = calculations.mean(humi_data)
    
    # Get the air pressure data.
    airp_data1, airp_data2 = datasets.split_list(datasets.get_column(data, 5))
    airp_data1 = datasets.convert_float(airp_data1)
    airp_low = min(airp_data1)
    airp_high = max(airp_data1)
    airp_avg = calculations.mean(airp_data1)
    
    # Get the cloud cover data.
    clou_data = Counter(datasets.get_column(data, 6))
    clou_mode = clou_data.most_common(1)[0][0]
    
    # Change any values, if needed.
    prec_low = "None" if prec_low == "None" else ("%.2f %s" % (prec_low, units["prec"]))
    prec_high = "None" if prec_high == "None" else ("%.2f %s" % (prec_high, units["prec"]))
    prec_avg = "None" if prec_avg == "None" else ("%.2f %s" % (prec_avg, units["prec"]))
    wind_low = "None" if wind_low == "None" else ("%.2f %s" % (wind_low, units["wind"]))
    wind_high = "None" if wind_high == "None" else ("%.2f %s" % (wind_high, units["wind"]))
    wind_avg = "None" if wind_avg == "None" else ("%.2f %s" % (wind_avg, units["wind"]))
    
    # Create the data list.
    data2 = [
        ["First day", "%s" % date_first],
        ["Last day", "%s" % date_last],
        ["Number of days", "%d" % day_num],
        ["Range of days", "%d" % date_num],
        ["Lowest temperature", "%.2f %s" % (temp_low, units["temp"])], 
        ["Highest temperature", "%.2f %s" % (temp_high, units["temp"])],
        ["Average temperature", "%.2f %s" % (temp_avg, units["temp"])],
        ["Lowest precipitation", prec_low],
        ["Highest precipitation", prec_high],
        ["Average precipitation", prec_avg],
        ["Lowest wind speed", wind_low],
        ["Highest wind speed", wind_high],
        ["Average wind speed", wind_avg],
        ["Lowest humidity", "%.2f%%" % humi_low], 
        ["Highest humidity", "%.2f%%" % humi_high],
        ["Average humidity", "%.2f%%" % humi_avg],
        ["Lowest air pressure", "%.2f %s" % (airp_low, units["airp"])],
        ["Highest air pressure", "%.2f %s" % (airp_high, units["airp"])],
        ["Average air pressure", "%.2f %s" % (airp_avg, units["airp"])],
        ["Most common cloud cover", "%s" % clou_mode]
    ]
    
    return data2


def temp_info(data, units):
    """"Gets the temperature info."""
    
    # Get the data.
    temp_data = datasets.convert_float(datasets.get_column(data, 1))
    temp_low = min(temp_data)
    temp_high = max(temp_data)
    temp_avg = calculations.mean(temp_data)
    temp_median = calculations.median(temp_data)
    temp_range = calculations.range(temp_data)
    temp_mode = calculations.mode(temp_data)
    
    # Create the data list.
    data2 = [
        ["Lowest temperature", "%.2f %s" % (temp_low, units["temp"])],
        ["Highest temperature", "%.2f %s" % (temp_high, units["temp"])],
        ["Average temperature", "%.2f %s" % (temp_avg, units["temp"])],
        ["Median temperature", "%.2f %s" % (temp_median, units["temp"])],
        ["Range of temperatures", "%.2f %s" % (temp_range, units["temp"])],
        ["Most common temperature", "%.2f %s" % (temp_mode, units["temp"])]
    ]
    
    return data2


def prec_info(data, units):
    """"Gets the precipitation info."""
    
    # Get the data.
    prec_data1, prec_data2 = datasets.split_list(datasets.get_column(data, 2))
    prec_split = datasets.split_list2(datasets.get_column(data, 2))
    prec_data1 = datasets.none_to_zero(prec_data1)
    prec_data1 = datasets.convert_float(prec_data1)
    try:
        prec_low = min(prec_data1)
        prec_high = max(prec_data1)
        prec_avg = calculations.mean(prec_data1)
        prec_median = calculations.median(prec_data1)
        prec_range = calculations.range(prec_data1)
    except:
        prec_low = "None"
        prec_high = "None"
        prec_avg = "None"
        prec_median = "None"
        prec_range = "None"
    prec_total = 0
    prec_total_rain = 0
    prec_total_snow = 0
    prec_total_hail = 0
    prec_total_sleet = 0
    prec_none = 0
    prec_rain = 0
    prec_snow = 0
    prec_hail = 0
    prec_sleet = 0
    for i in prec_split:
        if i[1] != "None":
            prec_total += float(i[0])
        if i[1] == "None":
            prec_none += 1
        elif i[1] == "Rain":
            prec_total_rain += float(i[0])
            prec_rain += 1
        elif i[1] == "Snow":
            prec_total_snow += float(i[0])
            prec_snow += 1
        elif i[1] == "Hail":
            prec_total_hail += float(i[0])
            prec_hail += 1
        elif i[1] == "Sleet":
            prec_total_sleet += float(i[0])
            prec_sleet += 1
    prec_mode = calculations.mode(prec_data2)
    
    # Change any values, if needed.
    prec_low = "None" if prec_low == "None" else ("%.2f %s" % (prec_low, units["prec"]))
    prec_high = "None" if prec_high == "None" else ("%.2f %s" % (prec_high, units["prec"]))
    prec_avg = "None" if prec_avg == "None" else ("%.2f %s" % (prec_avg, units["prec"]))
    prec_median = "None" if prec_median == "None" else ("%.2f %s" % (prec_median, units["prec"]))
    prec_range = "None" if prec_range == "None" else ("%.2f %s" % (prec_range, units["prec"]))
    
    # Create the data list.
    data2 = [
        ["Lowest precipitation", prec_low],
        ["Highest precipitation", prec_high],
        ["Average precipitation", prec_avg],
        ["Median precipitation", prec_median],
        ["Range precipitation", prec_range],
        ["Total precipitation", "%.2f %s" % (prec_total, units["prec"])],
        ["Total rain", "%.2f %s" % (prec_total_rain, units["prec"])],
        ["Total snow", "%.2f %s" % (prec_total_snow, units["prec"])],
        ["Total hail", "%.2f %s" % (prec_total_hail, units["prec"])],
        ["Total sleet", "%.2f %s" % (prec_total_sleet, units["prec"])],
        ["Days with no precipitation", "%d day%s" % (prec_none, "" if prec_none == 1 else "s")],
        ["Days with rain", "%d day%s" % (prec_rain, "" if prec_rain == 1 else "s")],
        ["Days with snow", "%d day%s" % (prec_snow, "" if prec_snow == 1 else "s")],
        ["Days with hail", "%d day%s" % (prec_hail, "" if prec_hail == 1 else "s")],
        ["Days with sleet", "%d day%s" % (prec_sleet, "" if prec_sleet == 1 else "s")],
        ["Most common type of precipitation", "%s" % (prec_mode if prec_mode != "" else "None")]
    ]
    
    return data2


def wind_info(data, units):
    """Gets the wind info."""
    
    # Get the data.
    wind_data1, wind_data2 = datasets.split_list(datasets.get_column(data, 3))
    wind_data1 = datasets.none_to_zero(wind_data1)
    wind_data1 = datasets.convert_float(wind_data1)
    try:
        wind_low = min(wind_data1)
        wind_high = max(wind_data1)
        wind_avg = calculations.mean(wind_data1)
        wind_median = calculations.median(wind_data1)
        wind_range = calculations.range(wind_data1)
    except:
        wind_low = "None"
        wind_high = "None"
        wind_avg = "None"
        wind_median = "None"
        wind_range = "None"
    wind_mode = calculations.mode(wind_data2)
    
    # Change any values, if needed.
    wind_low = "None" if wind_low == "None" else ("%.2f %s" % (wind_low, units["wind"]))
    wind_high = "None" if wind_high == "None" else ("%.2f %s" % (wind_high, units["wind"]))
    wind_avg = "None" if wind_avg == "None" else ("%.2f %s" % (wind_avg, units["wind"]))
    wind_median = "None" if wind_median == "None" else ("%.2f %s" % (wind_median, units["wind"]))
    wind_range = "None" if wind_range == "None" else ("%.2f %s" % (wind_range, units["wind"]))
    
    # Create the data list.
    data2 = [
        ["Lowest wind speed", wind_low],
        ["Highest wind speed", wind_high],
        ["Average wind speed", wind_avg],
        ["Median wind speed", wind_median],
        ["Range of wind speeds", wind_range],
        ["Most common wind direction", "%s" % (wind_mode if wind_mode != "" else "None")]
    ]
    
    return data2


def humi_info(data, units):
    """Gets the humidity info."""
    
    # Get the data.
    humi_data = datasets.convert_float(datasets.get_column(data, 4))
    humi_low = min(humi_data)
    humi_high = max(humi_data)
    humi_avg = calculations.mean(humi_data)
    humi_median = calculations.median(humi_data)
    humi_range = calculations.range(humi_data)
    humi_mode = calculations.mode(humi_data)
    
    # Create the data list.
    data2 = [
        ["Lowest humidity", "%.2f%%" % humi_low],
        ["Highest humidity", "%.2f%%" % humi_high],
        ["Average humidity", "%.2f%%" % humi_avg],
        ["Median humidity", "%.2f%%" % humi_median],
        ["Range of humidity", "%.2f%%" % humi_range],
        ["Most common humidity", "%.2f%%" % humi_mode]
    ]
    
    return data2


def airp_info(data, units):
    """Gets the air pressure info."""
    
    # Get the data.
    airp_data1, airp_data2 = datasets.split_list(datasets.get_column(data, 5))
    airp_data1 = datasets.convert_float(airp_data1)
    airp_low = min(airp_data1)
    airp_high = max(airp_data1)
    airp_avg = calculations.mean(airp_data1)
    airp_median = calculations.median(airp_data1)
    airp_range = calculations.range(airp_data1)
    airp_mode = calculations.mode(airp_data1)
    airp_steady = 0
    airp_rising = 0
    airp_falling = 0
    for i in airp_data2:
        if i == "Steady":
            airp_steady += 1
        elif i == "Rising":
            airp_rising += 1
        elif i == "Falling":
            airp_falling += 1
    
    # Create the data list.
    data2 = [
        ["Lowest air pressure", "%.2f %s" % (airp_low, units["airp"])],
        ["Highest air pressure", "%.2f %s" % (airp_high, units["airp"])],
        ["Average air pressure", "%.2f %s" % (airp_avg, units["airp"])],
        ["Median air pressure", "%.2f %s" % (airp_median, units["airp"])],
        ["Range of air pressures", "%.2f %s" % (airp_range, units["airp"])],
        ["Most common air pressure", "%.2f %s" % (airp_mode, units["airp"])],
        ["Days with steady pressure", "%d day%s" % (airp_steady, "" if airp_steady == 1 else "s")],
        ["Days with rising pressure", "%d day%s" % (airp_rising, "" if airp_rising == 1 else "s")],
        ["Days with falling pressure", "%d day%s" % (airp_falling, "" if airp_falling == 1 else "s")]
    ]
    
    return data2


def clou_info(data, units):
    """Gets the cloud cover info."""
    
    # Get the data.
    # Put the items into a collection.
    clou_data = Counter(datasets.get_column(data, 6))
    # Find how many times the items appear.
    m_list = clou_data.most_common()
    # Convert the list to a dictionary.
    m_dict = {}
    for i in m_list:
        m_dict[i[0]] = i[1]
    
    # If any of the items don't appear, add dict items for them, with the values set to 0.
    if not "Sunny" in m_dict:
        m_dict["Sunny"] = 0
    if not "Mostly Sunny" in m_dict:
        m_dict["Mostly Sunny"] = 0
    if not "Partly Cloudy" in m_dict:
        m_dict["Partly Cloudy"] = 0
    if not "Mostly Cloudy" in m_dict:
        m_dict["Mostly Cloudy"] = 0
    if not "Cloudy" in m_dict:
        m_dict["Cloudy"] = 0
    
    # Create the data list.
    data2 = [
        ["Days sunny", "%s day%s" % (m_dict["Sunny"], "" if m_dict["Sunny"] == 1 else "s")],
        ["Days mostly sunny", "%s day%s" % (m_dict["Mostly Sunny"], "" if m_dict["Mostly Sunny"] == 1 else "s")],
        ["Days partly cloudy", "%s day%s" % (m_dict["Partly Cloudy"], "" if m_dict["Partly Cloudy"] == 1 else "s")],
        ["Days mostly cloudy", "%s day%s" % (m_dict["Mostly Cloudy"], "" if m_dict["Mostly Cloudy"] == 1 else "s")],
        ["Days cloudy", "%s day%s" % (m_dict["Cloudy"], "" if m_dict["Cloudy"] == 1 else "s")]
    ]
    
    return data2


def note_info(data, units):
    """Gets the notes info."""
    
    # Get the data.
    data2 = []
    
    # Loop through the list, appending the dates and notes.
    for i in range(0, len(data)):
        if data[i][7] != "":
            data2.append([data[i][0], data[i][7]])
    
    return data2
