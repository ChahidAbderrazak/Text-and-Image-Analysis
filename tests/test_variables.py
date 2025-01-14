import os

import numpy as np


# from lib.Autils_Object_detection import load_class_dict
# from lib.networks import get_model_instance
# from lib.utils import extract_experiment_parameters

# configuration file
config_file = "config/config.yml"

# load a demo dict
# growth_dict = load_dict_from_json(filepath="data/test/growth_rate_dict.json")

# testing database samples
valid_data = {
    "name": "user",
    "description": "This is a test description",
    "price": 12.3,
}
update_data = {  # update product id=0 with
    "name": "user2",
    "description": "This is a test description [updated]",
    "price": 1236.5,
}

invalid_data = [
    {
        "name": "user3",
        "description": 12,
        "price": 5e40,  # DECIMAL(10, 2): max 10 digits
    },
]


# files and directories
IMAGE_ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets")
FAKEDATA_DIR = os.path.join(IMAGE_ROOT, "fakedata")
IMAGE_DIR = os.path.join(FAKEDATA_DIR, "imagefolder")
DAMAGED_JPEG = os.path.join(IMAGE_ROOT, "damaged_jpeg")
ENCODE_JPEG = os.path.join(IMAGE_ROOT, "encode_jpeg")

# # extract the parameters from the config_file
# (
#     device,
#     DIR_WORKSPACE,
#     RAW_DATA_ROOT,
#     dev,
#     CSV_TRAIN_FILE,
#     CSV_TEST_FILE,
#     CSV_DEPLOY_FILE,
#     DIR_TRAIN,
#     DIR_TEST,
#     DIR_DEPLOY,
#     size,
#     model_name,
#     model_path,
#     num_epoch,
#     N_split,
#     num_workers,
#     step_size,
#     gamma,
#     transfer_learning,
#     momentum,
#     weight_decay,
#     lr_scheduling,
#     verbose,
#     lr_list,
#     batch_size_list,
#     optimizer_list,
#     es_patience_ratio_list,
#     infer_model_path,
# ) = extract_experiment_parameters(config_file=config_file)

# # load classes
# CLASS_dict, classes = load_class_dict(CSV_TRAIN_FILE)

# # model instantiation
# model = get_model_instance(model_name, classes)

# demo trining data
vect_length = 10
epoch_list = [k for k in range(vect_length)]
train_loss_list = np.random.normal(0, 10, vect_length)
val_iou_list = np.random.normal(0, 1, vect_length)

assert len(epoch_list) == len(train_loss_list) == len(val_iou_list)

# IOU thresholds
iou_thresholds = [x for x in np.arange(0.5, 0.76, 0.05)]
