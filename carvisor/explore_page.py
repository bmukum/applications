import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

def preprocess_data():
    cleaner = pd.read_csv('vehicles.csv')
    cleaner = cleaner[["price", "year", "manufacturer", "model", "condition", "cylinders", "fuel", "odometer", "drive"]]
    #print(list(cleaner))
    cleaner = cleaner[(cleaner.price < 70000) & (cleaner.price >= 800)]
    cleaner = cleaner[(cleaner.odometer < 130000)]

    #print(cleaner.shape)
    cleaner.loc[cleaner.year >= 2021, 'condition'] = cleaner.loc[cleaner.year >= 2021, 'condition'].fillna('new')
    cleaner.loc[cleaner.year >= 2019, 'condition'] = cleaner.loc[cleaner.year >= 2019, 'condition'].fillna('like new')
    #print(cleaner.condition.value_counts())


    ##odometer reading
    excellent_odo_mean = cleaner[cleaner['condition'] == 'excellent']['odometer'].mean()
    good_odo_mean = cleaner[cleaner['condition'] == 'good']['odometer'].mean()
    like_new_odo_mean = cleaner[cleaner['condition'] == 'like new']['odometer'].mean()
    salvage_odo_mean = cleaner[cleaner['condition'] == 'salvage']['odometer'].mean()
    fair_odo_mean = cleaner[cleaner['condition'] == 'fair']['odometer'].mean()

    cleaner.loc[cleaner['odometer'] <= like_new_odo_mean, 'condition'] = cleaner.loc[cleaner['odometer'] <= like_new_odo_mean, 'condition'].fillna('like new')
    cleaner.loc[cleaner['odometer'] >= fair_odo_mean, 'condition'] = cleaner.loc[cleaner['odometer'] >= fair_odo_mean, 'condition'].fillna('fair')
    cleaner.loc[((cleaner['odometer'] > like_new_odo_mean) &
        (cleaner['odometer'] <= excellent_odo_mean)), 'condition'] = cleaner.loc[((cleaner['odometer'] > like_new_odo_mean) &
        (cleaner['odometer'] <= excellent_odo_mean)), 'condition'].fillna('excellent')

    cleaner.loc[((cleaner['odometer'] > excellent_odo_mean) &
        (cleaner['odometer'] <= good_odo_mean)), 'condition'] = cleaner.loc[((cleaner['odometer'] > excellent_odo_mean) &
        (cleaner['odometer'] <= good_odo_mean)), 'condition'].fillna('good')

    cleaner.loc[((cleaner['odometer'] > good_odo_mean) &
        (cleaner['odometer'] <= fair_odo_mean)), 'condition'] = cleaner.loc[((cleaner['odometer'] > good_odo_mean) &
        (cleaner['odometer'] <= fair_odo_mean)), 'condition'].fillna('salvage')

    cleaner['cylinders'] = cleaner['cylinders'].fillna(method='ffill')
    cleaner['fuel'] = cleaner['fuel'].fillna(method='ffill')
    cleaner['drive'] = cleaner['drive'].fillna(method='ffill')
    cleaner['manufacturer'] = cleaner['manufacturer'].fillna(method='ffill')
    cleaner['year'] = cleaner['year'].fillna(method='ffill')
    cleaner['model'] = cleaner['model'].fillna(method='ffill')
    missing_drive = cleaner['drive'].isna()
    cleaner.loc[missing_drive, 'drive'] = 'fwd'

@st.cache
def load_data():
    df = pd.read_csv("clean_data.csv")
    return df

df = load_data()

def show_explore_page():
    st.title("Visualizing Car Prices")
    
    st.write("""### Visualizations""")
    manufacture_data = df["manufacturer"].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(manufacture_data, labels=manufacture_data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    ax1.axis("equal")

    st.write("""### Distribution of Cars by Manufacturers""")

    st.pyplot(fig1)

    st.write("""### Mean Price of Car by Year""")
    year_data = df.groupby(["year"])["price"].mean().sort_values(ascending=True)
    st.bar_chart(year_data)

    st.write("""### Mean Price of Car Based on Condition""")
    condition_data = df.groupby(["condition"])["price"].mean().sort_values(ascending=True)
    st.line_chart(condition_data)
