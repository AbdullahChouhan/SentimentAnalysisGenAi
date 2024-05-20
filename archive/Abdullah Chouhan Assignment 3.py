print("Abdullah Chouhan: Assignment 3\n\nLoading models...")

try:
    import pandas as pd
    from sklearn.model_selection import train_test_split
    from sklearn.ensemble import RandomForestClassifier
    from sklearn.metrics import classification_report
except ModuleNotFoundError as e:
    print(f"Couldn't import modules: {e}")
    exit(1)
    
try:
    dataset = pd.read_csv("Breast_cancer_data.csv")
    print("Successfully accessed csv locally")
except FileNotFoundError as e:
    print(f"Couldn't access csv locally: {e}\nTrying online url instead")
    try:
        dataset = pd.read_csv('https://raw.githubusercontent.com/pkmklong/Breast-Cancer-Wisconsin-Diagnostic-DataSet/master/data.csv')
        print("Successfully accessed csv online")
    except Exception as e:
        print(f"Couldn't access csv online: {e}")
        exit(1)

print(f"\nPrinting dataset:\n{dataset}")

X = dataset.drop('diagnosis', axis=1)
y = dataset['diagnosis']

print("Splitting data into train and test sets...")
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

print("\nTraining model...")
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

y_pred = model.predict(X_test)
print(f"\nClassification report:\n{classification_report(y_test, y_pred)}")