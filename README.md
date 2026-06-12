# InsightScraper Pro 🔍

**InsightScraper Pro** is a professional-grade, minimalistic web scraping tool designed for precision data extraction. Developed as part of a Python Development Internship, this tool provides a seamless interface for extracting structured data from any website without requiring complex coding.

## 🚀 Features

- **Dual Extraction Modes**:
    - **Common Elements**: Instantly extract Titles, Links, and Images.
    - **Custom CSS Multi-Column**: Extract specific data points (prices, ratings, etc.) using comma-separated CSS selectors to build custom datasets.
- **Site Insights**: Automatically extracts and displays page metadata (Title, Description, Keywords) to provide context for your scraping tasks.
- **In-App Data Filtering**: Search and filter through extracted results directly within the UI.
- **Export Capabilities**: Download your structured data in professional **CSV** or **JSON** formats.
- **Minimalistic UI**: A clean, distraction-free interface designed for productivity, avoiding heavy colors and emojis.
- **Robust Error Handling**: Real-time feedback on connection status and data availability.

## 🛠️ Technology Stack

- **Python**: Core programming language.
- **Streamlit**: Web interface and interactive components.
- **BeautifulSoup4**: HTML parsing and data extraction.
- **Pandas**: Data manipulation and export processing.
- **Requests**: HTTP handling for website fetching.

## 📥 Installation

1. **Clone the repository**:
   ```bash
   git clone https://github.com/khushalidesai/InsightScraper-Pro.git
   cd InsightScraper-Pro
   ```

2. **Install dependencies**:
   ```bash
   py -m pip install -r requirements.txt
   ```

3. **Run the application**:
   ```bash
   py -m streamlit run app.py
   ```

## 📖 Usage Examples

### Scraping a Bookstore (Multiple Columns)
- **URL**: `https://books.toscrape.com`
- **Mode**: Custom CSS Selector
- **Selector(s)**: `h3 a, .price_color`
- **Result**: A correlated table of book titles and their respective prices.

### Extracting News Headlines
- **URL**: `https://news.ycombinator.com`
- **Mode**: Common Elements
- **Result**: All news titles and direct links extracted instantly.

## 👤 Developer
**Khushali Desai**
- [LinkedIn](https://linkedin.com/in/khushali-desai)
- [GitHub](https://github.com/khushalidesai)

---
*Developed as a project for Python Development Internship.*
