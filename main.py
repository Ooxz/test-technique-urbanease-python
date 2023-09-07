import logging
import os
from bs4 import BeautifulSoup
import requests
import json
import psycopg2
from scrap.conf import config
from scrap.database import insert_data_into_database 

# Specify the full path to the log file
log_file_path = config['log_file_path']

# Create the parent directory for the log file if it doesn't exist
log_dir = os.path.dirname(log_file_path)
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configure logging with the specified log file path
logging.basicConfig(filename=log_file_path, level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Define the database connection information
# code I entered to create my table on pgadmin4 in table => qsl tool
#
# CREATE TABLE adverts (
# id SERIAL PRIMARY KEY,
# advert_title VARCHAR(255),
# advert_price VARCHAR(255),
# advert_surface VARCHAR(255),
# advert_url VARCHAR(255) UNIQUE (unique to make sure no duplicate in URL and so no duplicate advert)
#
# to check if it works in pgadmin4 go in the table, 
# here adverts => query tool and type SELECT * FROM adverts; then run it

conn = psycopg2.connect(
    host=config['db_host'],
    database=config['db_name'],
    user=config['db_user'],
    password=config['db_password']
)

# Function to scrape and save data
def scrape_and_save(url):
    scraped_data = []

    for page in range(1, 3):  # Scrape two pages (you can adjust this as needed)
        # Append the page parameter to the URL
        page_url = f"{url}&page={page}"

        logging.info("Scraping page %d", page)  # Log the page being scraped

        html_text = requests.get(page_url).text
        soup = BeautifulSoup(html_text, "lxml")
        adverts = soup.find_all('div', class_='offers-list__item')

        for advert in adverts:
            adverts_price_label = advert.find('span', class_='badge__label')
            # Check if Prix is present
            if adverts_price_label and 'Prix' in adverts_price_label.text:
                adverts_price_surface = advert.find_all('div', class_='badge__content')
                adverts_title = advert.find('header', class_='offer-card__header').text.replace(' ', '')
                adverts_url = advert.find('a').get('href')

                if adverts_url:  # Check if href exists
                    advert_data = {
                        'Advert Title': adverts_title.strip(),
                        'Advert price': adverts_price_surface[0].text.strip(),
                        'Advert surface': None,
                        'Advert URL': f'https://www.cessionpme.com{adverts_url}',
                    }

                    if len(adverts_price_surface) >= 2:
                        advert_data['Advert surface'] = adverts_price_surface[1].text.strip()

                    scraped_data.append(advert_data)

                    # Log the number of advertisements found on the page
                    logging.info("Found %d advertisements on page %d", len(scraped_data), page)

    return scraped_data

# Function to generate dynamic URLs for all departments and categories
def generate_urls(base_url, output_folder, departments, categories, rubrique_imo_mapping):
    for department in departments:
        department_data = {'Locaux, Entrepôts, Terrains': [], 'Bureaux, Coworking': []}  # Create a dictionary for department data

        for category in categories:
            # Generate the URL dynamically for each department and category
            rubrique_imo = rubrique_imo_mapping.get((department, category), "")  # Default to "V" if not found
            url = f"{base_url}&departement_imo={department}&secteur_activite_imo={category}&rubrique_imo={rubrique_imo}"

            # Log a message indicating the URL being scraped
            logging.info("Scraping URL: %s", url)

            try:
                # Scrape the data and store it in the dictionary
                scraped_data = scrape_and_save(url)

                # Define the output file name based on department
                if department == '93':
                    department_output_file = f"{output_folder}/resultats_64.json"  # Rename for department 93
                elif department == '87':
                    department_output_file = f"{output_folder}/resultats_33.json"  # Rename for department 87
                else:
                    department_output_file = f"{output_folder}/resultats_{department}.json"  # Default naming for other departments

                # Log a message indicating where the data is being saved
                logging.info("Data for department %s saved to %s", department, department_output_file)

                # Add category data to department data
                department_data[category] = scraped_data

                # Save the department data in the JSON file with the appropriate name
                with open(department_output_file, 'w') as f:
                    json.dump(department_data, f, indent=4)

                # Log a message indicating that data for the department has been saved
                logging.info("Data for department %s saved to %s", department, department_output_file)

                # Insert the scraped data into the database
                insert_data_into_database(conn, scraped_data)  # Call insert_data_into_database with conn and scraped_data
            except Exception as e:
                # Handle exceptions and log error details
                logging.error("An error occurred while processing department %s: %s", department, str(e))

# Base URL without department and category
base_url = "https://www.cessionpme.com/index.php?action=affichage&annonce=offre&moteur=OUI&type_moteur=imo&nature_imo=V&region_imo=2&commune_imo=0&multiple_lieu_imo&trap_imo&ou_imo&surfmin&et&immo_tri=prix&immo_tri=prix&surfmax&entre&entre_dab&et_dab&cwkg_rent_max&cwkg_places_min&motcle_imo"

# List of departments and categories (93 for department 64 and 87 for department 33)
departments = ['93', '87']  # Add more departments as needed
categories = ['Locaux, Entrepôts, Terrains', 'Bureaux, Coworking']  # Add more categories as needed

# Define rubrique_imo values for specific department and category combinations
rubrique_imo_mapping = {
    ('93', 'Locaux, Entrepôts, Terrains'): "", 
    ('87', 'Locaux, Entrepôts, Terrains'): "",
    ('93', 'Bureaux, Coworking'): "52",
    ('87', 'Bureaux, Coworking'): "52",
}

# Output folder for JSON files
output_folder = 'scrap/datas'

try:
    # Generate URLs and scrape data for all departments and categories
    generate_urls(base_url, output_folder, departments, categories, rubrique_imo_mapping)

    # Log a message indicating the completion of the script
    logging.info("Script completed successfully.")
    
    logging.info("Scraped data saved to JSON files.")
except Exception as e:
    # Handle unexpected exceptions and log error details
    logging.error("An unexpected error occurred: %s", str(e))

