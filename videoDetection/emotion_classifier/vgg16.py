import warnings
warnings.simplefilter(action = 'ignore', category = FutureWarning)

import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'

import sys
import tensorflow as tf
import matplotlib.pyplot as plt
from tensorflow.keras import preprocessing, datasets, layers, models
from tensorflow.keras.applications.vgg16 import VGG16

class model:
  def __init__(self, train_path, val_path, test_path):
    # Define local directories where samples are stored
    self.samples_dir = {
      "train": train_path,
      "validation": val_path,
      "test": test_path
    }
    self.NUM_CLASSES = 2
  
  def create_data_generator(self):
    data_generator = {}

    for split in self.samples_dir:
      data_generator[split] = preprocessing.image_dataset_from_directory(
        self.samples_dir[split],
        labels = "inferred",
        label_mode = "categorical",
        class_names = ['Anger', 'Disgust', 'Fear', 'Happiness', 'Neutral', 'Sadness', 'Surprise'],
        color_mode = "rgb",
        batch_size = 32,
        image_size = (224, 224),
        shuffle = True,
        seed = None,
        validation_split = None,
        subset = None,
        interpolation = "bilinear",
        follow_links = False
      )

      # Optimize the dataset using buffered prefetching to avoid blocking I/O
      data_generator[split] = data_generator[split].prefetch(buffer_size = 32)
  
    return data_generator
  
  def define(self):
    model = VGG16(include_top = True, weights = None, input_shape = (224, 224, 3), pooling = 'avg', classes = self.NUM_CLASSES)

    return model.input, model.output
  
  def build(self, input_layer, output_layer, print_summary = False):
    model = models.Model(input_layer, output_layer)

    if print_summary:
      model.summary()

    return model

  def compile(self, model):
    optimizer = tf.keras.optimizers.Adam(learning_rate = 0.001)
    
    model.compile(loss  = "categorical_crossentropy",
                  optimizer = optimizer,
                  metrics = ["accuracy"])
    
    return model

  def fit(self, model, data_generator):
    history = model.fit(data_generator["train"],
                        validation_data = data_generator["validation"],
                        epochs = 40)
    return model, history

  def visualize_metrics(self, history):
    plt.plot(history.history["accuracy"], label = "Train Accuracy")
    plt.plot(history.history["val_accuracy"], label = "Validation Accuracy")
    plt.xlabel("Epoch")
    plt.ylabel("Accuracy")
    plt.xscale("linear")
    plt.yscale("linear")
    plt.grid(True)
    plt.ylim([0, 1])
    plt.legend(loc = "lower right")
    plt.show()
  
  def evaluate(self, model, data_generator):
    # Model evaluation
    test_loss, test_acc = model.evaluate(data_generator["test"])

    print(f"\n Test Loss: {test_loss}, Test Accuracy: {test_acc}")
  
  def run(self):
    data_generator = self.create_data_generator()
    input_layer, output_layer = self.define()
    model = self.build(input_layer, output_layer, print_summary = True)
    model = self.compile(model)
    model, history = self.fit(model, data_generator)
    self.visualize_metrics(history)
    self.evaluate(model, data_generator)

    return model, history
