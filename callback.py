# Importing dependencies
import numpy as np
import tensorflow.keras as keras

# Class CustomCallback 
class CustomCallback(keras.callbacks.Callback):
    # This method intriduces some randomness in the prediction
    def sample(self, preds, temperature=1.0):
        preds = np.asarray(preds).astype('float64')
        preds = np.log(preds) / temperature
        exp_preds = np.exp(preds)
        preds = exp_preds / np.sum(exp_preds)
        probas = np.random.multinomial(1, preds, 1)
        return np.argmax(probas)
    
    # This method runs after each epoch
    def on_epoch_end(self, epoch, logs={}):
        sample_text = """#if UINTPTR_MAX == 0xffffffff
#define UPB_SIZE(size32, size64) size32
#else
#define UPB_SIZE(size32, size64) size64
#endif"""

        # Printing some info and predicted text
        print('\nCurrently at epoch {}'.format(epoch + 1))
        print('Starter text : {}'.format(sample_text))
        
        for temperature in [0.2, 0.5, 1.0, 1.2]:
            # Selecting first 40 characters
            review = sample_text[0:40]
            review = [ord(i) for i in review]
            
            # Predicting the next characters for 500 times
            for k in range(500):  
                # Predicting using the model
                temp = self.model.predict(np.array([review[k: k + 40]]))

                # Calling the sample method
                temp = self.sample(temp[0], temperature)

                # Appending the predicted charcter
                review.append(temp)
        

            print('\nGenerated text with temperature {}: {}'.format(temperature, ''.join([chr(i) for i in review])))