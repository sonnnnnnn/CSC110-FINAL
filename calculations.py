"""CSC110 Fall 2021 Project, Calculations

Description
===============================
The calculations file reads and transforms data from the dataset, forming a complete list of Industry objects.
It computes all the rates seen in the Industry dataclass.

Short-forms:
ur = unemployment rate
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

# Unmployment rate calculations
def average_unemployment_rate(rates: list[float]) -> float:
    """ Return the average unemployment rate based on a list of rates.

    >>> average_unemployment_rate([6.2, 2.3, 7.7, 3.8])
    5.0
    """
    return sum(rates) / len(rates)


def rates_without_COVID(rates: list[float]) -> list[float]:
    """ Return the predicted unemployment rate in 2020 and 2021 based on unemployment rate before COVID-19
    using arithmetic mean method.
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
def calculate_ci(rates: list[float]) -> int:
    """ Calculate the impact of COVID-19 on a job industry. Impact values increase as impact does.

    Preconditions:
        - len(rates) == 6

    >>> calculate_ci([5.4, 4.9, 5.1, 4.6, 8, 5.6])
    2
    """
    avg_ur_before = (rates[0] + rates[1] + rates[2] + rates[3]) / 4
    avg_ur_after = (rates[4] + rates[5]) / 2
    ur_difference = abs(avg_ur_after - avg_ur_before)

    impact = 1
    difference = 1

    while ur_difference > difference:
        impact = impact + 1
        difference = difference + 1.5

    return impact


# Reading from datasets
def read_data() -> JobMarket:
    """Read the data in both of our data sets and store in a JobMarket object.
    """
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


def read_industry_data() -> list[system.Industry]:
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
        data[i][0] = system.Rates(unemployment_rates=rates, predicted_rates=predicted_rates(rates),
                           rates_without_COVID=rates_without_COVID(rates))

    return [data[i] for i in range(len(data))]


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    python_ta.check_all(config={
        'extra-imports': ['python_ta.contracts', 'dataclasses'],
        'max-line-length': 100,
        'disable': ['R1705', 'C0200'],
    })
