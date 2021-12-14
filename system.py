"""CSC110 Fall 2021 Project, System Module

Description
===============================
The system module stores several constants, functions and classes used in our calculations related to the
unemployment rates of the different industries in Canada.

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
from dataclasses import dataclass

# Global variables
# Names of all Canadian industries we'll be tracking
INDUSTRIES = [
    'Accommodation and food services',
    'Information, culture and recreation',
    'Construction',
    'Other services (except public administration)',
    'Transportation and warehousing',
    'Wholesale and retail trade',
    'Manufacturing',
    'Educational services',
    'Professional, scientific and technical services',
    'Health care and social assistance',
    'Finance, insurance, real estate, rental and leasing',
    'Public administration',
    'Forestry, fishing, mining, quarrying, oil and gas',
    'Agriculture'
]

# Classes
@dataclass
class Rates:
    """A bundle of all the unemployment rates to display for a job industry.

    Instance Attributes:
        - unemployment_rates: a list of the unemployment rates for this industry, from 2016 to 2021
        - predicted_rates: a list of the predicted unemployment rates for this industry, from 2022 to 2024
        - rates_without_COVID: a list of the unemployment rates if COVID hadn't happened, from 2020 to 2021

    """
    unemployment_rates: list[float]
    predicted_rates: list[float]
    rates_without_COVID: list[float]


@dataclass
class Industry:
    """A job industry in the Canadian job market.

    Instance Attributes:
        - name: an index that points to a name in the INDUSTRIES list
        - rates: the unemployment rates (and related statistics) for this job industry
        - impact: a score that measures how much this industry was impacted by COVID-19, increasing as impact is larger

    Representation Invariants:
        - 0 <= self.name < len(INDUSTRIES)

    """
    name: int
    rates: Rates
    impact: int


class JobMarket:
    """A class that holds all the data related to unemployment rates and job industries
     in a country's job market.

    Instance Attributes:
        - country_name: the  name of the country whose job market this is
        - rates: the unemployment rates (current and future) for the country
        - industries: a list of all the job industries in this country
        - sorted_by_impact: a list of indexes that point to objects in industries, sorted by the impact COVID-19
        had on them

    Representation Invariants:
        - {index < len(industries) for index in sorted_by_impact}

    """
    country_name: str
    rates: Rates
    industries: list[Industry]
    sorted_by_impact: list[int]
    impact_groups: set[int]

    def __init__(self, name: str, rates: Rates, industries: list[Industry], impact_groups: set[int]) -> None:
        """Initialize a new country's job market/unemployment statistics object
        with the name of the country.
        """
        self.country_name = name

        self.rates = rates
        self.industries = industries
        self.impact_groups = impact_groups
        self.sorted_by_impact = []

    def get_industry(self, name: str) -> Industry:
        """Return the Industry object corresponding to the name passed in.

        Preconditions:
            - name in INDUSTRIES
        """
        index = name_to_int(name)

        for industry in self.industries:
            if index == industry.name:
                return industry

    def get_rates(self, industry_names: list[str]) -> list[list[float]]:
        """Return the unemployment rates (reported and predicted) of the industries selected.

        Preconditions:
            - {name in INDUSTRIES for name in industry_names}
        """
        industries = [self.get_industry(industry) for industry in industry_names]
        list_so_far = []

        for industry in industries:
            list_so_far.append(industry.rates.unemployment_rates + industry.rates.predicted_rates)

        return list_so_far

    def get_rates_wt_covid(self, industry_names: list[str]) -> list[list[float]]:
        """Return the unemployment rates (reported and without COVID-19) of the industries selected.

        Preconditions:
            - {name in INDUSTRIES for name in industry_names}
        """
        industries = [self.get_industry(industry) for industry in industry_names]
        list_so_far = []

        for industry in industries:
            list_so_far.append([industry.rates.unemployment_rates[i] for i in range(0, 4)]
                               + industry.rates.rates_without_COVID)

        return list_so_far

    def rates_in_range(self, industry_names: list[str], years: list[int]) -> list[list[float]]:
        """Return the unemployment rates (reported and predicted) of the industries over the years selected.

        Preconditions:
            - {2016 <= year <= 2024 for year in years}
            - {name in INDUSTRIES for name in industry_names}
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
        """Return the country's (reported and predicted) unemployment rates.
        """
        return self.rates.unemployment_rates + self.rates.predicted_rates

    def get_national_rates_wt_covid(self) -> list[float]:
        """Return the country's (reported and without COVID-19) unemployment rates.
        """
        return [self.rates.unemployment_rates[i] for i in range(0, 4)] + self.rates.rates_without_COVID

    def national_rates_in_range(self, years: list[int]) -> list[float]:
        """Return the unemployment rates (reported and predicted) of the country over the years selected.

        Preconditions:
            - {2016 <= year <= 2024 for year in years}
        """
        rates = [self.rates.unemployment_rates[i] for i in range(0, len(years))]
        if len(years) > len(self.rates.unemployment_rates):
            rates.extend([self.rates.predicted_rates[i] for i in range(0, len(years) -
                                                                       len(self.rates.unemployment_rates))])

        return rates

    def sort_industries_by_impact(self) -> None:
        """Sort the industries by the impact COVID-19 had on them.
        """
        for i in range(0, len(self.industries)):
            max = i
            for j in range(0, len(self.industries)):
                if self.industries[j].impact > self.industries[max].impact\
                        and j not in self.sorted_by_impact:
                    max = j
            self.sorted_by_impact.append(max)

    def group_industries_by_impact(self, group: int) -> list[list[float]]:
        """Return all the industries in a specific impact group. The impact value of an industry
         increases the more COVID-19 had an impact on unemployment rate.
        """
        group_so_far = []
        entered = False

        if self.sorted_by_impact == []:
            self.sort_industries_by_impact()

        for index in self.sorted_by_impact:
            if self.industries[index] == group:
                entered = True
                group_so_far.append(self.industries[index].rates.unemployment_rates +
                                    self.industries[index].rates.predicted_rates)
            elif entered:
                return group_so_far

    def top_urs(self, year: int, amount: int) -> list[list[float]]:
        """"Return # (based on amount sent in) industries with the highest unemployment rates in the year mentioned.

        Preconditions:
            - year in [2016, 2017, 2018, 2019, 2020, 2021]
            - amount < len(self.industries)
        """
        top_ur_so_far = []
        index = year_to_index(year)

        for i in range(0, amount):
            max = i
            for j in range(0, len(self.industries)):
                if self.industries[j].rates.unemployment_rates[index] > \
                        self.industries[i].rates.unemployment_rates[index] and j not in top_ur_so_far:
                    max = j
            top_ur_so_far.append(max)

        return [self.industries[index].rates.unemployment_rates + self.industries[index].rates.predicted_rates
                for index in top_ur_so_far]


# Helper functions
def year_to_index(year: int) -> int:
    """Returns the corresponding list position of a specific year. For example, a list of
     total workers in the Information, culture and recreation industry
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


def int_to_name(index: int) -> str:
    """ Return the name of this industry using the index stored in self.name
    and the list of industry names in INDUSTRIES.

    Preconditions:
        - 0 <= self.name < len(INDUSTRIES)

    >>> int_to_name(1)
    Information, culture and recreation
    """
    return INDUSTRIES[index]


def name_to_int(name: str) -> int:
    """ Return the index of this industry in INDUSTRIES using the name passed in.

    Preconditions:
        - name in INDUSTRIES

    >>> name_to_int('Information, culture and recreation')
    1
    """
    for i in range(0, len(INDUSTRIES)):
        if name == INDUSTRIES[i]:
            return i


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
