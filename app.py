import streamlit as st
import pandas as pd
from scraper import WebScraper
import io

# Page configuration
st.set_page_config(
    page_title="Professional Web Scraper",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling (Minimalistic & Professional)
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        background-color: #4a90e2;
        color: white;
        border-radius: 5px;
        border: none;
        padding: 10px 24px;
        transition: all 0.3s;
    }
    .stButton>button:hover {
        background-color: #357abd;
        border: none;
    }
    .css-1d391kg {
        background-color: #ffffff;
    }
    h1 {
        color: #2c3e50;
        font-weight: 700;
    }
    .stAlert {
        border-radius: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("Advanced Web Scraper")
    st.markdown("---")

    # Sidebar for configuration
    with st.sidebar:
        st.header("Settings")
        url = st.text_input("Enter Website URL", placeholder="https://example.com")
        
        st.subheader("Extraction Mode")
        mode = st.radio("Choose Mode", ["Common Elements", "Custom CSS Selector"])
        
        if mode == "Custom CSS Selector":
            selector = st.text_input("CSS Selector", placeholder="h1.title or .price")
            attribute = st.text_input("Attribute (optional)", placeholder="e.g., href, src")
        
        st.markdown("---")
        st.info("This tool extracts structured data from any website using BeautifulSoup.")

    if not url:
        st.warning("Please enter a URL in the sidebar to begin.")
        return

    # Scraper instance
    scraper = WebScraper(url)
    
    if st.sidebar.button("Fetch & Scrape"):
        with st.spinner("Fetching content..."):
            if scraper.fetch_content():
                st.success(f"Successfully connected to {url}")
                
                extracted_data = {}
                
                if mode == "Common Elements":
                    extracted_data = scraper.get_common_data()
                else:
                    if selector:
                        data = scraper.extract_data(selector, attribute if attribute else None)
                        extracted_data = {f"Custom ({selector})": data}
                    else:
                        st.error("Please provide a CSS selector.")
                
                if extracted_data:
                    df = scraper.to_dataframe(extracted_data)
                    
                    # Display Results
                    st.subheader("Extracted Data Preview")
                    st.dataframe(df, use_container_width=True)
                    
                    # Standout Feature: Basic Stats
                    st.subheader("Quick Insights")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Rows", len(df))
                    with col2:
                        st.metric("Columns Found", len(df.columns))
                    with col3:
                        non_null = df.count().sum()
                        st.metric("Total Data Points", non_null)

                    # Export Options
                    st.subheader("Download Data")
                    export_col1, export_col2 = st.columns(2)
                    
                    # CSV Export
                    csv = df.to_csv(index=False).encode('utf-8')
                    export_col1.download_button(
                        label="Download as CSV",
                        data=csv,
                        file_name="scraped_data.csv",
                        mime="text/csv",
                    )
                    
                    # JSON Export
                    json_str = df.to_json(orient="records")
                    export_col2.download_button(
                        label="Download as JSON",
                        data=json_str,
                        file_name="scraped_data.json",
                        mime="application/json",
                    )
                    
                    # Standout Feature: Visual Preview of first few items
                    if "Titles" in df.columns:
                        st.markdown("### Sample Titles")
                        for title in df["Titles"].dropna()[:5]:
                            st.write(f"- {title}")

            else:
                st.error("Failed to fetch the website. Please check the URL or try another site.")

if __name__ == "__main__":
    main()
