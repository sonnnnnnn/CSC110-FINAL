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

import calculations
from system import JobMarket
from system import INDUSTRIES
import pandas as pd
import plotly.express as pe
import plotly


def get_plot_unemployment(data: JobMarket, labels: list, name: str) -> None:
    """ Plots a line graph and Bar Chart showing  the data given. Graph should be outputted in browser
        User is able to toggle between a line graph and a bar chart.
         """
    data1 = INDUSTRIES
    data2 = data.rates_in_range(INDUSTRIES, [2016, 2017, 2018, 2019, 2021])
    dataframe = pd.DataFrame(data1)
    dataframe = dataframe.assign(rate=data2)
    plot = pe.line(dataframe, x=labels[0], y=labels[1], title=name, markers=True)
    # updates the layout of the graph to include  menu to toggle between graphs
    plot.update_layout(updatemenus=[dict(buttons=list([dict(args=["type", "bar"], label="Bar Chart", method="restyle"),
                                                       dict(args=["type", "line"], label="Line Graph",
                                                            method="restyle")]), direction="right", ), ])
    # outputs the plot
    plot.show()


def get_plot_comparison(data: JobMarket) -> None:
    """Plots a comparison graph showing the current unemployment rates and the unemployment rates without COVID-19 .
     Graph should be outputted in browser"

     Comparison graph shows both a line graph and a bar chart. trace0 is the current unemployment rates while Trace1
     are the unemployment rates without COVID-19"
    """
    graph = plotly.graph_objects.Figure()
    # adds the line graph
    graph.add_trace(plotly.graph_objects.Scatter(x=INDUSTRIES, y=data.rates_in_range(INDUSTRIES,
                                                                                     [2016, 2017, 2018, 2019, 2021]), name="COVID-19"))
    # adds bar chart
    graph.add_trace(plotly.graph_objects.Bar(x=data.industries, y=data.get_rates_wt_covid(INDUSTRIES),
                                             name="Without COVID-19"))

    # outputs graph
    graph.show()


def get_plot_prediction(data: JobMarket) -> None:
    """Plots a  graph showing the predicted unemployment for each industry .
         Graph should be outputted in browser"
        """
    data1 = INDUSTRIES
    data2 = data.get_rates(INDUSTRIES)
    dataframe = pd.DataFrame(data1)
    dataframe = dataframe.assign(rate=data2)
    plot = pe.line(dataframe, x=0, y="rate", title="Predicted Unemployment 2022 -2024", markers=True)
    # outputs the plot
    plot.show()


if __name__ == '__main__':
    job_market = calculations.read_data()

