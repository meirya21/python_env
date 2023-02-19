from flask import Flask, render_template, session, request, redirect, jsonify 
import random 
import math

app = Flask(__name__)
app.secret_key = 'thisIsSecret'
random_decimal = random.randrange(0,100)

@app.route('/')
def index():
	session["victory"] = 0
	return render_template('guess.html')

@app.route('/process', methods=['POST'])
def process():
	if request.form.get('low'):
		low = int(request.form['low'])
		high = int(request.form['high'])
		randomValue = int(random.randint(low, high))
		Guesses = round(math.log(randomValue + 1, 2))

		if high - low < 9:
			Message = ("Thats to easy! The offset between the numbers needs to atleast be 10")
			return jsonify({'inputError' : Message})
		else:
			session['random_value'] = randomValue
			session['guess_value'] = Guesses
			guessLeft = str(session['guess_value'])
			print(session)

			Message = ("You've only " + str(Guesses)  + " chances to guess the integer!")
			return jsonify({'set' : Message, 'lowest' : low, 'highest' : high, 'guesses' : guessLeft})

	if request.form.get('guess'):
		guess = int(request.form['guess'])

		if session['random_value'] == guess:
			session['victory'] += 1
			score = session['victory']
			Message = ("Correct! The number was: " + str(guess))
			return jsonify({'won' : Message, 'score': score})

		elif session['random_value'] > guess:
			session['guess_value'] -= 1
			if session['guess_value'] == 0:
				session['victory'] -= 1
				score = session['victory']
				Message = ("Sadly you ran out of guesses, the number was " + str(session['random_value']) + ". please try again ")
				return jsonify({'error' : Message, 'guesses' : '0', 'score': score})
			else:
				Message = (str(guess) + " is to low! You have " + str(session['guess_value']) + " left")
				guessLeft = str(session['guess_value'])
				return jsonify({'wrong' : Message, 'guesses' : guessLeft})

		elif session['random_value'] < guess:
			session['guess_value'] -= 1
			if session['guess_value'] == 0:
				session['victory'] -= 1
				score = session['victory']
				Message = ("Sadly you ran out of guesses, the number was " + str(session['random_value']) + ". please try again ")
				return jsonify({'error' : Message, 'guesses' : '0', 'score': score})
			else:
				Message = (str(guess) + " is to high! You have " + str(session['guess_value'])  + " left")
				guessLeft = str(session['guess_value'])
				return jsonify({'wrong' : Message, 'guesses' : guessLeft})

	return jsonify({'error' : 'Some data is missing, please try again!'})

if __name__ == "__main__":
    app.debug = True
    app.run(host="0.0.0.0", port=5000)