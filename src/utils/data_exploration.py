# Import other modules not related to PySpark
import os

import matplotlib
import numpy as np
import pandas as pd

# Import PySpark related modules
from IPython.core.interactiveshell import InteractiveShell
from pyspark.sql.functions import array_contains, col

# from pyspark.sql.types import *

# from datetime import *
matplotlib.rcParams["figure.dpi"] = 100
InteractiveShell.ast_node_interpurchase = "all"


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
        print(
            " string_columns "
            + f"[size= {len(string_columns)}] = {string_columns}"
        )
        print(
            " numeric_columns "
            + f"[size= {len(numeric_columns)}] = {numeric_columns}"
        )
        print(
            " array_columns "
            + f"[size= {len(array_columns)}] = {array_columns}"
        )
        print(
            " unkown_columns "
            + f"[size= {len(unkown_columns)}] = {unkown_columns}"
        )

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
        if (
            column in string_columns
        ):  # check string columns with None and Null values
            missing_count = spark_df.filter(
                col(column).eqNullSafe(None) | col(column).isNull()
            ).count()
            missing_values.update({column: missing_count})

        if column in numeric_columns:  # check None, NaN
            missing_count = spark_df.where(
                col(column).isin([None, np.nan])
            ).count()
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


def data_preparation_pipeline(spark, spark_df):
    print("\n\n - data preparation in process ...")

    # Replace 0 for null on only population column
    spark_df = spark_df.na.fill(value=0, subset=["Returns"])

    # remove the invalid value (negative price, quantity, others)
    nb_invalid_values = (
        spark_df.select("*")
        .where(
            (col("Price") < 0)
            | (col("Quantity") < 0)
            | (col("Purch_Amt") < 0)
            | (col("Returns") < 0)
            | (col("Churn") < 0)
        )
        .count()
    )
    total_nb_samples = spark_df.count()

    if nb_invalid_values >= 0:
        print(
            f"- {nb_invalid_values}/{total_nb_samples} "
            + f"invalid (negative) values found!!. \
            \n {100*nb_invalid_values/total_nb_samples}%"
            + " samples were removed from the dataset "
        )
        spark_df = spark_df.select("*").where(
            (col("Price") >= 0)
            & (col("Quantity") >= 0)
            & (col("Purch_Amt") >= 0)
            & (col("Returns") >= 0)
            & (col("Churn") >= 0)
        )

    # remove the invalid computation(s) of Purch_Amt=Price*Quantity
    nb_invalid_Purch_Amt_values = (
        spark_df.select("*")
        .where((col("Price") * col("Quantity") != col("Purch_Amt")))
        .count()
    )
    total_nb_samples = spark_df.count()

    if nb_invalid_Purch_Amt_values >= 0:
        print(
            f"- {nb_invalid_Purch_Amt_values}/{total_nb_samples} "
            + "invalid computation(s) of Purch_Amt=Price*Quantity are found!!.\
             \n {100*nb_invalid_Purch_Amt_values/total_nb_samples}% "
            + "samples were removed from the dataset "
        )
        spark_df = spark_df.select("*").where(
            (col("Price") * col("Quantity") == col("Purch_Amt"))
        )

    # count the missing values
    missing_invalid_df = count_missing_invalid_values(spark_df)

    return spark_df, missing_invalid_df


def get_widget_info(value, rate, digits=0):
    """
    build the attributes of the dashboard widget
    """
    # print(value, rate)
    # print(type(value), type(rate))

    rate = float(rate)
    if digits == 0:
        value = int(float(value))
    else:
        value = round(float(value), digits)

    # define the arrow direction and color
    if rate > 0:
        arrow = "cilArrowTop"
        color = "color:green;"
    elif rate == 0:
        arrow = ""
        color = "color:gray;"
    else:
        arrow = "cilArrowBottom"
        color = "color:red;"

    widget_dic = {
        "value": "{:,}".format(value),
        "rate": rate,
        "arrow": arrow,
        "color": color,
    }

    return widget_dic
