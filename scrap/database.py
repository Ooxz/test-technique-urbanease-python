# database.py

import logging

# Function to insert data into the database
def insert_data_into_database(conn, data):
    try:
        cursor = conn.cursor()

        for item in data:
            # Check if a record with the same advert_url already exists
            cursor.execute("SELECT id FROM adverts WHERE advert_url = %s", (item['Advert URL'],))
            existing_record = cursor.fetchone()

            if existing_record:
                # Record with the same advert_url exists, you can update it here
                logging.info("Updating existing record for %s", item['Advert URL'])
            else:
                # Record with the same advert_url does not exist, insert the new data
                # Define the SQL INSERT statement
                sql = """
                    INSERT INTO adverts (advert_title, advert_price, advert_surface, advert_url)
                    VALUES (%s, %s, %s, %s)
                """
                # Execute the INSERT statement with the data
                cursor.execute(sql, (
                    item.get('Advert Title', ''),
                    item.get('Advert price', ''),
                    item.get('Advert surface', ''),
                    item.get('Advert URL', ''),
                ))
                logging.info("Inserted new record for %s", item['Advert URL'])

        # Commit the changes to the database
        conn.commit()

        # Close the cursor
        cursor.close()

        logging.info("Data inserted into the database successfully")

    except Exception as e:
        # Handle exceptions and print error details
        logging.error("An error occurred while inserting data into the database: %s", str(e))
        conn.rollback()