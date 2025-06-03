# Decision Tree Classification

# Importing the libraries

import numpy as np
import pandas as pd  
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import confusion_matrix, accuracy_score
from matplotlib import pyplot as plt

#import os  
#path = os.getcwd() 
#os.chdir(path)
 

# Importing the dataset 
dataset = pd.read_csv('./social_network_ads.csv')
# dataset = pd.read_csv('/adult_income.csv')
X = dataset.iloc[:, :-1].values
y = dataset.iloc[:, -1].values

# TODO: Visualize each feature and observe the plots to better understand 
# Write code scripts to plot the figures
plt.scatter(X[:, 0],X[:, 1], c=y)
plt.title('Social Network Advertisment')
plt.xlabel('Age')
plt.ylabel('Revenue')
plt.show()



# Splitting the dataset into the Training set and Test set
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size = 0.20, random_state = 0) # 80% train, 20% test

# Training the Decision Tree Classification model on the Training set
classifier = DecisionTreeClassifier(criterion = 'entropy', random_state = 0) # Use 'gini' for Gini impurity
classifier.fit(X_train, y_train)


# Predicting the Test set results
y_pred = classifier.predict(X_test)



#  Evaluate the model by making the Confusion Matrix
cm = confusion_matrix(y_test, y_pred) 
print(f"Confusion Matrix: \n {cm}")
 
accuracy = accuracy_score(y_test, y_pred)
print(f"Accuracy: {accuracy}")
 

# Visualize the decision tree  
plt.figure(figsize=(25,20))
tree.plot_tree(classifier, class_names=['no', 'yes'],  filled=True, rounded=True)
plt.show()



# Predicting a new result
new_data=[[30,87000]]
prediction = classifier.predict(new_data)
print(f"Prediction for new data: {prediction}")
 
# TODO: Observe the plotted tree to see if it is too complex or not
# write a code check whether or not there is an overfitting
# if the model is overfitting, fix the overfitting and show the plot results for before and after
y_train_pred = classifier.predict(X_train)
train_accuracy = accuracy_score(y_train, y_train_pred)
print(f"\nOriginal Tree:")
print(f"Training Accuracy: {train_accuracy}")
print(f"Test Accuracy: {accuracy}")

# Visualize original decision tree
plt.figure(figsize=(20, 15))
tree.plot_tree(classifier, class_names=['no', 'yes'], filled=True, rounded=True)
plt.title("Original Decision Tree (Possibly Overfitted)")
plt.show()

# If overfitting is suspected (training acc >> test acc), fix it by pruning the tree
if train_accuracy - accuracy > 0.1:
    print("\nModel might be overfitting. Training pruned tree...")

    pruned_classifier = DecisionTreeClassifier(criterion='entropy', max_depth=3, random_state=0)
    pruned_classifier.fit(X_train, y_train)

    # Predict and evaluate pruned model
    y_test_pred_pruned = pruned_classifier.predict(X_test)
    pruned_accuracy = accuracy_score(y_test, y_test_pred_pruned)
    print(f"Pruned Tree Test Accuracy: {pruned_accuracy}")

    # Visualize the pruned decision tree
    plt.figure(figsize=(20, 15))
    tree.plot_tree(pruned_classifier, class_names=['no', 'yes'], filled=True, rounded=True)
    plt.title("Pruned Decision Tree (max_depth=3)")
    plt.show()
else:
    print("No significant overfitting detected. No pruning applied.")


