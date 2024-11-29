#Deriving the latest base image
FROM tensorflow/tensorflow:latest

RUN pip install scikit-learn numpy pandas fpdf

#Labels as key value pair
LABEL Maintainer="won2013.tensorflow_sklearn"

# Any working directory can be chosen as per choice like '/' or '/home' etc
# I have chosen /usr/app/src
WORKDIR /usr/app/src