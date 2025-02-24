import streamlit as st
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin

st.title("Web Scraper for Extracting Components")

url = st.text_input("Enter Website URL:", "")

if st.button("Scrape"):
    if url:
        try:
            response = requests.get(url, headers={'User-Agent': 'Mozilla/5.0'})
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, "html.parser")

                headings = [h.get_text(strip=True) for h in soup.find_all(["h1", "h2", "h3"])]
                paragraphs = [p.get_text(strip=True) for p in soup.find_all("p")]
                links = [urljoin(url, a["href"]) for a in soup.find_all("a", href=True)]
                images = [urljoin(url, img["src"]) for img in soup.find_all("img", src=True)]

               
                st.subheader("Headings")
                for h in headings:
                    st.write(f"- {h}")

                st.subheader("Paragraphs")
                for p in paragraphs[:5]:  
                    st.write(f"- {p}")

                st.subheader("Links")
                for link in links[:5]: 
                    st.write(f"- [{link}]({link})")

                st.subheader("Images")
                for img in images[:5]: 
                    st.image(img, caption=img, use_column_width=True)

            else:
                st.error(f"Error: Unable to fetch the page (Status Code: {response.status_code})")

        except requests.exceptions.RequestException as e:
            st.error(f"Request failed: {e}")
    else:
        st.warning("Please enter a valid URL.")
