"""

Name: Daniel Kotey
CS230: Section 1
Data: Used cars for sale on Craigslist
URL:

Description:

This program is an application that helps users who are looking for Used Cars on craigslist find
a potential car that fits for them. it also shows the top 5 brands from the total listings in a bar chart. Users
can also compare the total cars in the listings by brand in a bar chart.

"""

import pandas as pd
import matplotlib.pyplot as plt
import streamlit as st
import pydeck as pdk
import time


def read_data(filename):
    df = pd.read_csv(filename).dropna()
    lst = []
    column = ["url", "region", "region_url", "price", "year", "manufacturer", "model", "condition", "cylinders", "fuel",
              "odometer", "title_status", "transmission", "VIN", "drive", "size", "type", "paint_color", "image_url",
              "state", "lat", "long", "posting_date"]

    for index, row in df.iterrows():
        sub = []
        for col in column:
            index_no = df.columns.get_loc(col)
            sub.append(row[index_no])
        lst.append(sub)

    return lst


def make_list(data):
    makes = []

    for i in range(len(data)):
        if data[i][5] not in makes:
            makes.append((data[i][5]))
    return makes


def popular_brands(data, makes):
    counts = {}

    for make in makes:
        freq = 0
        for i in range(len(data)):
            if data[i][5] == make:
                freq += 1
            counts[make] = freq

    return counts


def bar_chart_1():
    # Make a chart to see how the top 5 brands
    df = pd.read_csv('cl_used_cars_7000_sample.csv')
    data = df.groupby(['manufacturer']).size().sort_values(ascending=False).head(5)
    x = data.index.tolist()
    y = data.values.tolist()
    plt.bar(x, y, color='maroon')
    plt.xlabel('Car Brands')
    plt.ylabel('Number of Listings')
    plt.title('Top 5 Brands by Listings')
    st.write(f"{x[0]} has the most listings at {y[0]} listings. Maybe start your research with {x[0]}?")
    return plt


def bar_chart(counts):
    x = counts.keys()
    y = counts.values()

    plt.bar(x, y)
    plt.xticks(rotation=45)
    plt.xlabel('Car Brands')
    plt.ylabel('Frequencies of Listings')
    title = 'Listing in'
    for key in counts.keys():
        title += ' ' + key
    plt.title(title)

    return plt


def display(data, makes):
    # Display map based on latitude and longitude
    loc = []
    for i in range(len(data)):
        if data[i][5] in makes:
            loc.append([data[i][5], data[i][20], data[i][21]])

    nap_df = pd.DataFrame(loc, columns=['Listing', 'lat', 'lon'])
    view_state = pdk.ViewState(latitude=nap_df['lat'].mean(), longitude=nap_df['lon'].mean(), zoon=10, pitch=0)
    layer = pdk.Layer('ScatterplotLayer', data=nap_df, get_position='[lon, lat]', get_radius=50, get_color=[0, 255, 255]
                      , pickable=True)
    tool_tip = {'html': 'Listing:<br/>{Listing}', 'style': {'backgroundColor': 'steelblue', 'color': 'white'}}
    maps = pdk.Deck(map_style='mapbox://styles/mapbox/light-v9', initial_view_state=view_state, layers=[layer],
                    tooltip=tool_tip)

    st.pydeck_chart(maps)


def dataset(data):
    # Displays a Dataframe that is filtered based on user input in Sidebar
    st.write('Used Car Finder results: ')
    with st.sidebar.expander('Expand for Filters'):
        car_make = st.selectbox('Select Car Make', data['manufacturer'].unique())
        data = data[data['manufacturer'] == car_make]
        car_model = st.selectbox('Select Car Model', data['model'].unique())
        data = data[data['model'] == car_model]
        car_price = st.slider('Set the minimum price', 0, max(data['price']))
        data = data[data['price'] >= car_price]
        car_condition = st.selectbox('Select Vehicle Condition', data['condition'].unique())
        data = data[data['condition'] == car_condition]
        car_fuel = st.selectbox('Select Vehicle Fuel Type', data['fuel'].unique())
        data = data[data['fuel'] == car_fuel]
        car_transmission = st.selectbox('Select Transmission type', data['transmission'].unique())
        data = data[data['transmission'] == car_transmission]
        car_drive = st.selectbox('Select Vehicle Drivetrain', data['drive'].unique())
        data = data[data['drive'] == car_drive]
        car_type = st.selectbox('Select Vehicle Type', data['type'].unique())
        data = data[data['type'] == car_type]
        car_color = st.selectbox('Select Exterior Color', data['paint_color'].unique())
        data = data[data['paint_color'] == car_color]
    st.write(data)


def main():
    data = read_data('cl_used_cars_7000_sample.csv')
    ata = pd.read_csv('cl_used_cars_7000_sample.csv')
    # Progress Bar courtesy of https://upslearn.github.io/Books/concepts.html
    my_bar = st.progress(0)

    for percent_complete in range(100):
        time.sleep(0.1)
        my_bar.progress(percent_complete + 1)

    with st.spinner('Wait for it...'):
        time.sleep(5)
    st.write('Done!')
    # Title and Message
    st.title('Used Cars from Craigslist')
    st.write('Welcome to my hopefully helpful app!')
    # Sidebar Widgets and Code
    st.sidebar.title('Compare Listings by Brand')
    makes = st.sidebar.multiselect('Select Car Makes', make_list(data))
    st.sidebar.title('Top 5 Car Brands')
    brands = st.sidebar.button('Click Here for Top 5')
    # Columns
    col1, col2 = st.columns(2)
    with col2:
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.markdown('')
        st.image('Craigslist-Emblem.png', use_column_width=True)
    with col1:
        if brands:
            st.pyplot(bar_chart_1())
        st.sidebar.title("Used Car Finder")

    dataset(ata)

    if len(makes) > 0:
        st.write('Map of Listing')
        display(data, makes)
        st.write('\nPopular Brands based on frequency of make listings')
        st.pyplot(bar_chart(popular_brands(data, makes)))


main()
