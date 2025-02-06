# PhobiaDB

This repository contains scripts used to populate my Phobia Database with data collected from various internet sources. The database includes information on different phobias, their symptoms, and associated questions.

## Directory Structure

- **ClevelandClinicScrape**: Scripts for scraping data from the Cleveland Clinic website.
- **WikipediaPhobiaScrape**: Scripts for scraping data from Wikipedia.
- **Data**: Holds folders over of years of scraped phobia information.
- **PhobiaApp**: Holds script for running the app (main.py) and for updating the database.
- **Tests**: Holds testing scripts for verifying api endpoints, disease processing, and clicks while crawling.

## Usage

To run the Flask application:

```
cd PhobiaApp/scripts
python main.py
```

To run the Cleveland Clinic Crawler:

```
cd ClevelandClinicScrape
python main.py
```

## Contributing

Contributions are welcome! If you have any suggestions or improvements, please fork the repository and submit a pull request. Ensure your contributions follow the existing code style and include appropriate documentation.

    1. Fork the repository
    2. Create your feature branch (git checkout -b feature/AmazingFeature)
    3. Commit your changes (git commit -m 'Add some AmazingFeature')
    4. Push to the branch (git push origin feature/AmazingFeature)
    5. Open a pull request


## License

This project is licensed under the MIT License. See the LICENSE file for details.
