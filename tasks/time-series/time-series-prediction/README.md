# Time Series Prediction
In this project I tried to implement the stock market prediction using Keras and MLflow. For this I have trained a LSTM model

The MLflow model produced by running this example can be deployed to any MLflow supported endpoints. All the necessary image preprocessing is packaged with the model. The model can therefore be applied to image data directly. All that is required in order to pass new data to the model is to encode the image binary data as base64 encoded string in pandas DataFrame (standard interface for MLflow python function models). The included Python scripts demonstrate how the model can be deployed to a REST API endpoint for realtime evaluation or to Spark for batch scoring..

In order to include custom image pre-processing logic with the model, we define the model as a custom python function model wrapping around the underlying Keras model. The wrapper provides necessary preprocessing to convert input data into multidimensional arrays expected by the Keras model. The preprocessing logic is stored with the model as a code dependency.


The example contains the following files:

MLproject Contains definition of this project. Contains only one entry point to train the model.
conda.yaml Defines project dependencies. 
apple_stock_using_rnn.py Main entry point of the project. Handles command line arguments and possibly downloads the dataset.


# Running this Example
First, install MLflow (via pip install mlflow) and import keras and tensorflow from mlflow(import mlflow.keras and import mlflow.tensorflow)
call the autologging API using
mlflow.keras.autolog() to automatically log metrics and parameters to MLflow during training.


To train the model, run the example as a standard MLflow project:
mlflow run examples/keras-Lstm-example

