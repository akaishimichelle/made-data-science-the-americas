import requests
import sqlite3
import pandas as pd
import os
import zipfile
import kagglehub


def extract_data_set(dataset_url):
    path = kagglehub.dataset_download(dataset_url)
    downloaded_files = os.listdir(path)
    
    csv_files = [f for f in downloaded_files if f.endswith('.csv')]        
    csv_file_path = os.path.join(path,csv_files[0])

    df = pd.read_csv(csv_file_path,delimiter=',')
    return df


def transformByYear(data) :
    year_1980_to_year_1990 = data['year'].between(1980,1990)
    year_2010_to_year_2020 = data['year'].between(2010,2020)
    data = data[year_1980_to_year_1990 + year_2010_to_year_2020]
    return data

def transformSelectColumns(data,columns):
    data = data[columns]
    return data

def transformMerge(data1, data2, onkey = ""):
    merged = data1.join(data2.set_index(onkey), on=onkey)
    return merged

# def transformAddColumns(mergedData):
#     mergedData[""]

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
    dataset.to_sql('database', conn, if_exists='replace', index = False)
    conn.close()

if __name__ == "__main__":
    
    urls = [
    "asaniczka/productivity-and-hourly-compensation-1948-2021",
    "asaniczka/poverty-level-wages-in-the-usa-dataset-1973-2022"
    ]

    select_poverty_columns = ["year", "annual_poverty-level_wage", "white_women_share_below_poverty_wages", "black_women_share_below_poverty_wages", "hispanic_women_share_below_poverty_wages"]
    select_productivity_columns = ["year", "net_productivity_per_hour_worked", "average_compensation", "women_median_compensation"]

    # EXTRACTION
    productivity_data_set = extract_data_set(urls[0])
    poverty_data_set = extract_data_set(urls[1])

    # TRANSFORMATION
    tf_productivity_dataset = transformByYear(productivity_data_set)
    tf_poverty_data_set = transformByYear(poverty_data_set)

    tf_productivity_dataset = transformSelectColumns(tf_productivity_dataset,select_productivity_columns)
    tf_poverty_data_set = transformSelectColumns(tf_poverty_data_set,select_poverty_columns)

    tf_merged_dataset = transformMerge(tf_productivity_dataset, tf_poverty_data_set, "year")
    tf_merged_dataset = transformFillMissingValuesWithMean(tf_merged_dataset)

    #print(tf_merged_dataset.shape)

    # LOAD
    loadDataSet(tf_merged_dataset)






