"""CSC110 Fall 2021 Project,  Main Module Description
===============================
This  module stores several functions that Output Graphs based on calculations performed in the additional modules.
Copyright and Usage Information
===============================
This file is provided solely for the use of TAs
marking CSC110 projects at the University of Toronto St. George campus. All forms of
distribution of this code, whether as given or with any changes, are
expressly prohibited. For more information on copyright for CSC110 materials,
please consult us at our email addresses.
This file is Copyright (c) 2021 Juhwan Son, Defne Altiok, Aliyah James, and Rohma Daud.
"""

import pandas as pd
import plotly
import plotly.express as pe
import calculations as calc
from system import JobMarket
from system import int_to_name


def read_data() -> JobMarket:
    """Read the data in both of our data sets and store in a JobMarket object.
    """
    country_data = calc.read_national_data()
    data = calc.read_industry_data('data/unemployment_industry.csv')
    industries = calc.save_industry_data(data)
    return JobMarket('Canada', country_data, industries[0], industries[1])


def run_graphs(data: JobMarket) -> None:
    """Runs all graphs below"""
    get_plot_unemployment(data)
    get_plot_comparison(data)
    get_plot_impact(data)
    get_plot_prediction_all(data)
    get_plot_comparison_2020(data)


def get_plot_unemployment(data: JobMarket) -> None:
    """ Plots a line graph and Bar Chart showing  the data given. Graph should be outputted in browser
        User is able to toggle between a line graph and a bar chart.
         """

    data1 = [2016, 2017, 2018, 2019, 2020, 2021]
    data2 = data.rates.unemployment_rates
    dataframe = pd.DataFrame(data1)
    dataframe = dataframe.assign(rate=data2)
    plot = pe.line(dataframe, x=0, y="rate", title='Graph Showing Yearly Unemployment Rates (2016 - 2021)',
                   markers=True)
    # updates the layout of the graph to include  menu to toggle between graphs
    plot.update_layout(updatemenus=[dict(buttons=list([dict(args=["type", "bar"], label="Bar Chart", method="restyle"),
                                                       dict(args=["type", "line"], label="Line Graph",
                                                            method="restyle")]), direction="right", ), ])
    # outputs the plot
    plot.show()


def get_plot_comparison(data: JobMarket) -> None:
    """Plots a comparison graph showing the 2020 and 2021 unemployment rates without COVID-19 .
     Graph should be outputted in browser"

     Comparison graph shows both a line graph and a bar chart. trace0 is the current unemployment rates while Trace1
     are the unemployment rates without COVID-19"
    """
    graph = plotly.graph_objects.Figure()
    # adds the line graph
    industries = data.industries
    data1 = [int_to_name(industries[x].name) for x in range(len(industries))]
    # Extract predicted unemployment rates without Covid-19
    y_data = [industries[x].rates.rates_without_COVID[0] for x in range(len(industries))]
    graph.add_trace(plotly.graph_objects.Scatter(x=data1, y=y_data, name="Without Covid-19, 2020"))
    # adds bar chart
    y_data1 = [industries[x].rates.rates_without_COVID[1] for x in range(len(industries))]
    graph.add_trace(plotly.graph_objects.Bar(x=data1, y=y_data1,
                                             name="Without COVID-19,2021"))

    # outputs graph
    graph.show()


def get_plot_impact(data: JobMarket) -> None:
    """Plots a  graph showing the predicted unemployment for each industry in 2022 .
         Graph should be outputted in browser"
        """
    industries = data.industries
    data1 = [int_to_name(industries[x].name) for x in range(len(industries))]
    data2 = [industries[x].impact for x in range(len(industries))]

    dataframe = pd.DataFrame(data1)
    dataframe = dataframe.assign(rate=data2)
    plot = pe.bar(dataframe, x=0, y="rate", title="Impact of COVID-19 Per Industry")
    # outputs the plot
    plot.show()


def get_plot_prediction_all(data: JobMarket) -> None:
    """ Plots a line graph and Bar Chart showing  the data given. Graph should be outputted in browser
        User is able to toggle between a line graph and a bar chart.
         """

    industries = data.industries
    data1 = [int_to_name(industries[x].name) for x in range(len(industries))]
    data2 = [industries[x].rates.predicted_rates[0] for x in range(len(industries))]
    data3 = [industries[x].rates.predicted_rates[1] for x in range(len(industries))]
    data4 = [industries[x].rates.predicted_rates[2] for x in range(len(industries))]
    dataframe = pd.DataFrame(data1)
    dataframe = dataframe.assign(rate_2022=data2)
    dataframe = dataframe.assign(rate_2023=data3)
    dataframe = dataframe.assign(rate_2024=data4)
    plot = pe.bar(dataframe, x=0, y=['rate_2022', 'rate_2023', 'rate_2024'],
                  title="Predicted Unemployment Rates 2022 - 2024")
    plot.update_layout(barmode='group')
    # updates the layout of the graph to include  menu to toggle between graphs
    plot.update_layout(updatemenus=[dict(buttons=list([dict(args=["type", "bar"], label="Bar Chart", method="restyle"),
                                                       dict(args=["type", "line"], label="Line Graph",
                                                            method="restyle")]), direction="right", ), ])
    # outputs the plot
    plot.show()


def get_plot_comparison_2020(data: JobMarket) -> None:
    """Plots a comparison graph showing the 2020  national unemployment rate and the rates per sector .
     Graph should be outputted in browser"

     Comparison graph shows both a line graph and a bar chart. trace0 is the current unemployment rates while Trace1
     are the unemployment rates without COVID-19"
    """
    graph = plotly.graph_objects.Figure()
    # adds the line graph
    industries = data.industries
    data1 = [int_to_name(industries[x].name) for x in range(len(industries))]
    data2 = data.rates_in_range(data1, [2020])
    y_data = [row[4] for row in data2]
    x_data = [data.rates.unemployment_rates[4]] * len(industries)
    graph.add_trace(plotly.graph_objects.Line(x=data1, y=x_data, name="National Unemployment Rate 2020"))
    # adds bar chart

    graph.add_trace(plotly.graph_objects.Bar(x=data1, y=y_data,
                                             name="Sector Unemployment Rate 2020"))

    # outputs graph
    graph.show()


if __name__ == '__main__':
    import doctest

    doctest.testmod()

    import python_ta
    import python_ta.contracts

    python_ta.contracts.DEBUG_CONTRACTS = False
    python_ta.contracts.check_all_contracts()

    python_ta.check_all(config={
        'max-line-length': 100,
        'disable': ['R1705', 'C0200'],
    })
