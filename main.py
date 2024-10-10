import numpy as np # linear algebra
import pandas as pd # data processing, CSV file I/O (e.g. pd.read_csv)
import os
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import FunctionTransformer, MinMaxScaler, OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.compose import ColumnTransformer
from sklearn.model_selection import train_test_split
import matplotlib.pyplot as plt

import seaborn as sns

train_data = pd.read_csv(os.path.join(os.getcwd(), 'titanic', 'train.csv'))
test_data = pd.read_csv(os.path.join(os.getcwd(), 'titanic', 'test.csv'))

features = ['Survived', 'Pclass', 'Sex', 'Age', 'SibSp', 'Parch', 'Fare', 'Embarked']

train_df = train_data[features]
train_df = train_df.dropna(subset=['Embarked'])
train_df['IsAgeMissing'] = train_df['Age'].isna().astype(int)
# y = train_df.pop('Survived')


# Apply the default theme
sns.set_theme()
sns.catplot(data=train_df, kind="swarm", x="Survived", y="Age", hue="Sex")
fig = plt.figure()
ax = fig.add_subplot(111)

plt.bar(train_df['Survived'], train_df['Age'])
plt.show(block=True)

# age_transformer = Pipeline(steps=[
#     ('imputer', SimpleImputer(strategy='constant', fill_value=-1)),
#     ('scaler', MinMaxScaler())])

# def log_transform(x):
#     return np.log1p(x+1.01)

# fare_transformer = Pipeline(steps=[
#     ('imputer', SimpleImputer(strategy='constant', fill_value=-1)),
#     ('scaler', FunctionTransformer(log_transform))])

# categorical_features = ['Embarked', 'Sex', 'Pclass']
# for col in categorical_features:
#     train_data[col] = train_data[col].astype('category')

# categorical_transformer = Pipeline(steps=[
#     ('imputer', SimpleImputer(strategy='most_frequent')),
#     ('OneHotEncoder', OneHotEncoder(drop= 'first',handle_unknown='error'))])

# preprocessor = ColumnTransformer(
#     transformers=[
#         ('age', age_transformer, ['Age']),
#         ('fare', fare_transformer, ['Fare']),
#         ('cat', categorical_transformer, categorical_features)],
#         remainder='passthrough'
# )


# from sklearn.ensemble import RandomForestClassifier

# RFmodel = RandomForestClassifier(n_estimators=100, max_depth=7, random_state=1)

# clf = Pipeline([
#     ('preprocessing', preprocessor),
#     ('model', RFmodel)
# ])

# X_train, X_test, y_train, y_test = train_test_split(
#     train_df, y, test_size=0.1, random_state=1)

# # Fit the pipeline to the data
# clf.fit(X_train, y_train)
# print("model score: %.3f" % clf.score(X_train, y_train))
# print("model score: %.3f" % clf.score(X_test, y_test))

# clf.fit(train_df, y)
# print("model score: %.3f" % clf.score(train_df, y))

# features = [item for item in features if item != 'Survived']
# test_df = test_data[features]
# test_df['IsAgeMissing'] = test_df['Age'].isna().astype(int)

# predictions = clf.predict(test_df)

# output = pd.DataFrame({'PassengerId': test_data.PassengerId, 'Survived': predictions})
# save_path = os.path.join(os.getcwd(), 'titanic', 'submission.csv')
# output.to_csv(save_path, index=False)
# print("Your submission was successfully saved!")