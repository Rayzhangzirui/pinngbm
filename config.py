import os
import tensorflow as tf

# Set data type
DTYPE='float32'
tf.keras.backend.set_floatx(DTYPE)


hostname = os.uname()[1].lower()

if 'gru' in hostname:
    DATADIR='~/pinndata'
elif 'hpc3' in hostname:
    DATADIR='/mnt/data/rzhang'
else:
    DATADIR='./'



