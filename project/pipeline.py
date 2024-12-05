import sqlite3
import pandas as pd
import os
import zipfile
import kagglehub
from requests.exceptions import HTTPError, ConnectionError
import sys

def extract_data_set(dataset_url):
    try:
        path = kagglehub.dataset_download(dataset_url)
        downloaded_files = os.listdir(path)
        
        csv_files = [f for f in downloaded_files if f.endswith('.csv')]        
        csv_file_path = os.path.join(path,csv_files[0])

        df = pd.read_csv(csv_file_path,delimiter=',')

    except HTTPError as he:
        sys.exit("Invalid URL. Please enter correct URL for the dataset.")

    except ConnectionError as ce:
        sys.exit("Network issue. Please check you internet connection and retry.")

    except Exception as e:
        sys.exit("An error occured. Please retry.")    
    return df

def transformByYear(data):
    try:
        year_1980_to_year_1990 = data['year'].between(1980,1990)
        year_2010_to_year_2020 = data['year'].between(2010,2020)
        data = data[year_1980_to_year_1990 + year_2010_to_year_2020]

        if len(data) != 22:
          sys.exit("Insufficient data: Data does not cover 2 decades.")

    except KeyError as ke:
        sys.exit("The specified column does not exist in the dataset.")

    return data

def transformSelectColumns(data,columns):
        if len(columns) == 0:
         sys.exit("No columns specified. Please assign them again.")
       
        invalid_cols = [col for col in columns if col not in data.columns]

        #all columns are invalid
        if len(invalid_cols) == len(columns):
            sys.exit("Invalid columns: Please specify correct columns.")

        #some columns are valid
        else:
            valid_cols = [col for col in columns if col in data.columns]
            data = data[valid_cols]
            return data 

def transformMerge(data1, data2, onkey = ""):
    try:
        merged = data1.join(data2.set_index(onkey), on=onkey)
        return merged
    
    except KeyError as ke:
        sys.exit("The specified column(key) does not exist in the dataset.")

def transformFillMissingValuesWithMean(mergedData):
    yearColumn = "year"
    columnsWithMean = [col for col in mergedData.columns if col != yearColumn] 

    for col in columnsWithMean:
        mergedData.fillna({col:mergedData[col].mean()}, inplace=True)  # Fill NaNs with mean

    return mergedData

def loadDataSet(dataset):
    current_file = os.path.dirname(__file__)
    parent_directory = os.path.dirname(current_file)
    result = os.path.join(parent_directory, "data", 'productivity_compensation_and_poverty_level.db')

    conn = sqlite3.connect(result)
    dataset.to_sql('productivity_compensation_and_poverty_level', conn, if_exists='replace', index = False)
    conn.close()


def main():
    urls = [
    "asaniczka/productivity-and-hourly-compensation-1948-2021",
    "asaniczka/poverty-level-wages-in-the-usa-dataset-1973-2022"
    ]

    select_poverty_columns = ["year","jj", "annual_poverty-level_wage", "hourly_poverty-level_wage", "men_share_below_poverty_wages", "men_300%+_of_poverty_wages", "women_share_below_poverty_wages", "women_300%+_of_poverty_wages"]
    select_productivity_columns = ["year", "net_productivity_per_hour_worked", "average_compensation", "median_compensation", "men_median_compensation", "women_median_compensation"]

    # EXTRACTION
    productivity_data_set = extract_data_set(urls[0])
    poverty_data_set = extract_data_set(urls[1])

    # TRANSFORMATION
    tf_productivity_dataset = transformByYear(productivity_data_set)
    tf_poverty_data_set = transformByYear(poverty_data_set)

    tf_productivity_dataset = transformSelectColumns(tf_productivity_dataset,select_productivity_columns)
    tf_poverty_data_set = transformSelectColumns(tf_poverty_data_set,select_poverty_columns)
    print(tf_poverty_data_set.shape)

    tf_merged_dataset = transformMerge(tf_productivity_dataset, tf_poverty_data_set, "year")
    
    # LOAD
    loadDataSet(tf_merged_dataset)

if __name__ == "__main__":
    main()
   






