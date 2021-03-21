import pandas as pd
import plotly.graph_objs as go
import requests
from collections import defaultdict


# Use this file to read in your data and prepare the plotly visualizations. The path to the data files are in
# `data/file_name.csv`



top10country = ['us', 'cn', 'jp', 'de', 'gb', 'in', 'fr', 'br', 'it', 'ca','il']

def get_data_from_WB(year_start, year_end, indicator='SP.POP.GROW', country_list = top10country):
    """
    pulls data from world bank to json file
    
    Args:
        year_strat (int): first year for data
        year_end (int): last year for data
        country_list (list of strings): list of countries by 2 char ISO convention
        indicator (str): what value to pull, according to WB encoding
        
    returns:
        r (list): json file
        
    """
    
    date_range = str(year_start) + ":" + str(year_end)
    countries = ""
    for val in country_list:
        countries += ";" + val
    countries = countries[1::]    
    
    url = "http://api.worldbank.org/v2/countries/" + countries + "/indicators/" + indicator

    
    #pull relevant data using API
    payload = {'format': 'json', 'per_page': '500', 'date':date_range} 
    r = requests.get(url, params=payload)

    return r

def json_to_plot(r):
    """
    Accepts json file, returns list ready for plotting
    
    Args:
        r (list): output of get_data_from_WB function
    
    Returns:
        data_dict (list): data for plotting
        country list (list of strings): country name used for plotting

    """
    data_dict = defaultdict(list)
    for entry in r.json()[1]:
        if data_dict[entry['country']['value']]:
            data_dict[entry['country']['value']][0].append(int(entry['date']))
            data_dict[entry['country']['value']][1].append(entry['value'])
        else:
            data_dict[entry['country']['value']] = [[],[]]
            data_dict[entry['country']['value']][0].append(int(entry['date']))
            data_dict[entry['country']['value']][1].append(entry['value'])

        # {'China': [[2015, 2014, 2013],
        # [0.508136747291937, 0.506311591779847, 0.49370963351136]],
        # 'India': [[2015, 2014, 2013],
        # [1.16752707459156, 1.18932821143382, 1.21941894433091]]})

    countries = sorted(list(data_dict.keys()))
    return data_dict, countries
    
def return_figures():
    """Creates four plotly visualizations

    Args:
        None

    Returns:
        list (dict): list containing the four plotly visualizations

    """
    

    
    
    # first chart plots annual population growth in % from 1961 to 2019 in top 10 economies 
    # as a line chart
    
    #pull data from WB using API
    r = get_data_from_WB(1961,2019,'SP.POP.GROW')
    
    data, countries = json_to_plot(r)
    graph_one = []    
    
    for country in countries:
        graph_one.append(
          go.Scatter(
          x = data[country][0],
          y = data[country][1],
          mode = 'lines',
          name = country,
          )
        )

    layout_one = dict(title = 'Annual % population growth',
                xaxis = dict(title = 'Year'),
                yaxis = dict(title = '% Growth'),
                )

# second chart plots access to electricity in 2018 as a bar chart    
    r = get_data_from_WB(2018,2018,'EG.ELC.ACCS.ZS')
    data, countries = json_to_plot(r)
    
    
    
    graph_two = []

    graph_two.append(
      go.Bar(
      x = countries,
      y = [data[country][1][0] for country in countries],
      )
    )

    layout_two = dict(title = 'Access to electricity in 2018 (% of population)',
                xaxis = dict(title = 'Country',),
                yaxis = dict(title = '%'),
                )


# third chart plots inflation, consumer prices (annual %)
    r = get_data_from_WB(1960,2019,'FP.CPI.TOTL.ZG')
    data, countries = json_to_plot(r)

    graph_three = []
    for country in countries:
        graph_three.append(
          go.Scatter(
          x = data[country][0],
          y = data[country][1],
          mode = 'lines',
          name = country,
          )
        )

    layout_three = dict(title = 'Inflation, consumer prices (annual %)',
                xaxis = dict(title = 'Country'),
                yaxis = dict(title = 'Annual %')
                       )
    
# fourth chart shows government expenditure on education, total (% of government expenditure)
    
    r = get_data_from_WB(1981,2018,'se.xpd.totl.gb.zs')
    data, countries = json_to_plot(r)
    
    
    graph_four = []
    for country in countries:
        graph_four.append(
          go.Scatter(
          x = data[country][0],
          y = data[country][1],
          mode = 'markers',
          name = country
          )
        )

    layout_four = dict(title = 'Government expenditure on education,<br>total (% of government expenditure)',
                xaxis = dict(title = 'Country'),
                yaxis = dict(title = '%'),
                )
    
    # append all charts to the figures list
    figures = []
    figures.append(dict(data=graph_one, layout=layout_one))
    figures.append(dict(data=graph_two, layout=layout_two))
    figures.append(dict(data=graph_three, layout=layout_three))
    figures.append(dict(data=graph_four, layout=layout_four))

    return figures