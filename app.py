from flask import Flask, render_template, request
import tensorflow as tf
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

app = Flask(__name__)

# Load the trained model
model = tf.keras.models.load_model('sentiment_analysis.hdf5')

# Load the tokenizer used during training
with open('tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)


@app.route('/')
def man():
    return render_template('index.html')


@app.route('/predict', methods=['POST'])
def index():
    text = request.form['review_text']

    # Preprocess the text input correctly
    sequences = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(sequences, padding='post', maxlen=100)

    # Make a prediction
    pred = model.predict(padded)[0][0]

    # Interpret the prediction
    if pred >= 0.5:
        s = 'Positive'
    else:
        s = 'Negative'

    # Calculate the confidence percentage
    percentage = pred * 100 if s == 'Positive' else (1 - pred) * 100
    success_message = "Prediction completed successfully!"
    return render_template('index.html', predict=s, given_text=text, percentage=percentage,success_message=success_message)


# if __name__ == "__main__":
#     app.run(debug=True)
