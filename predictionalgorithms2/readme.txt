Prediction Algorithms Project
==============================

Streamlit link : https://josephalexius-predictionalgo20260408.streamlit.app/

Purpose: 
    This project aims to demonstrate a compilation of four  machine learning algorithms: Linear Regression, Random Forest, Clustering, and Neural Networks.
    All models were trained and evaluated, then saved into a pickle (.pkl) file, then loaded into the program to perform predictions based from the input parameters
    displayed in each algorithm page.

About the program:
    - This project is developed using python and streamlit libraries. 
    - The project is contained in a folder named Prediction Algorithms. It also contains the environment with the libraries used and listed in requirements.txt file.
    - Each algorithm is modularized between the following files:
        - Linear Regression: This is the main program within the folder Prediction Algorithms and the front page of the application. 
            The python file is named as linear_regression.py.
        - Random Forest: Algorithm contained in the subfolder Pages with filename randomforest.py.
        - Clustering: Algorithm contained in the subfolder Pages with filename clustering.py.
        - Neural Networks: Algorithm contained in the subfolder Pages with filename neuralnetworks.py.

How to use the program for all algorithms:
    - Using streamlit cloud: Access the program through this link by copying and pasting in a new browser tab: https://josephalexius-predictionalgo20260408.streamlit.app/
    - Using local IDE: on the terminal, navigate to your folder path where linear_regression.py was contained.
        - Run the application by typing streamlit run linear_regression.py
    - Input or select values in the page.
    - Once done, click the predict button to generate the result.
    - The prediction result will be displayed below the button.

Logs:
    - The progam incorporated log functions that saves the trail in housing_app.log, contained in Prediction Algorithms folder.
