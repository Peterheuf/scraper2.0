import streamlit as st
import requests
from bs4 import BeautifulSoup
import pandas as pd

# Functie om data te scrapen
def scrape_website(url, elements):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Dictionary om de data op te slaan
    data = {element: [] for element in elements}
    
    for element in elements:
        for item in soup.select(element):
            data[element].append(item.text.strip())

    return pd.DataFrame(data)

# Streamlit-app interface
st.title("Visuele Webscraper App")

# URL invoeren
url = st.text_input("Voer de URL in van de website die je wilt scrapen")

# Elementen kiezen
elements = st.text_area("Voer de CSS-selectoren in voor de elementen die je wilt scrapen, gescheiden door een komma", ".product-name, .product-price")

# Data scrapen en weergeven
if st.button("Scrapen"):
    if url and elements:
        elements_list = [selector.strip() for selector in elements.split(',')]
        df = scrape_website(url, elements_list)
        st.write("Gescraapte Data:")
        st.dataframe(df)
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name='gescrapte_data.csv',
            mime='text/csv',
        )
    else:
        st.error("Voer een URL in en kies ten minste één element.")
