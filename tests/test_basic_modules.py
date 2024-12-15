import pytest

# from test_variables import *
from utils.common_utils import load_env_variables
from utils.data_exploration import data_preparation_pipeline, get_widget_info


# @pytest.mark.skipif(True, reason="  skipped by Developer")
class Test_basic_Modules:

    def test_var_file_exists(verbose=0):
        # run the function
        load_env_variables()

    @pytest.mark.parametrize(
        "value, rate, digits, expected_arrow, expected_color",
        [
            (100, 0.5, 0, "cilArrowTop", "color:green;"),
            (10.36, -0.5, 1, "cilArrowBottom", "color:red;"),
            (-985810, 0, 2, "", "color:gray;"),
        ],
    )
    def test_widget_rate_Vs_green(
        self, value, rate, digits, expected_arrow, expected_color
    ):
        # test the value, rate pair
        result = get_widget_info(value, rate)

        # Assert
        assert result["arrow"] == expected_arrow
        assert result["color"] == expected_color

        # Remove rows with negative values in Price,
        # Quantity, Purch_Amt, Returns and Churn columns

    @pytest.mark.skipif(True, reason=" skipped because it takes long time")
    def test_remove_negative_values(self, verbose=1):
        from pyspark.sql import SparkSession

        # from pyspark.testing import assertDataFrameEqual

        columns = ["Price", "Quantity", "Purch_Amt", "Returns", "Churn"]
        test_data = [
            (10, 5, 50, 0, 1),
            (-10, 5, 50, 0, 1),
            (10, -5, 50, 0, 1),
            (10, 5, -50, 0, 1),
            (10, 5, 50, -1, 1),
            (10, 5, 50, 0, -1),
            (10, -5, 50, -1, 1),
            (-10, 5, -50, 0, -1),
        ]

        expected_data = [
            (10, 5, 50, 0, 1),
        ]

        # Building the SparkSession and name
        # it :'pandas to spark'
        spark = SparkSession.builder.appName(
            "test spark functions"
        ).getOrCreate()

        # Create the DataFrame with the help
        spark_df = spark.createDataFrame(test_data, columns)
        expected_result_df = spark.createDataFrame(expected_data, columns)

        # run the function
        result_df, _ = data_preparation_pipeline(spark, spark_df)

        if verbose > 0:
            result_df.show()
            expected_result_df.show()

        # #! bug: check the expected spark output
        # assertDataFrameEqual(
        #     result_df, expected_result_df, includeDiffRows=True
        # )
