from sqlalchemy import create_engine
import pandas as pd
import logging
from multiprocessing import Process

log_format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
logging.basicConfig(level=logging.DEBUG, format=log_format)



def load_data_from_csv_and_store(filename):
    # load the data from the csv file
    logging.info('Loading data from csv file - ' + filename + '.csv')
    df = pd.read_csv('./datastore/' + filename + '.csv')
    logging.info('Data loaded from csv file' + filename + '.csv')
    # create the engine to connect to the database - postgres
    logging.info('Creating engine to connect to the database')
    engine = create_engine('postgresql://postgres:postgres@localhost:5432/store_monitor')
    logging.info('Engine created to connect to the database')
    # write the data to the database
    logging.info('Writing data to the database from ' + filename + '.csv')
    df.to_sql(filename, engine, index=False, if_exists='replace')
    logging.info('Data written to the database from ' + filename + '.csv')

fileName = ["menu-hours", "store-status", "store-timezone"];

if __name__ == '__main__':
  for file in fileName:
    p = Process(target=load_data_from_csv_and_store, args=(file,))
    p.start()
    p.join()






