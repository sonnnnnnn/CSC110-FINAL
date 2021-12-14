"""CSC110 Fall 2021 Project, System Module

Description
===============================
The system module stores several constants, functions and classes used in our calculations related to the
unemployment rates of the different industries in Canada.

Short-forms:
ur = unemployment rate
rps = recovery potential score
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

from dataclasses import dataclass

# Global variables
# Names of all Canadian industries we'll be tracking
INDUSTRIES = [
    'Accommodation and food services',
    'Information, culture and recreation',
    'Forestry, fishing, mining, quarrying, oil and gas',
    'Business, building and other support services',
    'Construction',
    'Other services (except public administration)',
    'Transportation and warehousing',
    'Wholesale and retail trade',
    'Manufacturing',
    'Educational services',
    'Agriculture',
    'Professional, scientific and technical services',
    'Health care and social assistance',
    'Finance, insurance, real estate, rental and leasing',
    'Public administration',
    'Utilities'
]

# Our own small set of values related to factors that affect a job industry's success during COVID-19
# The columns in order represent:
# (Work off computer, Communicate with clients,
# Essential
# Front-line
SUCCESS_FACTORS = [
    [(), False, False],
    [(), False, False],
    [(), True, False],
    [(), True, False],
    [(), True, False],
    [(), False, False],
    [(), True, False],
    [(), True, True],
    [(), True, True],
    [(), True, True],
    [(), True, True],
    [(), True, False],
    [(), True, True],
    [(), True, False],
    [(), False, False],
    [(), True, False]
]

# Classes
@dataclass
class Factors:
    """A bundle of possible factors that affect the potential of a job industry
    to be able to work remotely during the pandemic.

    Instance Attributes:
        - physical_proximity: an average based on
        - essential:
        - front_line:
        - overworked_employees: if the industry is both essential and front_line, this value is True
        - ur_trend_before:
        - ur_compared_to_nur:

    Representation Invariants:
        -
    """
    physical_proximity: int
    essential: bool
    front_line: bool
    overworked_employees: bool
    ur_trend_before: int
    ur_compared_to_nur: bool


@dataclass
class Rates:
    """A bundle of all the unemployment rates to display for a job industry.

    Instance Attributes:
        - employment_rates: a list of the unemployment rates for this industry, from 2016 to 2021
        - predicted_rates: a list of the predicted unemployment rates for this industry, from 2022 to 2024
        - rates_without_COVID: a list of the unemployment rates if COVID hadn't happened, from 2020 to 2024

    """
    unemployment_rates: list[float]
    predicted_rates: list[float]
    rates_without_COVID: list[float]


@dataclass
class Industry:
    """A job industry in the Canadian job market.

    Instance Attributes:
        - name: an index that points to a name in the INDUSTRIES list
        - rates: the unemployment rates (current and future) for this job industry
        - factors: the factors that affect this industry's ability to succeed during/after COVID-19
        - impact: a score that measures how much this industry was impacted by COVID-19, on a scale of 1-3 (low to high)
        - potential_remote_work: a score that measures this industry's potential to work remotely
        - recovery_potential: a score that measures how likely this industry is to recover after COVID-19

    Representation Invariants:
        - 0 <= self.name < len(INDUSTRIES)
        - len(employee_numbers) == 6
        - 0 <= potential_remote_work <= 100
        - 0 <= recovery_potential <= 100

    """
    name: int
    rates: Rates
    factors: Factors
    impact: int
    potential_remote_work: int


class JobMarket:
    """A class that holds all the data related to unemployment rates
     in a country's job market.

    Instance Attributes:
        - country_name: the  name of the country whose job market this is
        - rates: the unemployment rates (current and future) for the country
        - industries: a list of all the job industries in this country

    Representation Invariants:
        -

    """
    country_name: str
    rates: Rates
    industries: list[Industry]
    sorted_industries_impact: list[int]
    highest_rwp: list[int]

    def __init__(self, name: str, rates: Rates, industries: list[Industry]) -> None:
        """Initialize a new country's job market/unemployment statistics object
        with the name of the country.
        """
        self.country_name = name

        self.rates = rates
        self.industries = industries
        self.sorted_industries_impact = []
        self.highest_rwp = []

    def get_industry(self, name: str) -> Industry:
        """Return the Industry object corresponding to the name passed in.
        """
        index = name_to_int(name)

        for industry in self.industries:
            if index == industry.name:
                return industry

    def get_rates(self, industry_names: list[str]) -> list[list[float]]:
        """Return the unemployment rates (reported and predicted) of the industries selected.

        """
        industries = [self.get_industry(industry) for industry in industry_names]
        list_so_far = []

        for industry in industries:
            list_so_far.append(industry.rates.unemployment_rates + industry.rates.predicted_rates)

        return list_so_far

    def get_rates_wt_covid(self, industry_names: list[str]) -> list[list[float]]:
        """Return the unemployment rates (reported and natural) of the industries selected.

        """
        industries = [self.get_industry(industry) for industry in industry_names]
        list_so_far = []

        for industry in industries:
            list_so_far.append(industry.rates.unemployment_rates + industry.rates.rates_without_COVID)

        return list_so_far

    def rates_in_range(self, industry_names: list[str], years: list[int]) -> list[list[float]]:
        """Return the unemployment rates (reported and predicted) of the industries over the years selected.

        """
        industries = [self.get_industry(industry) for industry in industry_names]
        list_so_far = []

        for industry in industries:
            temp_list = [industry.rates.unemployment_rates[i] for i in range(0, len(years))]
            if len(years) > len(industry.rates.unemployment_rates):
                temp_list.extend([industry.rates.predicted_rates[i] for i in range(0, len(years) - len(
                    industry.rates.unemployment_rates))])
            list_so_far.append(temp_list)

        return list_so_far

    def get_national_rates(self) -> list[float]:
        """f"""
        return self.rates.unemployment_rates + self.rates.predicted_rates

    def get_national_rates_wt_covid(self) -> list[float]:
        """f BUG HERE"""
        return self.rates.unemployment_rates + self.rates.rates_without_COVID

    def national_rates_in_range(self, years: list[int]) -> list[float]:
        """
        f
        """
        rates = [self.rates.unemployment_rates[i] for i in range(0, len(years))]
        if len(years) > len(self.rates.unemployment_rates):
            rates.extend([self.rates.predicted_rates[i] for i in range(0, len(years) -
                                                                       len(self.rates.unemployment_rates))])

        return rates

    def sort_impacted_industries(self) -> None:
        """s"""
        for i in range(0, len(self.industries)):
            max = i
            for j in range(i, len(self.industries)):
                if self.industries[j].impact > self.industries[max].impact:
                    max = j
            self.sorted_industries_impact.append(max)

    def impacted_industries_group(self, group: int) -> list[list[float]]:
        """Return the top # (based on amount sent in) most impacted (by COVID-19) industries."""
        max = 0
        group_so_far = []
        entered = False

        if self.sorted_industries_impact == []:
            self.sort_impacted_industries()

        for index in self.sorted_industries_impact:
            if self.industries[index] == group:
                entered = True
                group_so_far.append(self.industries[index].rates.unemployment_rates +
                                    self.industries[index].rates.predicted_rates)
            elif entered:
                return group_so_far

    def sort_rwps_score(self) -> None:
        """s"""
        for i in range(0, len(self.industries)):
            max = i
            for j in range(i, len(self.industries)):
                if self.industries[j].potential_remote_work > self.industries[max].potential_remote_work:
                    max = j
            self.highest_rwp.append(max)

    def top_rwps_score(self, amount: int) -> list[Industry]:
        """Return # (based on amount sent in) industries with the highest remote work potential."""
        max = 0

        if self.highest_rwp == []:
            self.sort_rwps_score()

        return [self.industries[self.highest_rwp[i]] for i in range(0, amount)]

    def get_rwps_scores(self, industry_names: list[str]) -> list[int]:
        """d"""
        industries = [self.get_industry(industry) for industry in industry_names]

        return [industry.potential_remote_work for industry in industries]

    def top_ur(self, year: int, amount: int) -> list[list[float]]:
        """"d"""
        top_ur_so_far = []
        index = year_to_index(year)

        for i in range(0, amount):
            max = i
            for j in range(i, len(self.industries)):
                if self.industries[j].rates.unemployment_rates[index] > \
                        self.industries[i].rates.unemployment_rates[index]:
                    max = j
            top_ur_so_far.append(max)

        return [self.industries[index].rates.unemployment_rates + self.industries[index].rates.predicted_rates
                for index in top_ur_so_far]


# Helper functions
def year_to_index(year: int) -> int:
    """Returns the corresponding list position of a specific year. For example, a list of
     total workers in the Forestry, fishing, mining, quarrying, oil and gas industry
     could be [20000, 30000, 43100, 24500, 43000]. The second element corresponds
     to the total number of workers in 2017.

     Preconditions:
     - year in [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

     >>> year_to_index(2017)
     1
    """
    years = [2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024]

    for i in range(0, len(years)):
        if years[i] == year:
            return i


def int_to_name(name: int) -> str:
    """ Return the name of this industry using the index stored in self.name
    and the list of industry names in INDUSTRIES.

    Preconditions:
    - 0 <= self.name < len(INDUSTRIES)

    >>> industry = Industry(2, Rates([], [], []), Factors(0), 0, 0)
    >>> int_to_name(industry.name)
    Forestry, fishing, mining, quarrying, oil and gas
    """
    return INDUSTRIES[name]


def name_to_int(name: str) -> int:
    """ Return the index of this industry in INDUSTRIES using the name passed in.

        Preconditions:
        - name in INDUSTRIES

        >>> industry = Industry(2, Rates([], [], []), Factors(0), 0, 0)
        >>> name_to_int('Forestry, fishing, mining, quarrying, oil and gas')
        2
        """

    for i in range(0, len(INDUSTRIES)):
        if name == INDUSTRIES[i]:
            return i
