import streamlit as st
import pandas as pd
from scraper import WebScraper
import io

# Page configuration
st.set_page_config(
    page_title="InsightScraper Pro",
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
        margin-bottom: 0px;
    }
    .stAlert {
        border-radius: 10px;
    }
    /* Footer Style */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #0e1117;
        color: #fafafa;
        text-align: center;
        padding: 12px 10px;
        font-size: 14px;
        border-top: 1px solid #262730;
        z-index: 1000;
    }
    .footer a {
        color: #4a90e2;
        text-decoration: none;
        margin: 0 12px;
        font-weight: 600;
    }
    .footer a:hover {
        text-decoration: underline;
    }
    </style>
    """, unsafe_allow_html=True)

def main():
    st.title("InsightScraper Pro")
    st.caption("Precision Data Extraction Tool")
    st.markdown("---")

    # Sidebar for configuration
    with st.sidebar:
        st.header("Settings")
        url = st.text_input("Enter Website URL", placeholder="https://example.com")
        
        st.subheader("Extraction Mode")
        mode = st.radio("Choose Mode", ["Common Elements", "Custom CSS Selector"])
        
        if mode == "Custom CSS Selector":
            st.info("Tip: Enter multiple selectors separated by commas for multiple columns (e.g., h3 a, .price_color)")
            selector = st.text_input("CSS Selector(s)", placeholder="e.g., h3 a, .price_color")
            attribute = st.text_input("Attribute (optional)", placeholder="e.g., href, src")
        
        st.markdown("---")
        st.info("This tool extracts structured data from any website using BeautifulSoup.")

    if not url:
        st.warning("Please enter a URL in the sidebar to begin.")
        return

    # Scraper instance
    scraper = WebScraper(url)
    
    if st.sidebar.button("Fetch & Scrape"):
        with st.spinner("Analyzing site architecture..."):
            if scraper.fetch_content():
                st.success(f"Successfully connected to {url}")
                
                # Standout Feature: Metadata Extraction
                metadata = scraper.get_metadata()
                with st.expander("Site Insights (Metadata)", expanded=False):
                    col_m1, col_m2, col_m3 = st.columns(3)
                    col_m1.markdown(f"**Title:**\n{metadata.get('Page Title')}")
                    col_m2.markdown(f"**Description:**\n{metadata.get('Description')}")
                    col_m3.markdown(f"**Keywords:**\n{metadata.get('Keywords')}")

                extracted_data = {}
                
                if mode == "Common Elements":
                    extracted_data = scraper.get_common_data()
                else:
                    if selector:
                        # Split by comma for multi-column support
                        selectors = [s.strip() for s in selector.split(",") if s.strip()]
                        extracted_data = {}
                        for s in selectors:
                            data = scraper.extract_data(s, attribute if attribute else None)
                            extracted_data[s] = data
                    else:
                        st.error("Please provide a CSS selector.")
                
                if extracted_data:
                    df = scraper.to_dataframe(extracted_data)
                    
                    if not df.empty and df.count().sum() > 0:
                        # Standout Feature: Search/Filter results
                        st.subheader("Extracted Data Preview")
                        search_term = st.text_input("Filter results by text", placeholder="Type to search in the table...")
                        
                        if search_term:
                            df = df[df.apply(lambda row: row.astype(str).str.contains(search_term, case=False).any(), axis=1)]
                        
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

    # Professional Footer
    st.markdown("""
        <div class="footer">
            Developed by <b>Khushali Desai</b> | 
            <a href="https://www.linkedin.com/in/khushali-desai-2b1ab2282/?lipi=urn%3Ali%3Apage%3Ad_flagship3_profile_view_base_contact_details%3BdeTUIw7%2BSmyhZri6zSskrw%3D%3D" target="_blank">LinkedIn</a> | 
            <a href="https://github.com/kd-debug" target="_blank">GitHub</a>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
