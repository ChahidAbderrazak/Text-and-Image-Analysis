import pytest

# from test_variables import *
from utils.common_utils import load_env_variables


# @pytest.mark.skipif(True, reason="  skipped by Developer")
class Test_basic_Modules:

    def test_var_file_exists(verbose=0):
        # run the function
        load_env_variables()


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
