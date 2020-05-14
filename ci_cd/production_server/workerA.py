from celery import Celery

from numpy import loadtxt
from keras.models import model_from_json
from keras.models import Sequential

model_json_file = './model.json'
model_weights_file = './model.h5'
data_file = './pima-indians-diabetes.csv'

def load_data():
    dataset =  loadtxt(data_file, delimiter=',')
    X = dataset[:,0:8]
    y = dataset[:,8]
    y = list(map(int, y))
    return X, y

def load_model():
    # load json and create model
    json_file = open(model_json_file, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    # load weights into new model
    loaded_model.load_weights(model_weights_file)
    #print("Loaded model from disk")
    return loaded_model

# Celery configuration
CELERY_BROKER_URL = 'amqp://rabbitmq:rabbitmq@rabbit:5672/'
CELERY_RESULT_BACKEND = 'rpc://'
# Initialize Celery
celery = Celery('workerA', broker=CELERY_BROKER_URL, backend=CELERY_RESULT_BACKEND)

@celery.task()
def add_nums(a, b):
   return a + b

@celery.task
def get_predictions():
    results ={}
    X, y = load_data()
    loaded_model = load_model()
    predictions = loaded_model.predict_classes(X)
    results['y'] = y
    results['predicted'] =[]
    #print ('results[y]:', results['y'])
    for i in range(len(results['y'])):
        #print('%s => %d (expected %d)' % (X[i].tolist(), predictions[i], y[i]))
        results['predicted'].append(predictions[i].tolist()[0])
    #print ('results:', results)
    return results

@celery.task
def get_accuracy():
    X, y = load_data()
    loaded_model = load_model()
    loaded_model.compile(loss='binary_crossentropy', optimizer='rmsprop', metrics=['accuracy'])

    score = loaded_model.evaluate(X, y, verbose=0)
    #print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1]*100))
    return score[1]*100

