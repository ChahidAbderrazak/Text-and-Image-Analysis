# Import other modules not related to PySpark
import os

import matplotlib
import pandas as pd

# Import PySpark related modules
import pyspark
from IPython.core.interactiveshell import InteractiveShell
from pyspark.sql import SparkSession

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
            f"Invalid file extension ({file_extension}). "
            + "Please upload CSV/xlsx file types."
        )
