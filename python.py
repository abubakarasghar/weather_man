import numpy as np
from pathlib import Path
import calendar
from colorama import Fore
import os


def clear():
    os.system("cls")


def city_name():
    city1_input = input('''
                       LAHORE
                       MURREE
                       DUBAI
                       Type one of the above city to check the weather of: ''')
    clear()
    city_input = city1_input.upper()
    if city_input == "LAHORE":
        open_file = "weather_man\lahore_weather"
    elif city_input == "MURREE":
        open_file = "weather_man\Murree_weather"
    elif city_input == "DUBAI":
        open_file = "weather_man\Dubai_weather"
    else:
        print("you enter invalid city")
    return (open_file)


def select_option():
    select_input1 = input('''
                  Highest temperature and day
                  Average highest temperature
                  Lowest and Highest temperature on each day
                  Type H , A or L: ''')
    clear()
    select_input = select_input1.upper()
    select = ""
    if select_input == "H":
        select = "high_temp"
    elif select_input == "A":
        select = "average_temp1"
    elif select_input == "L":
        select = "horizontal_bar"
    return (select)


file_path = city_name()
select_method = select_option()
year_input = input("Enter the year of the weather you want to know: ")
clear()


def average_temp2(data):
    max_avg = []
    min_avg = []
    humid_avg = []

    for i in data:
        if i[1] != "":
            max_avg.append(int(i[1]))
            min_avg.append(int(i[3]))
            humid_avg.append(int(i[7]))
    max_temp_avg = int(np.sum(max_avg)/len(max_avg))
    min_temp_avg = int(np.sum(min_avg)/len(min_avg))
    max_humid_avg = int(np.sum(humid_avg)/len(humid_avg))
    return max_temp_avg, min_temp_avg, max_humid_avg


def highest_temp(data1):
    high_temp = []
    lowest_temp = []
    humidty = []

    for i in data1:
        if i[1] != "":
            high_temp.append(int(i[1]))
            lowest_temp.append(int(i[3]))
            humidty.append(int(i[7]))
    max_temp_avg1 = np.max(high_temp)
    min_temp_avg1 = np.min(lowest_temp)
    max_humid_avg1 = np.max(humidty)
    for i in data1:
        if i[1] != "" and int(i[1]) == max_temp_avg1:
            max_date = i[0]
        if i[3] != "" and int(i[3]) == min_temp_avg1:
            min_date = i[0]
        if i[3] != "" and int(i[7]) == max_humid_avg1:
            humid_date = i[0]
    return max_temp_avg1, max_date, min_temp_avg1, min_date, max_humid_avg1, humid_date


def max_min(data1):
    max_daily = []
    min_daily = []
    date_daily = []
    for data in data1:
        if data[1] != "":
            max_daily.append(int(data[1]))
            min_daily.append(int(data[3]))
            date_daily.append(data[0])
    return max_daily, min_daily, date_daily


def data_cleaning(files):
    local_list = []
    for file in files:
        data_file = open(file, 'r')
        data = data_file.read().splitlines()

        if "Max" in data[0]:
            data.pop(0)
        elif "Max" in data[1]:
            data.pop(0)
            data.pop(0)
        if "<!--" in data[-1]:
            data.pop()
        else:
            pass
        for element in data:
            local_list.append(element.split(','))
    return local_list


def fun(choose):
    try:
        year = year_input
        if choose == "high_temp":
            file = Path(file_path).rglob(
                '*{date}*.txt'.format(date=year_input))
            highest_result = highest_temp(data_cleaning(file))
            max_month = calendar.month_name[int(
                highest_result[1].split('-')[1])]
            min_month = calendar.month_name[int(
                highest_result[3].split('-')[1])]
            min_day = int(highest_result[3].split('-')[2])
            humid_month = calendar.month_name[int(
                highest_result[5].split('-')[1])]
            humid_day = int(highest_result[5].split('-')[2])
            print("Highest: " + str(highest_result[0])+"C on ", end="")
            print(str(max_month)+' ' +
                  str(int(highest_result[1].split('-')[2])))
            print(
                "Lowest:  " + str(highest_result[2])+"C on "+str(min_month)+" "+str(min_day))
            print(
                "Humid:   " + str(highest_result[4])+"% on "+str(humid_month)+" "+str(humid_day))
        elif choose == "average_temp1":
            month = input("Enter the month like jan,aug,dec: ")
            month = month[:1].upper() + month[1:3].lower()
            file = Path(file_path).rglob(
                '*{date}_{month}.txt'.format(date=year, month=month))
            average_temp = average_temp2(data_cleaning(file))
            print("Highest Average: " + str(average_temp[0])+"C")
            print("Lowest Average:  " + str(average_temp[1])+"C")
            print("Humid Average:   " + str(average_temp[2])+"%")
        elif choose == "horizontal_bar":
            month = input("Enter the month like jan,aug,dec: ")
            month = month[:1].upper() + month[1:3].lower()
            file = Path(file_path).rglob(
                '*{date}_{month}.txt'.format(date=year, month=month))
            values = max_min(data_cleaning(file))
            for i in range(len(values[1])):
                _v = values[2][i].split('-')[2]
                print(_v, end="")
                for _x in range(int(values[0][i])):
                    print(Fore.RED, "+", end="")
                print()
                print(Fore.WHITE, _v, end="")
                for _x in range(int(values[1][i])):
                    print(Fore.BLUE, "+", end="")
                print(Fore.WHITE, str(values[0][i])+"-"+str(values[1][i]))
    except ValueError:
        print("Please enter right information")

fun(select_method)
