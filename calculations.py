"""CSC110 Fall 2021 Project, Calculations

Description
===============================
The calculations file reads and transforms data from the dataset, forming a complete list of Industry objects.
It computes all the rates and potential scores seen in the Industry dataclass.

Short-forms:
ur = unemployment rate
rwps = remote work potential score
ci = covid-19 impact

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
import system
from system import JobMarket
import numpy as np

# Global variables -- NOT THE BEST PRACTICE, SOMEHOW FIND BETTER WAY
# A JobMarket object that holds the results of all of our computations
CANADA = JobMarket('Canada', system.Rates([], [], []), [])

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
    rate2021 = (sum(rates) + rate2020) / (len(rates) + 1)

    return [rate2020, rate2021]


def predicted_rates(rates: list[float]) -> list[float]:
    """ Return the predicted unemployment rate between 2022 and 2024 based on
    unemployment rate data between 2017 and 2021.

    """
    rate2022 = sum(rates) / len(rates)
    rate2023 = (sum(rates) + rate2022) / (len(rates) + 1)
    rate2024 = (sum(rates) + rate2022 + rate2023) / (len(rates) + 2)

    return [rate2022, rate2023, rate2024]


# Calculations related to factors that affect unemployment
def calculate_ci(rates: list[float]) -> int:
    """
    f
    """
    avg_ur_before = (rates[0] + rates[1] + rates[2]) // 3
    avg_ur_after = (rates[3] + rates[4]) // 2

    ur_difference = abs(avg_ur_after - avg_ur_before)

    if ur_difference < 0.5:
        return 1
    elif ur_difference < 1.0:
        return 2

    return 3


def calculate_rwps(name: str) -> int:
    """
    d - FIX SCORING
    """
    index = system.name_to_int(name)
    data = system.SUCCESS_FACTORS[index]

    score = sum([data[i] for i in range(0, 4)]) // 4

    if data[4]:
        if data[5]:
            return score
        else:
            return (score + 100) // 2
    else:
        return score


# Reading from datasets
def read_data() -> JobMarket:
    """"""
    country_data = read_national_data()
    industries = read_industry_data()
    return JobMarket('Canada', country_data, industries)


def read_national_data() -> system.Rates:
    """Return the data stored in the given file.
    The file is a CSV file with two columns, one columns gives the month and year while the other gives the unemployment
    rate. These files are based on real  data from the Canadian Government.
    """

    rates = [6.4, 5.5, 5.2, 5.5, 8, 5.6]
    national_data = system.Rates(unemployment_rates=rates, predicted_rates=predicted_rates(rates),
                                 rates_without_COVID=rates_without_COVID(rates))
    return national_data


def read_industry_data() -> list[list]:
    """Return the data stored in the given file.
    The file is a CSV file with seven columns, one columns gives industries while the other six give the number of
    employment between 2016 and 2021. These files are based on real data from the Canadian Government.
    """

    unemployment_csv = csv.reader(open("unemployment_industry.csv"))
    header = unemployment_csv.next()
    data = []
    for row in unemployment_csv:
        data.append(row)

    data = np.array(data)

    for i in range(len(data)):
        rates = [data[i][1], data[i][2], data[i][3], data[i][4], data[i][5], data[i][6]]
        data[i][0] = Rates(unemployment_rates=rates, predicted_rates=predicted_rates(rates),
                           rates_without_COVID=rates_without_COVID(rates))

    return [data[i] for i in range(len(data))]
