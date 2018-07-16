from keras.models import Model
from keras.layers import Input, add, Activation, Lambda, Flatten, Reshape, LeakyReLU, concatenate, Dense
from keras.layers.convolutional import Conv2D
from keras.layers.merge import Multiply
from keras.losses import binary_crossentropy
from keras import backend as K


def createModel():
	in1 = Input(shape=(6,7,3))
	in2 = Input(shape=(7,1))
	x = Conv2D(128, (3,3), activation = 'relu', padding = 'same')(in1)
	x = Conv2D(128, (3,3), activation = 'relu', padding = 'same')(x)
	x = Conv2D(128, (3,3), activation = 'relu', padding = 'same')(x)
	x = Conv2D(128, (3,3), activation = 'relu', padding = 'same')(x)
	x = Conv2D(128, (3,1), activation = 'relu', padding = 'valid')(x)
	x = Conv2D(128, (3,1), activation = 'relu', padding = 'valid')(x)
	x = Conv2D(128, (2,1), activation = 'relu', padding = 'valid')(x)
	x = Conv2D(1, (1,1), activation = 'sigmoid')(x)
	x = Reshape((7,1))(x)
	out = Multiply()([x, in2]) #Mask invalid moves
	model = Model(inputs=[in1, in2], outputs=out)
	model.compile(loss='mean_squared_error',optimizer='adam')
	#model.summary()
	return model