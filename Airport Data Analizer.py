"""
****************************************************************************
Student ID: [20240761]
Date: [02-07-2025]
****************************************************************************
"""
import math
from graphics import *
import csv

# Global list to hold CSV data
data_list = []

# Dictionary of valid airport codes and their names
valid_airport_codes = {
    'LHR': 'London Heathrow', 'MAD': 'Madrid Adolfo Suárez-Barajas',
    'CDG': 'Charles De Gaulle International', 'IST': 'Istanbul Airport International',
    'AMS': 'Amsterdam Schiphol', 'LIS': 'Lisbon Portela',
    'FRA': 'Frankfurt Main', 'FCO': 'Rome Fiumicino',
    'MUC': 'Munich International', 'BCN': 'Barcelona International'
}

# Dictionary of valid airline codes and their names
valid_airlines = {
    'BA': 'British Airways', 'AF': 'Air France', 'AY': 'Finnair', 'KL': 'KLM',
    'SK': 'Scandinavian Airlines', 'TP': 'TAP Air Portugal', 'TK': 'Turkish Airlines',
    'W6': 'Wizz Air', 'U2': 'easyJet', 'FR': 'Ryanair', 'A3': 'Aegean Airlines',
    'SN': 'Brussels Airlines', 'EK': 'Emirates', 'QR': 'Qatar Airways',
    'IB': 'Iberia', 'LH': 'Lufthansa'
}

def load_csv(CSV_chosen):
    """
    Loads any CSV file by name into the list 'data_list'.
    """
    data_list.clear()
    with open(CSV_chosen, 'r') as file:
        csvreader = csv.reader(file)
        next(csvreader)  # Skip the header row
        for row in csvreader:
            data_list.append(row)

def get_valid_city():
    """
    Prompt for a valid 3-letter city code.
    """
    while True:
        city = input("Please enter the three-letter code for the departure city required: ").strip().upper()
        if len(city) != 3:
            print("Wrong code length - please enter a three-letter city code.")
        elif city not in valid_airport_codes:
            print("Unavailable city code - please enter a valid city code.")
        else:
            return city

def get_valid_year():
    """
    Prompt for a valid year between 2000 and 2025.
    """
    while True:
        year_input = input("Please enter the year required in the format YYYY: ").strip()
        if not year_input.isdigit() or len(year_input) != 4:
            print("Wrong data type - please enter a four-digit year value.")
        elif not 2000 <= int(year_input) <= 2025:
            print("Out of range - please enter a value from 2000 to 2025.")
        else:
            return year_input

def calculate_statistics():
    """
    Analyze data in data_list and return all required statistics as a tuple.
    """
    total = len(data_list)
    runway_1 = 0
    over_500 = 0
    ba_count = 0
    rain_count = 0
    delay_count = 0
    rain_hours = set()
    destination_counts = {}

    for row in data_list:
        flight = row[1]
        sched_dep = row[2]
        actual_dep = row[3]
        destination = row[4]
        distance = int(row[5])
        runway = row[8]
        weather = row[9].lower()

        if runway == '1':
            runway_1 += 1
        if distance > 500:
            over_500 += 1
        if flight.startswith('BA'):
            ba_count += 1
        if "rain" in weather:
            rain_count += 1
            rain_hours.add(sched_dep.split(":")[0])
        if sched_dep != actual_dep:
            delay_count += 1
        destination_counts[destination] = destination_counts.get(destination, 0) + 1

    avg_hour = round(total / 12, 2)
    af_count = sum(1 for row in data_list if row[1].startswith("AF"))
    af_percent = round((af_count / total) * 100, 2)
    delay_percent = round((delay_count / total) * 100, 2)
    max_count = max(destination_counts.values())
    most_common_dest = [valid_airport_codes.get(code, code) for code, count in destination_counts.items() if count == max_count]

    return (total, runway_1, over_500, ba_count, rain_count, avg_hour, af_percent, delay_percent, len(rain_hours), most_common_dest)

def print_results(city, year, results):
    """
    Print the analysis results to the python shell window.
    """
    print("********************************************************************")
    print(f"File {city}{year}.csv selected - Planes departing {valid_airport_codes[city]} {year}.")
    print("********************************************************************")
    print(f"The total number of flights from this airport was {results[0]}")
    print(f"The total number of flights departing Runway one was {results[1]}")
    print(f"The total number of departures of flights over 500 miles was {results[2]}")
    print(f"There were {results[3]} British Airways flights from this airport")
    print(f"There were {results[4]} flights from this airport departing in rain")
    print(f"There was an average of {results[5]} flights per hour from this airport")
    print(f"Air France planes made up {results[6]}% of all departures")
    print(f"{results[7]}% of all departures were delayed")
    print(f"There were {results[8]} hours in which rain fell")
    print(f"The most common destinations are {results[9]}")

def save_results(city, year, results):
    """
    Save the results into results.txt file.
    """
    with open("results.txt", "a") as file:
        file.write(f"\nFile {city}{year}.csv - Planes departing {valid_airport_codes[city]} {year}\n")
        file.write(f"The total number of flights from this airport was {results[0]}\n")
        file.write(f"The total number of flights departing Runway one was {results[1]}\n")
        file.write(f"The total number of departures of flights over 500 miles was {results[2]}\n")
        file.write(f"There were {results[3]} British Airways flights from this airport\n")
        file.write(f"There were {results[4]} flights from this airport departing in rain\n")
        file.write(f"There was an average of {results[5]} flights per hour from this airport\n")
        file.write(f"Air France planes made up {results[6]}% of all departuresn\n")
        file.write(f"{results[7]}% of all departures were delayed\n")
        file.write(f"There were {results[8]} hours in which rain fell\n")
        file.write(f"The most common destinations are {results[9]}\n")

def draw_histogram(airline_code, city, year):
    """
    Draw histogram of flight departures for the selected airline using graphics.py.
    """
    win = GraphWin(f"{valid_airlines[airline_code]} Histogram", 800, 400)
    hour_counts = [0] * 12

    for row in data_list:
        if row[1].startswith(airline_code):
            hour = int(row[2].split(":")[0])
            hour_counts[hour] += 1

    max_val = max(hour_counts)
    for i in range(12):
        x1 = 50 + i * 60
        height_per_unit=350/max_val
        y1 = 350 - (hour_counts[i] * 15)
        x2 = x1 + 40
        y2 = 350

        bar = Rectangle(Point(x1, y1), Point(x2, y2))
        bar.setFill("blue")
        bar.draw(win)

        label = Text(Point((x1 + x2) / 2, 360), str(i))
        label.draw(win)

        value = Text(Point((x1 + x2) / 2, y1 - 10), str(hour_counts[i]))
        value.setSize(8)
        value.draw(win)

    title = Text(Point(400, 20), f"{valid_airlines[airline_code]} Flights from {city} - {year}")
    title.setSize(14)
    title.draw(win)

    Bar_line=Line(Point(50,350), Point(750,350))
    Bar_line.setFill("black")
    Bar_line.draw(win)
    

    below_title=Text(Point(400,385),"Hours 00.00 to 11.00")
    below_title.setSize(12)
    below_title.draw(win)
    

    win.getMouse()
    win.close()

def main():
    """
    Main loop of the program.
    """
    while True:
        city = get_valid_city()
        year = get_valid_year()
        selected_data_file = f"{city}{year}.csv"
        try:
            load_csv(selected_data_file)
        except FileNotFoundError as F:
            print("********************************************************************")
            print(f"File {city}{year}.csv selected - Planes departing {valid_airport_codes[city]} {year}.")
            print("********************************************************************")
            main()


        results = calculate_statistics()
        print_results(city, year, results)
        save_results(city, year, results)

        while True:
            airline_code = input("Enter a two-character Airline code to plot a histogram: ").strip().upper()
            if airline_code in valid_airlines:
                try:
                    draw_histogram(airline_code,valid_airport_codes[city], year)
                except GraphicsError:
                    print("")
                break
            else:
                print("Unavailable Airline code please try again.")

        repeat = input("Do you want to select a new data file? Y/N: ").strip().upper()
        if repeat != 'Y':
            print("Thank you. End of run.")
            break

# Run the program
main()
