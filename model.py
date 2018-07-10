from keras.models import Model
from keras.layers import Input, add, Activation, Lambda, Flatten, Reshape, LeakyReLU, concatenate, Dense
from keras.layers.convolutional import Conv2D
from keras.layers.merge import Multiply
from keras.losses import binary_crossentropy
from keras import backend as K


def createModel():
	in1 = Input(shape=(6,7,3))
	x = Conv2D(64, (3,3), activation = 'relu', padding = 'same')(in1)
	x = Conv2D(64, (3,3), activation = 'relu', padding = 'same')(x)
	x = Conv2D(64, (3,3), activation = 'relu', padding = 'same')(x)
	x = Conv2D(64, (3,3), activation = 'relu', padding = 'same')(x)
	x = Conv2D(64, (3,3), activation = 'relu', padding = 'same')(x)
	x = Conv2D(64, (3,3), activation = 'relu', padding = 'same')(x)
	x = Flatten()(x)
	out = Dense(7, activation='sigmoid')(x)
	model = Model(inputs=in1, outputs=out)
	model.compile(loss='mean_squared_error',optimizer='adam')
	model.summary()
	return model