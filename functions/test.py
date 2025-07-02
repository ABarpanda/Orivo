import joblib

clf = joblib.load('spam_model.pkl')
vectorizer = joblib.load('vectorizer.pkl')

def predict_spam(text):
    text_vec = vectorizer.transform([text])
    prediction = clf.predict(text_vec)[0]
    return "Spam" if prediction == 1 else "Ham"

print(predict_spam("Free money!!! Click here to claim your prize."))
print(predict_spam("Congratulations! You've won a $1000 Walmart gift card. Click here!"))