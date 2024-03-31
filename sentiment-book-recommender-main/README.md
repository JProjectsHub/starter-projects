# Movie to Book Recommendation Model - Intro to AI Project

Welcome to the README for our Intro to AI Project! In this document, we will provide you with comprehensive instructions on how to run our model. Please follow these steps carefully to ensure a smooth setup and execution.

# Prerequisites

Before you begin, ensure that you have the following prerequisites installed on your system:

- **Python 3.11+**: This model is developed using Python, so you need to have Python 3.11 or a higher version installed on your machine.

# NLTK Data Download

This project uses the Natural Language Toolkit (NLTK) for text processing tasks. To ensure proper functionality, you need to download additional NLTK resources: `punkt`, `stopwords`, and `wordnet`.

You can do this by running the following Python commands after installing the project dependencies:

```python
import nltk
nltk.download('punkt')
nltk.download('stopwords')
nltk.download('wordnet')
```

# Installing Project Dependencies

Install the required dependencies by running the following command from the project's root directory:

```bash
pip3 install -r requirements.txt
```

This command will fetch and install all the necessary libraries and packages needed for the model to run successfully.

## Additional installations
There are a few depenencies in requirements.txt that are related to evaluation portions of model, not the main model you will be running. 
If there are any issues with installing requirements.txt due to the sci-kit-surprise module, run these commands.

```bash
pip3 install --upgrade wheel
pip3 install --upgrade setuptools
pip3 install --upgrade setuptools wheel
```

# Running the model

Go into the models directory, and then run model_4.py

```bash
cd models
python3 model_4.py
```
This will start the model and bring up the menu options. 

1. Rate a Book
2. Get Book Recommendations from a Movie Title
3. Save Feedback and Exit

# 1. Rate a Book
 
With this input, the user can input a rating for a book. Follow the prompts that come up to input inlcluding inputing a user id to keep track of your preferences, as well as the book_id you want to rate and its rating. 

## User Id
    User_id = This can be any number to represent a user. Choose a unique number, and input all of your book ratings under this id.

    For the purposes of testing the model, user_id = 1 has some ratings uploaded already. 

## Book Id
    Book_Id is the index of a book within the cleaned_dataset.csv file. Use this id to select the book you wish to rate. 

## How this plays into the model

A user's book ratings help the model cater book reccomendations to their specific preferences, by modifying its internal matrices and calibrating the ratings of similar books. The model learns based on a user's unique preferences. 

##   The user feedback inputed in a session will NOT SAVE, until option 3 is selected. 

In order to save feedback(s) you have entered to the model, you must choose option 3 on the main menu.


# 2. Get a Book Recommendations from  Movie Title
Input a movie name and then your user id, and the model will give you a list of the 5 most appropriate book reccomendations. 

# 3. Save Feedback and Exit
This input is used to save the ratings you may have added to the model, and exit out. 


# Vision of how the model works

1. The new user asks for a book reccomendation based on a movie and gets a list of 5 reccomendations. 

2. The user 'reads' one of these reccomended books, and gives a rating back to the model using option 1 in main menu, under a user id they come up with. They then use option 3 to save their feedback.  

3. Rerunning the model under your user id will now give you more personalized reccomendations, as the model dynamically adapts its matrices based on your inputs. 

    If for example you rated a book extremely poorly, that book and similar books would be weighted as lower by the model. 

4. Different users will get different book reccomendations based on the relevance of their existing catalog of book ratings to the movie reccomendation they're requesting. The severity of their ratings relative to baseline user scores for those books will also impact the reccomended suggestions. 