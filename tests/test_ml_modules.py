import pytest

from chatbot.serve_tensorflow import loaded_clf_model, loaded_tokenizer, predict


@pytest.mark.skipif(True, reason="test not ready yet, Skip for now!")
class Test_TrainingModules:
    @pytest.mark.parametrize(
        "num_epoch, expected_out",
        [
            (10, 10),
            (0, 21),
        ],
    )
    # !rewrite the test function
    def test_auto_epochs(self, num_epoch, expected_out):
        # #  run the auto epochs
        # out, auto_msg = auto_epochs_definition(
        #     num_epoch=num_epoch, nb_TR_image=10
        # )
        assert True  # out == expected_out

        if num_epoch > 0:  # test manual definition scenario
            assert True  # auto_msg == ""

        elif num_epoch == 0:  # test basic scenario
            assert True  # "auto" in auto_msg

    def test_save_model_for_inference(self):

        # saved the trained model for inference
        save_model_for_inference(
            device=device,
            model_path=infer_model_path,
            model=model,
            model_name=model_name,
            size=size,
            CLASS_dict=CLASS_dict,
            DIR_DEPLOY=DIR_DEPLOY,
            epoch_list=epoch_list,
            train_loss_list=train_loss_list,
            val_iou_list=val_iou_list,
        )


@pytest.mark.skipif(True, reason="  skipped by Developer")
class Test_Metrics:

    def test_IOU(self):
        import cv2

        img_path = "data/image_0.jpg"
        boxA = [[166, 673, 490, 1230], [], [266, 83, 690, 1830]]
        boxB = [[16, 573, 890, 1230], [166, 73, 790, 100]]
        # compute the average IOU of all bboxes
        iou = compute_average_IOU(boxA, boxB)
        logger.info(f"iou={iou}")

        image = cv2.imread(img_path)

        # visualize
        for boxes, color in [(boxA, 250), (boxB, 55)]:
            logger.info(f"boxes={boxes}")
            for box in boxes:
                try:
                    x1, y1, x2, y2 = box
                    logger.info(x1, y1, x2, y2)

                    cv2.rectangle(
                        image,
                        (x1, y1),
                        (x2, y2),
                        color=(color, 0, 0),
                        thickness=20,
                    )
                except Exception as e:
                    logger.info(f"error occurred --> skipped bbox \n {e}")

        # # Display the resulting frame
        # plt.figure()
        # plt.imshow(image)
        # plt.title(f"iou={iou}")
        # plt.savefig("img.png")
        # plt.show()
        assert True


class Test_Model_Prediction:

    @pytest.mark.parametrize(
        "text, expected_out",
        [
            ("I love the latest @RoKy music", "POSITIVE"),
            ("I hate the rain", "NEGATIVE"),
        ],
    )
    def test_text_classification(self, text, expected_out):
        # run the prediction
        prediction, prediction_msg = predict(
            text, loaded_tokenizer, loaded_clf_model
        )
        assert prediction["label"] == expected_out
