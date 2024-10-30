import random
from sklearn.ensemble import RandomForestClassifier
import pickle


def make_mouse_model():
    def get_target(num):
        if num >= 25:
            return 0  # Student is not paying attention
        else:
            return 1  # Student is probably paying attention

    mouse_clicked = [[0], [1], [25], [26]]
    target = [0, 1, 1, 0]
    mouse_clicked_class = {0: "Not paying attention", 1: "Paying attention"}

    for i in range(200):
        rand = random.randint(0, 100)
        mouse_clicked.append([rand])
        target.append(get_target(rand))

    # print(mouse_clicked)
    # print(target)

    model = RandomForestClassifier()
    model.fit(mouse_clicked, target)
    '''
    for i in range(10):
        rand = random.randint(0,50)
        pred = model.predict([[rand]])
        print('number of clicks: ' + str(rand))
        print('prediction: ' + str(mouse_clicked_class[pred[0]]))
    '''
    # To save the model
    filename = 'model/mouse_model.sav'
    pickle.dump(model, open(filename, 'wb'))
