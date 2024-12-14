# Import other modules not related to PySpark

import matplotlib

# Import PySpark related modules
from IPython.core.interactiveshell import InteractiveShell
from pyspark.sql.functions import col

# from pyspark.sql.types import *
from utils.spark_utils import count_missing_invalid_values

# from datetime import *
matplotlib.rcParams["figure.dpi"] = 100
InteractiveShell.ast_node_interpurchase = "all"


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
