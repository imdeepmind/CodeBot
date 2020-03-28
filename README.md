# CodeBot

A LSTM based Deep Learning model that generates random C/C++ code.

> Note: Due to limited computational power, I have trained the model only on limited data

## Table of contents:
- [Introduction](#introduction)
- [Dataset](#dataset)
- [Model](#model)
- [Sample Results](#sample-results)
- [Dependencies](#dependencies)
- [File Structure](#file-structure)
- [Future Improvements](#future-improvements)
- [Acknowledgments](#acknowledgments)

## Introduction

Computer codes are complicated, hard to learn for Humans. Here in this project, I attempted to make a Deep Learning model that leanrs to code in C/C++ and generates samll snippets of random code.

## Dataset

For training such language model, I need huge amount of codes. So after some research, I decided to use [Google's Chromium project](https://github.com/chromium/chromium). Chromium is open sourced web browser, and contains huge amount of code that are mostly written in C/C++.

To get the data, I cloned the repo and find a list of all C/C++ codes.

## Model

Here I have used a sinple LSTM based model. The first layer in the model is a [Embedding](https://www.tensorflow.org/api_docs/python/tf/keras/layers/Embedding) layer. 

The second layer is LSTM cell. LSTM or Long Short Term Memory Recurrent Neural Network is a type of Neural Network, that is used for sequenced data. 

Finally a Dense layer with Softmax activation function for the output layer.

## Sample Results

Here are some the text that the model generated after training.

 TODO

## Dependencies

The project is developed using Python 3.6. Along with that, I have used Tensorflow 2.0, NLTK, sqlite etc.

For details information about the libraries that I have used, please check the `requirements.txt` file.

## File Structure

Following are the files in the project.
- callback.py - This class is used for generating some samples results after each epoch
- model.py - This file contains the class Model that performs everything
- main.py - In this file, I'm calling the all the methods in the class

## Future Improvements

  - The model is trained only on fraction of the available data, so training the model on entire data can improve the accuracy of the model.
  - LSTM cells are simple and naive. Some of the latest models, like GPT and/or Transformer models can do a better job.

## Acknowledgments
- [Chromium Dataset](https://github.com/chromium/chromium)
