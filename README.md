
Built by https://www.blackbox.ai

---

# News Scraper

## Project Overview
News Scraper is a web application built with Flask that scrapes news articles and provides them in a user-friendly format. The application uses a scheduler to periodically scrape new articles and caches the results for quick access. Users can view the latest articles on the homepage and can also access a generated RSS feed of the scraped articles.

## Installation

To install the project, you need to have Python and pip installed on your machine. Follow the steps below to get started:

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/news-scraper.git
   cd news-scraper
   ```

2. It is recommended to create a virtual environment to manage dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. Install the required packages:
   ```bash
   pip install flask
   ```

## Usage

To run the application, use the following command in your terminal:
```bash
python app.py
```

This will start the Flask web server, and you should be able to access the application at `http://127.0.0.1:5000/`. The homepage will display the latest articles, and you can access the RSS feed at `http://127.0.0.1:5000/rss`.

## Features
- **Home Page**: Displays a list of the latest articles scraped from various sources.
- **RSS Feed**: Provides an XML feed for users to subscribe and receive updates.
- **Cached Data**: Articles and RSS feed data are cached to reduce load times and improve performance.

## Dependencies
The application requires the following Python package:
- Flask: A micro web framework for Python.

If you need additional dependencies or libraries, they should be included in your `requirements.txt` or `setup.py`.

## Project Structure
```
news-scraper/
│
├── data/            # Directory to store the cached articles and RSS feed
│   ├── articles.json # JSON file to hold scraped articles
│   └── rss.xml      # XML file for the RSS feed
│
├── scraper/         # Package containing the scraping logic and scheduling
│   └── scheduler.py # Scheduler functions to handle scraping jobs
│
├── templates/       # HTML templates for rendering pages
│   └── index.html   # Main page template
│
└── app.py           # Main application file
```

## Contributing
Contributions are welcome! Feel free to open issues, submit pull requests, or provide feedback.

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.