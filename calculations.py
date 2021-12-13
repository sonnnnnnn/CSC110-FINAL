"""CSC110 Fall 2021 Project, Calculations

Description
===============================
The calculations file reads and transforms data from the dataset, forming a complete list of Industry objects.
It computes all the rates and potential scores seen in the Industry dataclass.

Assumptions
===============================
We made a few assumptions (that are also mentioned below):
- COVID-19 restrictions are completely over starting 2023

Copyright and Usage Information
===============================

This file is provided solely for the use of TAs
marking CSC110 projects at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult us at our email addresses.

This file is Copyright (c) 2021 Juhwan Son, Defne Altiok, Aliyah James, and Rohma Daud.
"""

import csv
import helpers
from helpers import JobMarket

# Global variables -- NOT THE BEST PRACTICE, SOMEHOW FIND BETTER WAY
# A JobMarket object that holds the results of all of our computations
CANADA = JobMarket('Canada', helpers.Rates([], [], []), [])

# Unmployment rate calculations
def average_unemployment_rate(rates: list[float]) -> float:
    """ Return the average unemployment rate based on a list of rates.

    Preconditions:
        - {type(rate) == type(0.4) for rate in rates}

     >>> average_unemployment_rate()

    """
    return sum(rates) / len(rates)


def rates_without_COVID(rates: list[float]) -> list[float]:
    """ Return the predicted unemployment rate in 2020 and 2021 based on unemployment rate before COVID-19
    using arithmetic mean method.

    Preconditions:
        - len(rates) >= 1
    """

    rate2020 = average_unemployment_rate(rates)
    rate2021 = (sum(rates) + rate2020 - rates[0]) / (len(rates))

    return [rate2020, rate2021]


def predicted_rates(rates: list[float]) -> list[float]:
    """ Return the predicted unemployment rate between 2022 and 2024 based on
    past six years' unemployment rate data.
    >>> rates_2016to2021 = [6.4, 5.5, 5.2, 5.5, 8, 5.6]
    >>> predicted_rates(rates_2016to2021)
    [6.03, 5.97, 6.05]
    """
    rate2022 = float(round((sum(rates) / len(rates)), 2))
    rate2023 = float(round((sum(rates) + rate2022 - rates[0]) / (len(rates)), 2))
    rate2024 = float(round((sum(rates) + rate2022 + rate2023 - rates[0] - rates[1]) / (len(rates)), 2))

    return [rate2022, rate2023, rate2024]


# Calculations related to factors that affect unemployment
def calculate_COVID_impact() -> int:
    """
    f
    """

    return 0


def calculate_remote_work_potential() -> int:
    """
    d
    """

    return 0


def calculate_recovery_potential() -> int:
    """
    d
    """

    return 0


# Reading from datasets
def read_data(filenames: list) -> JobMarket:
    """"""
    country_data = read_national_data(filenames[0])
    industries = read_industry_data(filenames[1])
    return JobMarket('Canada', country_data, industries)

def read_national_data(filename: str) -> helpers.Rates:
    """Return the data stored in the given file.

    The file is a CSV file with two columns, one columns gives the month and year while the other gives the unemployment
    rate. These files are based on real  data from the Canadian Government.
    """
    # ACCUMULATOR data_output: The Unemployment parsed from file so far
    data_output = []
    with open(filename) as file:
        reader = csv.reader(file)

        # Skip header row
        next(reader)
        data = [row for row in reader if len(row) == 2]  # Length of each row is 2 ; Skips last row
        # for row in data:
        # data_output += [Unemployment(row[0], float(row[1]))]
        for row in data:
            row[1] = float(row[1])
    # return data
    return helpers.Rates([], [], [])


def read_industry_data(filename: str) -> list[helpers.Industry]:
    """Return the data stored in the given file.

    The file is a CSV file with two columns, one columns gives the month and year while the other gives the unemployment
    rate. These files are based on real  data from the Canadian Government.
    """
    # ACCUMULATOR data_output: The Unemployment parsed from file so far
    data_output = []
    with open(filename) as file:
        reader = csv.reader(file)

        # Skip header row
        next(reader)
        data = [row for row in reader if len(row) == 2]  # Length of each row is 2 ; Skips last row
        # for row in data:
        # data_output += [Unemployment(row[0], float(row[1]))]
        for row in data:
            row[1] = float(row[1])
    #return data
    return []
