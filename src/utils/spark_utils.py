# Import other modules not related to PySpark
import os

import matplotlib
import numpy as np
import pandas as pd

# Import PySpark related modules
import pyspark
from IPython.core.interactiveshell import InteractiveShell
from pyspark.sql import SparkSession
from pyspark.sql.functions import array_contains, col

# from pyspark.sql.types import *

# from datetime import *
matplotlib.rcParams["figure.dpi"] = 100
InteractiveShell.ast_node_interpurchase = "all"


# %matplotlib inline
def init_spark(MAX_MEMORY="15G"):
    # Initialize a spark session.
    conf = (
        pyspark.SparkConf()
        .setMaster("local[*]")
        .set("spark.executor.heartbeatInterval", 10000)
        .set("spark.network.timeout", 10000)
        .set("spark.core.connection.ack.wait.timeout", "3600")
        .set("spark.executor.memory", MAX_MEMORY)
        .set("spark.driver.memory", MAX_MEMORY)
    )
    # initait ethe sperk session
    spark = (
        SparkSession.builder.appName("Pyspark guide").config(conf=conf).getOrCreate()
    )
    return spark


# ---------------------- Spark basic functions -----------------------------


def spark_load_data(spark, filename_path):

    filename, file_extension = os.path.splitext(filename_path)

    # save file-like object for CSV reader
    if file_extension == ".xlsx":
        df = pd.read_excel(filename_path)
        spark_df = spark.createDataFrame(df)

    elif file_extension == ".csv":
        spark_df = spark.read.option("header", True).csv(filename_path)

    else:
        raise Exception(
            f"Invalid file extension ({file_extension}). "
            + "Please upload CSV/xlsx file types."
        )

    # displays
    # spark_df.toPandas().describe()
    print(f"There are total={spark_df.count()} rows")
    print("Raw data :\n", spark_df.limit(5).toPandas())
    return spark_df


def save_sample_data(df, filepath, nrows=100):
    """
    extract random sample data of nrows sample in <filename_path>
    """
    filename, file_extension = os.path.splitext(filepath)
    # extract random sample data of nrows samples
    df_sample = df.sample(n=nrows).reset_index().drop(columns="index")
    print(df_sample.head())

    # save file-like object for CSV reader
    if file_extension == ".xlsx":
        df_sample.to_excel(filepath, index=False)
    elif file_extension == ".csv":
        df_sample.to_csv(filepath)
    else:
        raise Exception(
            f"Invalid file extension ({file_extension}).\
              \n Please upload CSV/xlsx file types."
        )


def categorize_columns(spark_df, verbose=1):
    string_columns = []
    numeric_columns = []
    array_columns = []
    timestamp_columns = []
    unkown_columns = []
    for col_name, data_type in spark_df.dtypes:
        # print(f"({col_name},{col_name})")
        if data_type == "string":
            string_columns.append(col_name)
        elif data_type == "array":
            array_columns.append(col_name)
        elif data_type == "timestamp":
            timestamp_columns.append(col_name)
        elif (
            "int" in data_type
            or "long" in data_type
            or "float" in data_type
            or "double" in data_type
        ):
            numeric_columns.append(col_name)
        else:
            unkown_columns.append((col_name, data_type))
    if verbose > 0:
        print(
            " timestamp_columns "
            + f"[size={len(timestamp_columns)}]={timestamp_columns}"
        )
        print(" string_columns " + f"[size= {len(string_columns)}] = {string_columns}")
        print(
            " numeric_columns " + f"[size= {len(numeric_columns)}] = {numeric_columns}"
        )
        print(" array_columns " + f"[size= {len(array_columns)}] = {array_columns}")
        print(" unkown_columns " + f"[size= {len(unkown_columns)}] = {unkown_columns}")

    return (
        string_columns,
        numeric_columns,
        array_columns,
        timestamp_columns,
        unkown_columns,
    )


def count_missing_invalid_values(spark_df):
    # get the columns categories
    (
        string_columns,
        numeric_columns,
        array_columns,
        timestamp_columns,
        unkown_columns,
    ) = categorize_columns(spark_df, verbose=0)
    #  count the missing values
    missing_values = {}
    for index, column in enumerate(spark_df.columns):
        if column in string_columns:  # check string columns with None and Null values
            missing_count = spark_df.filter(
                col(column).eqNullSafe(None) | col(column).isNull()
            ).count()
            missing_values.update({column: missing_count})

        if column in numeric_columns:  # check None, NaN
            missing_count = spark_df.where(col(column).isin([None, np.nan])).count()
            missing_values.update({column: missing_count})

        if column in timestamp_columns:  # check Null
            missing_count = spark_df.filter(
                col(column).eqNullSafe(None) | col(column).isNull()
            ).count()
            missing_values.update({column: missing_count})

        if column in array_columns:  # check zeros and NaN
            missing_count = spark_df.filter(
                array_contains(spark_df[column], 0)
                | array_contains(spark_df[column], np.nan)
            ).count()
            missing_values.update({column: missing_count})
    # count the missing percentage
    nb_samples = 100 / spark_df.count()  # normalization factor
    missing_values_percentage = {
        column: nb_samples * missing_count
        for (column, missing_count) in missing_values.items()
    }

    # show the mising values table
    missing_invalid_df = pd.DataFrame(missing_values, index=["count"])
    missing_percentage_df = pd.DataFrame(
        missing_values_percentage, index=["percentage"]
    )
    missing_invalid_df = pd.concat([missing_invalid_df, missing_percentage_df])
    return missing_invalid_df
