import pandas as pd
import plotly.express as px
import matplotlib.pyplot as plt
import geopandas as gpd

filename = "C:/Users/User/Desktop/datasets/covid_19_clean_complete.csv"
df = pd.read_csv(filename, parse_dates=True)

df['Province/State'] = df['Province/State'].fillna('-')
# print(df.isn().sum())
# print(df.head(2))

# Confirmed Cases ( Top 25 Country )
world_confirmed_cases = df.groupby('Country/Region')['Confirmed'].sum().reset_index()
world_confirmed_cases = world_confirmed_cases.sort_values('Confirmed', ascending=False)[:25]
# print(world_confirmed_cases)

confirmed_figure = px.bar(world_confirmed_cases, x='Confirmed', y='Country/Region',
                          title='Confirmed Cases In The World', text='Confirmed', height=750, orientation='h',
                          color='Country/Region')
# confirmed_figure.show()


# Deaths in WorldWide ( Top 25 Country )

world_deaths = df.groupby('Country/Region')['Deaths'].sum().reset_index()
world_deaths = world_deaths.sort_values('Deaths', ascending=False)[:25]
# print(world_deaths)

deaths_figure = px.scatter(world_deaths, x='Deaths', y='Country/Region', title='Deaths In The World',
                           text='Deaths', height=750, orientation='h', color='Country/Region')
# deaths_figure.show()


# Active Cases WorldWide ( Top 25 Country )

active_cases_world = df.groupby('Country/Region')['Active'].sum().reset_index()
active_cases_world = active_cases_world.sort_values('Active', ascending=False)[:25]
# print(active_cases_world)

active_cases_figure = px.area(active_cases_world, x='Active', y='Country/Region', title='Active Cases WorldWide',
                              text='Active', height=750, color='Country/Region', orientation='h')
# active_cases_figure.show()


# Grouped Confirmed Cases and Deaths
deaths_confirmed_group = df.groupby('Country/Region')['Confirmed', 'Deaths'].sum().reset_index()
deaths_confirmed_group = deaths_confirmed_group.sort_values('Deaths', ascending=False)[:25]
# print(deaths_confirmed_group)

plt.figure(figsize=(30, 10))
plt.bar(deaths_confirmed_group['Country/Region'], deaths_confirmed_group['Confirmed'], label='Confirmed')
plt.bar(deaths_confirmed_group['Country/Region'], deaths_confirmed_group['Deaths'], label='Deaths',
        bottom=deaths_confirmed_group['Confirmed'])
plt.xticks(rotation=100)
plt.legend()
# plt.show()


# GPD Data
geo_data = gpd.GeoDataFrame(df, geometry=gpd.points_from_xy(df.Long, df.Lat))
# print(geo_data)

world_filename = gpd.datasets.get_path('naturalearth_lowres')
world_map = gpd.read_file(world_filename)
# print(world_map.head(5))
world_map.plot()
# plt.show()

format_info = df.groupby(['Date', 'Country/Region'])['Confirmed', 'Deaths'].max()
format_info = format_info.reset_index()

format_info['Date'] = pd.to_datetime(format_info['Date'])
format_info['Date'] = format_info['Date'].dt.strftime('%m/%d/%Y')
format_info['size'] = format_info['Confirmed'].pow(0.3)
# print(format_info)


# Covid19 Confirmed Cases in Between Time
world_figure_confirmed = px.scatter_geo(format_info, locations='Country/Region', locationmode='country names',
                                        color='Confirmed', size='size', hover_name='Country/Region',
                                        projection='natural earth', animation_frame='Date', range_color=[0, 1000],
                                        title='Covid19 Confirmed Cases in Between Time',
                                        color_continuous_scale='portland')
# world_figure_confirmed.show()


# Covid19 Deaths Cases in Between Time
world_figure_deaths = px.scatter_geo(format_info, locations='Country/Region', locationmode='country names',
                                     color='Deaths', size='size', hover_name='Country/Region',
                                     projection='natural earth', animation_frame='Date', range_color=[0, 1000],
                                     title='Covid19 Deaths Cases in Between Time',
                                     color_continuous_scale='portland')
# world_figure_deaths.show()

# Covid 19 increase Cases-Deaths-Recovered
inc_by_time = pd.read_csv("C:/Users/User/Desktop/datasets/day_wise.csv")
inc_by_time = inc_by_time.set_index("Date")
# print(inc_by_time)

plt.figure(figsize=(20, 10))
plt.plot(inc_by_time.Confirmed, label="World Confirmed Cases")
plt.plot(inc_by_time.Recovered, label="World Recovered Cases")
plt.plot(inc_by_time.Deaths, label="World Death Cases")

plt.xticks(['2020-01-22', '2020-02-22', '2020-03-22', '2020-04-22', '2020-05-22', '2020-06-22', '2020-07-27'], size=20)
plt.yticks([i for i in range(0, 10000000, 1000000)], size=20)
plt.ylabel("Total Number of Cases", size=20)
plt.title("Covid19 Confirmed, Recovered, Death Cases From 2020-01-22 To 2020-07-27")
# plt.show()
