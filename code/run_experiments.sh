#!/bin/bash

# SCRIPT TO BATCH RUN EXPERIMENTS.
# WARNING: ITS CONTENT IS GOING TO FREQUENTLY CHANGE, AS WE ARE GOING TO CUSTOMIZE IT FOR EACH BATCH
# OF EXPERIMENTS WE WANT TO EXECUTE.

# Train SSD300 on TT100K detection dataset
#python train.py -c config/tt100k_ssd300.py -e baseline_ssd300

# Train SSD300 on Udacity dataset
#python train.py -c config/udacity_ssd300.py -e baseline_ssd300

# Evaluate baseline YOLO on the test set

python eval_detection_fscore.py yolo TT100K_detection ../../data/master/Experiments/TT100K_detection/baseline_yolo/weights.hdf5 /data/module5/Datasets/detection/TT100K_detection/test/

# Evaluate baseline YOLO on the training set

python eval_detection_fscore.py yolo TT100K_detection ../../data/master/Experiments/TT100K_detection/baseline_yolo/weights.hdf5 /data/module5/Datasets/detection/TT100K_detection/train/

# Evaluate baseline YOLO on the validation set

python eval_detection_fscore.py yolo TT100K_detection ../../data/master/Experiments/TT100K_detection/baseline_yolo/weights.hdf5 /data/module5/Datasets/detection/TT100K_detection/valid/

# Evaluate baseline YOLO on the test set

python eval_detection_fscore.py yolo TT100K_detection ../../data/master/Experiments/Udacity/baseline_yolo/weights.hdf5 /data/module5/Datasets/detection/Udacity/test/

# Evaluate baseline YOLO on the training set

python eval_detection_fscore.py yolo TT100K_detection ../../data/master/Experiments/Udacity/baseline_yolo/weights.hdf5 /data/module5/Datasets/detection/Udacity/train/

# Evaluate baseline YOLO on the validation set

python eval_detection_fscore.py yolo TT100K_detection ../../data/master/Experiments/Udacity/baseline_yolo/weights.hdf5 /data/module5/Datasets/detection/Udacity/valid/


# Evaluate YOLO improvements on the test set

python eval_detection_fscore.py yolo TT100K_detection ../../data/master/Experiments/TT100K_detection/yolo_improvements/weights.hdf5 /data/module5/Datasets/detection/TT100K_detection/test/

# Evaluate YOLO improvements on the training set

python eval_detection_fscore.py yolo TT100K_detection ../../data/master/Experiments/TT100K_detection/yolo_improvements/weights.hdf5 /data/module5/Datasets/detection/TT100K_detection/train/

# Evaluate YOLO improvements on the validation set

python eval_detection_fscore.py yolo TT100K_detection ../../data/master/Experiments/TT100K_detection/yolo_improvements/weights.hdf5 /data/module5/Datasets/detection/TT100K_detection/valid/

# Evaluate baseline tiny-YOLO on the test set

python eval_detection_fscore.py tiny-yolo TT100K_detection ../../data/master/Experiments/TT100K_detection/baseline_tiny_yolo/weights.hdf5 /data/module5/Datasets/detection/TT100K_detection/test/

# Evaluate baseline tiny-YOLO on the training set

python eval_detection_fscore.py tiny-yolo TT100K_detection ../../data/master/Experiments/TT100K_detection/baseline_tiny_yolo/weights.hdf5 /data/module5/Datasets/detection/TT100K_detection/train/

# Evaluate baseline tiny-YOLO on the validation set

python eval_detection_fscore.py tiny-yolo TT100K_detection ../../data/master/Experiments/TT100K_detection/baseline_tiny_yolo/weights.hdf5 /data/module5/Datasets/detection/TT100K_detection/valid/

# Evaluate baseline tiny-YOLO on the test set

python eval_detection_fscore.py tiny-yolo udacity ../../data/master/Experiments/Udacity/baseline_tiny_yolo/weights.hdf5 /data/module5/Datasets/detection/Udacity/test/

# Evaluate baseline tiny-YOLO on the training set

python eval_detection_fscore.py tiny-yolo udacity ../../data/master/Experiments/Udacity/baseline_tiny_yolo/weights.hdf5 /data/module5/Datasets/detection/Udacity/train/

# Evaluate baseline tiny-YOLO on the validation set

python eval_detection_fscore.py tiny-yolo udacity ../../data/master/Experiments/Udacity/baseline_tiny_yolo/weights.hdf5 /data/module5/Datasets/detection/Udacity/valid/

# Evaluate baseline SSD on the test set

python eval_detection_fscore.py ssd TT100K_detection ../../data/master/Experiments/TT100K_detection/baseline_ssd300/weights.hdf5 /data/module5/Datasets/detection/TT100K_detection/test/

# Evaluate baseline SSD on the training set

python eval_detection_fscore.py ssd TT100K_detection ../../data/master/Experiments/TT100K_detection/baseline_ssd300/weights.hdf5 /data/module5/Datasets/detection/TT100K_detection/train/

# Evaluate baseline SSD on the validation set

python eval_detection_fscore.py ssd TT100K_detection ../../data/master/Experiments/TT100K_detection/baseline_ssd300/weights.hdf5 /data/module5/Datasets/detection/TT100K_detection/valid/

# Train Yolo on Udacity dataset with Data Aumentation

#python train.py -c config/udacity_tiny_yolo_da.py -e tiny_yolo_da