# covid_stats.py
# CHANTAE H, ENDG 233 Fall 2021
# Developed Nov. 2021

# Program that calculates vaccination rates and finds the number of Covid cases
# on a date chosen by the user. Uses matplotlib to display 2 bar graphs for above
# 2 statistics. Uses numpy arrays to import data from 3 datasets and compute calculations. 

# csv files are modified from datasets on Edmonton Open Data. See README file for more info.

import numpy as np
import matplotlib.pyplot as plt

class HealthZone:
    """Class that creates a HealthZone object for a health zone in Alberta

    Attributes:
        zone_num (int): Integer that represents the zone
        zone_name (string): String of the zone's name
        population (int): Integer representing the population of that zone
        case_num (int): Integer representing the number of Covid cases in that zone
        dose_1_rate (float): Percent of 1st vaccine doses administered out of zone's population
        dose_2_rate (float): Percent of 2nd vaccine doses administered out of zone's population
    """

    def __init__(self, zone_num, zone_name, population):
        self.zone_num = zone_num
        self.zone_name = zone_name
        self.population = population
        self.case_num = 0
        self.dose_1_rate = None
        self.dose_2_rate = None

    # instance methods
    def calc_vacc_rate(self, vacc_data):
        """Function that calculates the vaccination rate as a percentage

        Params:
            vacc_data (int): Number of vaccine doses administered

        Returns:
            vacc_rate (float): Percent of population that is vaccinated
        """
        vacc_rate = (vacc_data / self.population) * 100
        return vacc_rate

    def add_case(self):
        """Function that increments the Covid case number"""
        self.case_num += 1
    
    def set_vacc_rates(self, dose_1_rate, dose_2_rate):
        """Function that sets values of dose 1 and 2 vaccination rate attributes

        Params:
            dose_1_rate (float): Float representing vaccine 1st dose uptake rate
            dose_2_rate (float): Float representing vaccine 2nd dose uptake rate

        Returns: None
        """
        self.dose_1_rate = dose_1_rate
        self.dose_2_rate = dose_2_rate

    def get_zone_name(self):
        """Function that returns the name of the zone

        Returns:
            (string): String representing the zone's name
        """
        return self.zone_name
    
    def get_zone_num(self):
        """Function that returns the zone's number

        Returns:
            (int): Integer representing the zone's number
        """
        return self.zone_num

    def get_d1_rate(self):
        """Function that returns the zone's dose 1 uptake rate

        Returns:
            (float): Float representing vaccine 1st dose uptake rate
        """
        return self.dose_1_rate
    
    def get_d2_rate(self):
        """Function that returns the zone's dose 2 uptake rate

        Returns:
            (float): Float representing vaccine 2nd dose uptake rate
        """
        return self.dose_2_rate
    
    def get_case_num(self):
        """Function that returns the number of Covid cases in the zone

        Returns:
            (int): Integer representing the number of Covid cases in that zone
        """
        return self.case_num

  
def print_date(month, day):
    """Function that prints the date, formatted

    Params:
        month (int): Integer representing the month chosen by the user
        day (int): Integer representing the day chosen by the user
    
    Returns: None
    """
    print("Chosen date: {}/{}/2021".format(month, day))
    
def get_date_input(valid_months, months_dict, vaccinations, DAY_COL):
    """Function that gets valid date input from ths user

    Params:
        valid_months (list): List of the months that user can choose from
        months_dict (dict): Dictionary of months and their lengths
        vaccinations (array): Array of vaccination data
        DAY_COL (int): Integer of column corresponding to the day in the array

    Raises:
        IndexError: If month input given is not in valid_months list
        IndexError: If day input is out of bounds

    Returns:
        month (int): Numerical month chosen by user
        day (int): Numerical day chosen by user
    """
    
    # loop to prompt user to input valid month choice
    while True:
        print("Please enter a numerical month, from", valid_months[0], "to", valid_months[-1], "here:")
        try:
            month = int(input())
            # raise an exception if month is invalid
            if month not in valid_months:
                raise IndexError
        except ValueError:  # if user does not enter an integer
            print("That is not an integer value.\n")
            continue
        except IndexError:
            print("That is not a valid month.\n")
            continue
        break
    
    # loop until get valid user input for day
    while True:
        # if the month is the most recent month, then there is a minimum day that must be set
        if month == valid_months[0]:
            min_day = int(vaccinations[-1][DAY_COL])
        else:
            # otherwise, set the minimum day as 1
            min_day = 1
        max_day = months_dict[month]
    
        print("\nPlease enter a numerical day ({}-{}) from {} here:".format(min_day, max_day, month))
        try:
            day = int(input())
            # raise an exception if day is invalid
            if not (min_day <= day <= max_day):
                raise IndexError 
        except ValueError:  # if user does not enter an integer
            print("That is not an integer value.")
            continue
        except IndexError:
            print("That is not a valid day.")
            continue
        break
    return month, day

def calc_max_vrate(dose_num, zone_vacc_rates, zone_objs):
    """Function that determines the zone with the highest vaccination rate

    Params:
        dose_num (int): Integer of dose number (1 or 2)
        zone_vacc_rates (array): 2D Array of dose 1 and 2 vaccination rates for all zones
        zone_objs (list): List of HealthZone objects
    """
    # Dose number determines which part of the zone_vacc_rates array we look at
    if dose_num == 1: 
        index = 0
    else:
        index = 1
    
    # Numpy max method finds highest vacc. rate
    max_rate = np.max(zone_vacc_rates[:,index])
    # loop through HealthZone objects to find the one that corresponds with the max_rate
    for zone in zone_objs:
        if dose_num == 1:
            dose_rate = zone.get_d1_rate()
        else:
            dose_rate = zone.get_d2_rate()
        if dose_rate == max_rate:
            print("Highest vaccine dose {} uptake is {}% in the {}.".format(dose_num, max_rate, zone.get_zone_name()))
            break

def main():
    MONTH_COL = 0
    DAY_COL = 1

    # welcome user to program
    print("Welcome to the Covid stats program!\nI will calculate vaccination rates and find the number of Covid cases for a date you specify in 2021.")

    # import data using numpy arrays
    vaccinations = np.genfromtxt("AB_vaccinations.csv", delimiter = ",", skip_header = True, usecols = (1, 2, 3, 4, 5))
    populations = np.genfromtxt("AB_population.csv", delimiter = ",", skip_header = True, usecols = (1, 2, 3, 4))
    covid_cases = np.genfromtxt("AB_COVID_cases.csv", delimiter = ",", skip_header = True, usecols = (1, 2, 3, 4))

    # Initialize list with valid months taken from dataset starting and ending dates
    valid_months = [ x for x in range(int(vaccinations[-1][MONTH_COL]), int(vaccinations[0][MONTH_COL] + 1))]
    
    month_lengths = {1: 31, 2: 28, 3: 31, 4: 30, 5: 31, 6: 30, 7: 31, 8: 31, 9: 30, 10: 31, 11: 30, 12: 31}
    zones_dict = {0: "Calgary Zone", 1: "Central Zone", 2: "Edmonton Zone", 3: "North Zone", 4: "South Zone"}

    # Set bounds based on where data ends
    month_lengths[vaccinations[0][MONTH_COL]] = int(vaccinations[0][DAY_COL])
    
    # Create a dictionary of valid months and days to choose from
    months_dict = { month: month_lengths[month] for month in valid_months }

    # Call function to get valid date input
    month, day = get_date_input(valid_months, months_dict, vaccinations, DAY_COL)
    
    # User chooses stats for one zone or for all of AB
    print("\nWould you like stats for one zone in Alberta, or stats for all of Alberta?")
    print("1  Stats for one zone")
    print("2  Stats for all of Alberta")
    
    valid_choice = False
    
    # loop until user's input is valid
    while not valid_choice:
        location = input("Enter your choice (1 or 2) here: ")
        
        try:
            location = int(location)
        except ValueError:  # ValueError raised if an integer is not inputted
            print("Please enter a numerical value.\n")
            continue
        
        if not ((location == 1) or (location == 2)):
            print("That number is out of bounds.\n")
        else:
            if location == 1:
                while True:
                    print("\nSelect a zone from below:")
                    print("0 ", zones_dict[0])
                    print("1 ", zones_dict[1])
                    print("2 ", zones_dict[2])
                    print("3 ", zones_dict[3])
                    print("4 ", zones_dict[4])

                    zone = input("Enter your selection here: ")
                    try:
                        zone = int(zone)
                    except ValueError:  # ValueError raised if input values isn't an integer
                        print("Please enter a numerical value.")
                        continue
                    
                    if 0 <= zone <= 4:
                        location = zone
                        break
                    else:
                        print("That number is out of bounds.")
            else:
                location = 5    # if user chooses stats for all Alberta, set location to 5
                    
            valid_choice = True
        
    print("\nChosen date: {}/{}/2021".format(month, day))
    if 0 <= location <= 4:
        print("Chosen location:", zones_dict[location])
    else:
        print("Chosen location: All of Alberta")


    valid_date = False
    while not valid_date:
        valid_date = True
        # get rows that contain the number of the chosen month in any column
        filtered_rows = np.where(populations == month)
        temp_data = []
        temp_indexes = []

        # Find rows with correct date
        for row in filtered_rows[0]:
            if (populations[row][MONTH_COL] == month) and (populations[row][DAY_COL] == day):
                temp_data.append(populations[row])
                temp_indexes.append(row)

        indexes = []
       
        # find array indexes (i.e. row) of specified date and zone of vaccination numbers and population data
        if len(temp_indexes) != 0:
            indexes = [temp_indexes[0]]

            # filter out duplicate values if any exist
            pop_data = [temp_data[0]]
            for i in range(1, len(temp_data)):
                if temp_data[i][3] != temp_data[i-1][3]:
                    # Add values from temp lists to pop_data and indexes lists
                    pop_data.append(temp_data[i])
                    indexes.append(temp_indexes[i])
                else:
                    i += 1
            pop_data = np.array(pop_data)
        else:
            # If there are no indexes where that date is found, there is no data for that date
            # Prompt user to re-input date
            print("Sorry, there's no data available for that date. Please choose another date.")
            month, day = get_date_input(valid_months, months_dict, vaccinations, DAY_COL)
            print_date(month, day)

            valid_date = False
    
    # Calculate vacc. rates for doses 1 and 2
    vacc_data = np.array(vaccinations[indexes[0]:indexes[-1]+1])
    
    # if location chosen is a zone
    if location < 5:
        # Display stats to terminal
        zone_pop = int(pop_data[location][3])
        print("Population in the {}: {}".format(zones_dict[location], zone_pop))

        # Create HealthZone object
        zone1 = HealthZone(location, zones_dict[location], zone_pop)
        print("\n---- Vaccination Rate Statistics for", zone1.get_zone_name(), "----")
        print("1st Dose Uptake: {:.2f}%".format(zone1.calc_vacc_rate(vacc_data[location][3])))
        print("2nd Dose Uptake: {:.2f}%".format(zone1.calc_vacc_rate(vacc_data[location][4])))
        print()

        # Create list of HealthZone objects for each zone in Alberta
        zone_objs = [ HealthZone(zone_num, zones_dict[zone_num], int(pop_data[zone_num][3])) for zone_num in range(len(zones_dict))]
        zone_vacc_rates = []
        # calculate and set vaccination rates for each zone
        for zone in zone_objs:
            dose_1_rate = round(zone.calc_vacc_rate(vacc_data[zone.get_zone_num()][3]), 2)
            dose_2_rate = round(zone.calc_vacc_rate(vacc_data[zone.get_zone_num()][4]), 2)
            zone_vacc_rates.append([dose_1_rate, dose_2_rate])
            zone.set_vacc_rates(dose_1_rate, dose_2_rate)
        zone_vacc_rates = np.array(zone_vacc_rates)

        # create arrays of dose 1 and dose 2 vaccine uptake rates
        dose_1_list = []
        dose_2_list = []
        for row in zone_vacc_rates:
            dose_1_list.append(row[0])
            dose_2_list.append(row[1])
        dose_1_arr = np.array(dose_1_list)
        dose_2_arr = np.array(dose_2_list)
    else:   # if location chosen is all Alberta
        # Display stats to terminal
        ab_pop = 0
        for i in range(0, len(zones_dict)):
            ab_pop += pop_data[i][3]
        print("Population in all Alberta:", int(ab_pop))
        print("\n---- Vaccination Rate Statistics ----")
        print("(percentage of population vaccinated by zone)")
        # Create list of HealthZone objects
        zone_objs = [ HealthZone(zone_num, zones_dict[zone_num], int(pop_data[zone_num][3])) for zone_num in range(len(zones_dict))]
        zone_vacc_rates = []
        # Calculate and set values of zone vaccine uptake rates
        for zone in zone_objs:
            print("\n{}".format(zone.get_zone_name()))
            dose_1_rate = round(zone.calc_vacc_rate(vacc_data[zone.get_zone_num()][3]), 2)
            print("1st Dose Uptake: {:.2f}%".format(dose_1_rate))
            dose_2_rate = round(zone.calc_vacc_rate(vacc_data[zone.get_zone_num()][4]), 2)
            print("2nd Dose Uptake: {:.2f}%".format(dose_2_rate))
            zone_vacc_rates.append([dose_1_rate, dose_2_rate])
            zone.set_vacc_rates(dose_1_rate, dose_2_rate)
        zone_vacc_rates = np.array(zone_vacc_rates)
        print("--------------------\n")

        # Call functions to print zones with max vacc. rates for both doses
        calc_max_vrate(1, zone_vacc_rates, zone_objs)
        calc_max_vrate(2, zone_vacc_rates, zone_objs)

        # Create arrays of dose 1 and 2 uptake rates
        dose_1_list = []
        dose_2_list = []
        for row in zone_vacc_rates:
            dose_1_list.append(row[0])
            dose_2_list.append(row[1])
        dose_1_arr = np.array(dose_1_list)
        dose_2_arr = np.array(dose_2_list)

        # Take weighted averages of calculated vacc. rates to find overall vacc. rates for all of AB
        pop_weights = [ (pop_data[zone][3] / ab_pop) for zone in zones_dict ]        
        ab_dose_1 = np.sum(pop_weights * dose_1_arr)
        ab_dose_2 = np.sum(pop_weights * dose_2_arr)
        print("\nAll of AB dose 1 uptake: {}%".format(round(ab_dose_1, 2)))
        print("All of AB dose 2 uptake: {}%".format(round(ab_dose_2, 2)))
    
    # Plot figure (bar graph) of vaccination rate by zone 
    x_locations = np.array([1, 2, 3, 4, 5])
    width = 0.35
    plt.bar(x_locations, dose_1_arr, width, color = "lightgreen", label = "Dose 1")
    plt.bar(x_locations + width, dose_2_arr, width, color = "skyblue", label = "Dose 2")
    plt.ylabel("Vaccination Rates")
    plt.xticks(x_locations + (width / 2), zones_dict.values())
    plt.title("AB Vaccination Rate by Zone ({}/{}/2021)".format(month, day))
    plt.legend()


    # For covid case stats, find number of rows in covid case data with specified date. 
    # get rows that contain the number of the chosen month in any column
    covid_rows = np.where(covid_cases == month)
    temp_c_indexes = []

    # Finds rows where dates are correct
    for row in covid_rows[0]:
        if (covid_cases[row][MONTH_COL] == month) and (covid_cases[row][DAY_COL] == day):
            temp_c_indexes.append(row)

    covid_indexes = temp_c_indexes
    # filter duplicates out of list of indexes
    covid_indexes = set(covid_indexes)

    # put data into array
    ab_covid_data = []
    for index in covid_indexes:
        ab_covid_data.append(covid_cases[index])
    ab_covid_data = np.array(ab_covid_data)
    print("--------------------")
    print("\nOn {}/{}/2021, there were {} recorded Covid cases in Alberta.".format(month, day, len(ab_covid_data)))

    # loop through each covid case and add the case to the corresponding HealthZone object
    for case in ab_covid_data:
        case_zone = int(case[2])
        zone_objs[case_zone].add_case()

    # Put number of cases per zone into a numpy array and find zone with max number of cases
    case_count_list = [ zone.get_case_num() for zone in zone_objs]
    case_count_arr = np.array(case_count_list)
    max_count = np.max(case_count_arr)
    print("The zone with the highest number of cases on that date is the {}, at {} cases.".format(zones_dict[case_count_list.index(max_count)], max_count))

    # Plot figure of number of Covid cases per zone 
    plt.figure()
    plt.title("Number of Covid Cases in AB per Zone ({}/{}/2021)".format(month, day))
    plt.ylabel("Number of Cases")
    plt.bar(zones_dict.values(), case_count_list, color="lightpink")

    # Show plots
    plt.show()
    

if __name__ == "__main__":
    main()