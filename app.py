import streamlit as st
import pandas as pd
import os
from datetime import datetime
import csv

# Dictionary for pip values
pip_values = {
    "USD": 0.0001,
    "CHF": 0.00018,
    "CAD": 0.000074,
    "JPY": 0.00014,
    "AUD": 0.000067,
    "GBP": 0.000127,
    # Add other currencies as needed
}

# Function to calculate the size of the lot
def hitung_ukuran_lot(usd, tick, pair):
    # Extract the quote currency from the pair
    quote_currency = pair[-3:]

    # Get the pip value for the quote currency
    pip_value = pip_values.get(quote_currency.upper(), 0.0001)  # Default to 0.0001 if currency not found

    # Calculate the lot size
    if tick == 0:
        return 0.0

    lot_size = (usd / tick) * (pip_value / 0.0001)

    # If the pair is XAUUSD, multiply the lot size by 10
    if pair.lower() == "x":
        lot_size *= 10

    return lot_size

# Function to save to CSV
def simpan_ke_csv(file_path, pair, ukuran_lot):
    tanggal = datetime.now().strftime("%Y-%m-%d")
    new_row = [tanggal, pair, ukuran_lot]

    if not os.path.exists(file_path):
        with open(file_path, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Tanggal", "Pair", "Ukuran Lot (cent USD)"])
            writer.writerow(new_row)
    else:
        with open(file_path, mode='a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(new_row)

# Streamlit app layout
st.title("Forex Lot Size Calculator")
st.markdown("This application calculates the Forex lot size based on the input cent USD and tick values.")

# Form for user input
with st.form("lot_size_form"):
    usd_input = st.number_input("Enter the amount in cent USD:", min_value=0.0, value=40.0, format='%f')  # Set default value to 40
    tick_input = st.number_input("Enter the tick value:", min_value=0.0, format='%f')
    pair_input = st.text_input("Enter the currency pair:")
    submit_button = st.form_submit_button("Calculate Lot Size")

# Processing the form input
if submit_button:
    if tick_input == 0:
        st.error("Tick value cannot be zero.")
    else:
        pair_input_original = pair_input

        ukuran_lot = hitung_ukuran_lot(usd_input, tick_input, pair_input)
        file_path = "riwayatorder.csv"  # Modify this path as needed

        try:
            simpan_ke_csv(file_path, pair_input_original, ukuran_lot)
            st.success(f"Ukuran Lot (cent USD): {ukuran_lot} has been saved to CSV with today's date.")
        except Exception as e:
            st.error(f"An error occurred: {e}")

# Download CSV
if os.path.exists("riwayatorder.csv"):
    with open("riwayatorder.csv", "rb") as file:
        st.download_button(label="Download CSV", data=file, file_name="riwayatorder.csv", mime="text/csv")

# Footer or additional information
st.markdown("---")
st.info("Forex Lot Size Calculator by wildanzake")
