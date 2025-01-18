from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import load_img
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.vgg16 import preprocess_input
from tensorflow.keras.applications.vgg16 import decode_predictions
from tensorflow.keras.applications.vgg16 import VGG16
import numpy as np
 
from tensorflow.keras.models import load_model
 
output = { 0:'aatrox',1:'anivia',2:'ashe',3:'braum'}



model = load_model('model_saved.h5')
 
image = load_img('anivia.png', target_size=(128, 128))
img = np.array(image)
img = img / 255.0
img = img.reshape(1,128,128,3)
label = model.predict(img)
print("Predicted Class: ", output[np.argmax(label) - 1])