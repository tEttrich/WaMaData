import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

from pymongo import MongoClient

from sklearn.cluster import KMeans
from sklearn.neural_network import MLPClassifier
from sklearn.neural_network import MLPRegressor

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error, classification_report, confusion_matrix
from math import sqrt
from sklearn.metrics import r2_score

def calcFFT(accel,nrsamples):
    accel_without_mean = accel - np.mean(accel)  # Subtract mean Value to reduce the DC Offset in the FFT
    freq = np.fft.rfft(accel_without_mean, nrsamples, norm='ortho')
    freq = np.abs(freq)
    freq = freq / nrsamples  # Normalize the Amplitude by the known sample number
    return freq

def plotArrays(a_x, a_y, a_z, x_time, x_freq, LengthSample):
    global timeDia,fftDia

    ax_freq = calcFFT(a_x, LengthSample)
    ay_freq = calcFFT(a_y, LengthSample)
    az_freq = calcFFT(a_z, LengthSample)

    fftfig, (ax1, ax2, ax3) = plt.subplots(3)

    ax1.plot(x_time, a_x)
    ax1.plot(x_time, a_y)
    ax1.plot(x_time, a_z)

    ax2.plot(x_freq, ax_freq)  # plot FFT for x-accel
    ax2.plot(x_freq, ay_freq)  # plot FFT for y-accel
    ax2.plot(x_freq, az_freq)  # plot FFT for z-accel

    ax3.psd(a_x, NFFT=LengthSample, Fs=fs, window=np.blackman(LengthSample))  # plot ax-PSD
    ax3.psd(a_y, NFFT=LengthSample, Fs=fs, window=np.blackman(LengthSample))  # plot ay-PSD
    ax3.psd(a_z, NFFT=LengthSample, Fs=fs, window=np.blackman(LengthSample))  # plot az-PSD
    plt.show()


def createDataframe():
    ### Import Data from MongoDB Atlas Cloud Database
    print("Connecting to MongoDB")
    client = MongoClient("mongodb+srv://test:test@cluster1337.kv1ih.mongodb.net/IoTProjectData?ssl=true&ssl_cert_reqs=CERT_NONE")
    db = client.ProjectData
    col = db.Data
    print("Connected! Client:", db)

    cursor = col.find()
    print ("total docs in collection:", col.count_documents( {} ))

    print("Creating Dataframe from MongoDB Collection")
    df = pd.DataFrame(list(cursor))
    print("Dataframe created!")

    return df

def createPlot(Start, End):
    """

    :param Start: Unix epoch time der Start-DateTime aus Qt übergeben
    :param End: Unix epoch time der End-DateTime aus Qt übergeben
    :return: plot
    """
    ###  visualize Raw Data, fast Fourier transformation and Power-Spectral-Density
    #Timestamps = list(df['time'].unique())          # list all unique Timestamps
    #print(len(Timestamps), "Timestamps found.")

    #StartSample = Timestamps[0]
    #EndSample = Timestamps[1000]
    StartSample = Start
    EndSample = End

    print("Creating Dataframe from Timestamp",StartSample,"to Timestamp",EndSample)

    df_mask = df[df['time']>=StartSample]
    df_mask = df_mask[df_mask['time']<=EndSample]
    LengthSample = len(df_mask.index)               # Länge des aktuellen Samples ausgeben
    print("Dataframe created with", LengthSample, "Datasets")

    ax = df_mask['x_a'].values
    ay = df_mask['y_a'].values
    az = df_mask['z_a'].values

    fs = 100.0  # Sample Frequency 100 Hz
    Period = 1/fs

    x_time=np.linspace(0.0,Period*LengthSample,LengthSample)
    x_freq=np.linspace(0.0,fs/2.0,int(LengthSample/2)+1)

    print("Visualizing Raw Data, fast Fourier transformation and Power-Spectral-Density")
    plotArrays(ax,ay,az,x_time,x_freq,LengthSample)

def classifyTrain()
    df_train = df[['x_a', 'y_a', 'z_a']]
    # train KMeans
    train_clusters = KMeans(n_clusters=4).fit(df_train)

    # visualize clustered training Data
    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    xs = df_train['x_a']
    ys = df_train['y_a']
    zs = df_train['z_a']

    ax.scatter(xs, ys, zs, c = train_clusters.labels_)
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    df['status'] = pd.Series(list(train_clusters.labels_))

def trainTest():
    df_tt = df[['time', 'x_a', 'y_a', 'z_a', 'status']]
    target_column = ['status']
    predictors = list(set(list(df_tt.columns))-set(target_column))
    df_tt[predictors] = df_tt[predictors]/df_tt[predictors].max()

    # create train and test datasets
    X = df[predictors].values
    y = df[target_column].values

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.30, random_state=40)
    print(X_train.shape); print(X_test.shape)

    # Building, Predicting, and Evaluating the Neural Network Model
    mlp = MLPClassifier(hidden_layer_sizes=(8,8,8), activation='relu', solver='adam', max_iter=500)
    mlp.fit(X_train,y_train)

    predict_train = mlp.predict(X_train)
    predict_test = mlp.predict(X_test)

    print(confusion_matrix(y_train,predict_train))
    print(confusion_matrix(y_test,predict_test))