import streamlit as st
import pickle
import numpy as np
import csv
import seaborn as sns
import matplotlib.pyplot as plt
from matplotlib import style
from scipy import stats
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.linear_model import LinearRegression
from sklearn import metrics

#pip install -U scikit-learn scipy matplotlib

def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]
le_manufacturer = data["le_manufacturer"]
le_model = data["le_model"]
le_condition = data["le_condition"]
le_cylinders = data["le_cylinders"]
le_fuel = data["le_fuel"]
le_drive = data["le_drive"]


def show_predict_page():
    st.title("WGU Capstone Project: Car Price Prediction")
    st.write("""### Please provide some information to predict the price""")

    years = (
        1900,
        1901,
        1910,
        1915,
        1916,
        1918,
        1920,
        1921,
        1922,
        1923,
        1924,
        1925,
        1926,
        1927,
        1928,
        1929,
        1930,
        1931,
        1932,
        1933,
        1934,
        1935,
        1936,
        1937,
        1938,
        1939,
        1940,
        1941,
        1942,
        1943,
        1944,
        1945,
        1946,
        1947,
        1948,
        1949,
        1950,
        1951,
        1952,
        1953,
        1954,
        1955,
        1956,
        1957,
        1958,
        1959,
        1960,
        1961,
        1962,
        1963,
        1964,
        1965,
        1966,
        1967,
        1968,
        1969,
        1970,
        1971,
        1972,
        1973,
        1974,
        1975,
        1976,
        1977,
        1978,
        1979,
        1980,
        1981,
        1982,
        1983,
        1984,
        1985,
        1986,
        1987,
        1988,
        1989,
        1990,
        1991,
        1992,
        1993,
        1994,
        1995,
        1996,
        1997,
        1998,
        1999,
        2000,
        2001,
        2002,
        2003,
        2004,
        2005,
        2006,
        2007,
        2008,
        2009,
        2010,
        2011,
        2012,
        2013,
        2014,
        2015,
        2016,
        2017,
        2018,
        2019,
        2020,
        2021,
        2022,
    )

    manufacturers = (
        'gmc',
        'chevrolet', 
        'toyota' ,
        'ford' ,
        'jeep', 
        'nissan',
        'ram', 
        'mazda',
        'cadillac', 
        'honda', 
        'dodge' ,
        'lexus' ,
        'jaguar', 
        'buick', 
        'volvo', 
        'audi',
        'infiniti', 
        'lincoln' ,
        'alfa-romeo',
        'subaru' ,
        'acura' ,
        'hyundai', 
        'chrysler', 
        'mercedes-benz', 
        'bmw' ,
        'mitsubishi', 
        'porsche' ,
        'kia' ,
        'volkswagen', 
        'mini',
        'pontiac' ,
        'fiat' ,
        'rover' ,
        'tesla' ,
        'mercury', 
        'saturn', 
        'harley-davidson',
        'datsun', 
        'aston-martin', 
        'land rover', 
        'morgan', 
        'ferrari',
    )

    models = (
        'pickup',
        'truck',
        'other',
        'coupe',
        'SUV',
        'hatchback',
        'mini-van',
        'sedan',
        'convertible',
        'wagon',
        'van',
        'bus',
        'offroad',
    )

    conditions = (
        'good',
        'excellent',
        'fair',
        'like new',
        'new',
        'salvage',
    )

    cylinders = (
        '12 cylinders',
        '10 cylinders',
        '8 cylinders',
        '6 cylinders',
        '5 cylinders',
        '4 cylinders',
        '3 cylinders',
        'other',
    )

    fuel_type = (
        'gas',
        'diesel',
        'other',
        'hybrid',
        'electric',
    )

    drives = (
        'rwd',
        '4wd',
        'fwd',
    )
   
    year = st.selectbox("Year", years)
    manufacturer = st.selectbox("Manufacturer", manufacturers)
    model = st.selectbox("Model", models)
    condition = st.selectbox("Condition", conditions)
    cylinder = st.selectbox("Cylinder", cylinders)
    fuel = st.selectbox("Fuel Type", fuel_type)
    drive = st.selectbox("Drive", drives)
    odometer = st.slider("Car Mileage", 0, 300000, 3)

    ok = st.button("Get Price Prediction")
    if ok:
        X = np.array([[year, manufacturer, model, condition , cylinder, fuel, odometer,  drive]])
        X[:, 1] = le_manufacturer.transform(X[:, 1])
        X[:, 2] = le_model.transform(X[:, 2])
        X[:, 3] = le_condition.transform(X[:, 3])
        X[:, 4] = le_cylinders.transform(X[:, 4])
        X[:, 5] = le_fuel.transform(X[:, 5])
        X[:, 7] = le_drive.transform(X[:, 7])
        X = X.astype(float)

        price = abs(regressor.predict(X))
        st.subheader(f"The predicted price for that car is ${price[0]:.2f}")