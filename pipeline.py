import pandas as pd
import logging
import asyncio
from app.adapters.db.postgres import engine

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_format)



async def load_data_from_csv_and_store(filename):
    # load the data from the csv file
    logging.info('Loading data from csv file - ' + filename + '.csv')
    df = pd.read_csv('./datastore/' + filename + '.csv')
    logging.info('Data loaded from csv file' + filename + '.csv')
    # create the engine to connect to the database - postgres
    logging.info('Creating engine to connect to the database')

    logging.info('Engine created to connect to the database')
    # write the data to the database
    logging.info('Writing data to the database from ' + filename + '.csv')
    
    df.to_sql(filename, con=engine, index=False, if_exists='append')

    logging.info('Data written to the database from ' + filename + '.csv')


async def main():
  fileName = ["store_business_hours", "store_status", "store_timezone"];
  tasks = [asyncio.create_task(load_data_from_csv_and_store(file)) for file in fileName]

  await asyncio.gather(*tasks)



if __name__ == '__main__':
  asyncio.run(main())
  









