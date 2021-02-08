import keras
from keras.utils import plot_model

from config import MODEL_DIR_PATH

restored_keras_model = keras.models.load_model(MODEL_DIR_PATH + 'mod_to_plot.h5')

plot_model(restored_keras_model, to_file='media/model.png')