import pytest

# from test_variables import *
from utils.common_utils import load_env_variables
from utils.data_exploration import get_widget_info


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


# @pytest.mark.skipif(True, reason="  skipped by Developer")
class Test_ML_Modules:
    @pytest.mark.parametrize(
        "num_epoch, expected_out",
        [
            (10, 10),
            (0, 21),
        ],
    )
    def test_module1(self, num_epoch, expected_out):
        # run the test
        out = expected_out
        assert out == expected_out
