from sklearn import svm
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
import numpy as np
import pickle
from datasets import load_dataset
import pandas as pd
#from IPython.display import display
import random

# WASD Issue, listed as notes in DF, not due to lack of testing data


def make_keyboard_model():
    sizeLimit = 8000
    num_wasd = 1000
    dataset = load_dataset('daily_dialog', 'binary')
    #print(dataset)
    #print(dataset['train']['dialog'])
    combine_dialog = []
    for dialog in dataset['train']['dialog']:
        #print(dialog)
        combine_dialog.extend(dialog)

    class_target = ['dialog', 'note']

    df_dialog = pd.DataFrame(combine_dialog, columns=['text'])
    # Removes missing values; cleans up dataset/frame
    df_dialog = df_dialog.dropna()
    #print(df_dialog)
    df_dialog = df_dialog[:sizeLimit-num_wasd]

    # Attempts to add WASD Input into model
    wasdDict = {0: 'w', 1: 'a', 2: 's', 3: 'd', 4: ' '}
    wasdList = []
    for x in range(num_wasd):
        # x is the number of training lists
        numberKeyPresses = random.randint(10, 80)

        sentence = ""
        for y in range(numberKeyPresses):
            letter = wasdDict[random.randint(0,4)]
            if(random.randint(0,1) == 1):
                letter = letter.upper()
            sentence += letter
        wasdList.append([sentence])
    print(wasdList)

    wasdDF = pd.DataFrame(wasdList, columns = list(['text']))
    #print(wasdDF)
    df_dialog = pd.concat([df_dialog, wasdDF], ignore_index=True)

    print("-----------FIRST SEPARATOR-------------")
    # print(df_dialog.head(50))
    # print(df_dialog.tail(50))
    # print(df_dialog.style)
    df_dialog = df_dialog.dropna()

    # Add target to the dialog dataset
    print("-------------------Second Separator----------------------------")
    df_dialog['target'] = class_target.index("dialog")
    #print(df_dialog.head(50))
    # print(df_dialog.head(50))
    # print(df_dialog.tail(50))

    # Notes Dataset
    dataset = load_dataset('wikitext','wikitext-103-v1')
    # print(dataset)

    df_notes = pd.DataFrame(dataset['train'][:600000])

    # Removes empty strings
    df_notes['text'] = df_notes[df_notes['text'] != '']

    # Remove equal signs
    df_notes['text'] = df_notes[df_notes['text'].str.contains('=') == False]
    # Remove "@"s
    df_notes['text'] = df_notes[df_notes['text'].str.contains('@') == False]
    # Remove "<unk>"
    df_notes['text'] = df_notes[df_notes['text'].str.contains('<unk>') == False]
    # Remove none values
    df_notes = df_notes.dropna()
    df_notes['target'] = class_target.index('note')
    #print(df_notes.head(50))

    frames = [df_notes[:sizeLimit], df_dialog[:sizeLimit]]
    df = pd.concat(frames)
    #print(df)

    #Shuffle the Dataframe Rows
    print("Combined Dataframe information")
    print(df.head(100))
    print(df.tail(100))
    df = df.sample(frac = 1)
    print("-"*100)

    # WASD Inpout Issue occurs under test model or possibly under df, when the two dataframes (diaolog and notes) are combined
    # Tests Model?
    vectorizer = CountVectorizer(decode_error="replace")
    input_data = vectorizer.fit_transform(df['text'])

    #print(sorted(vectorizer.vocabulary_.items(), key = lambda x : x[1], reverse = True))
    #Save vectorizer.vocabulary_
    pickle.dump(vectorizer.vocabulary_, open("model/feature.pkl","wb"))
    print("Finished First Dump")

    # Classification Model
    model = svm.SVC()
    model.fit(input_data, df['target'])
    filename = 'model/keyboard_model.sav'
    pickle.dump(model, open(filename, 'wb'))
    print("Finished Second Dump")

    frames = [df_notes[-11:], df_dialog[-11:]]
    print("Dataframe Notes and Dialog")
    print(df_notes[-11:])
    # WASD INPUT is seen as having a target of 0, which is the target of dialog
    print(df_dialog[-11:])

    df_test = pd.concat(frames)
    print(df_test[-22:])

    sentences = df_test['text'].values
    print(sentences)
    test_data = vectorizer.transform(sentences)

    pred = model.predict(test_data)
    print(pred)
    for i, p in enumerate(pred):
        print(sentences[i])
        print(class_target[p])
        print("*"*100)




