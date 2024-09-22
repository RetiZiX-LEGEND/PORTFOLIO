from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Feedback(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    email = db.Column(db.String(120), nullable=False)
    comment = db.Column(db.String(500), nullable=False)

with app.app_context():
    db.create_all()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        email = request.form.get('email')
        comment = request.form.get('text')
        
        if email and comment:
            new_feedback = Feedback(email=email, comment=comment)
            db.session.add(new_feedback)
            db.session.commit()
            print(f"Получено сообщение от {email}: {comment}")

    return render_template('index.html')

@app.route('/feedbacks')
def show_feedbacks():    
    feedbacks = Feedback.query.all()

    for feedback in feedbacks:
        print(f"ID: {feedback.id}, Email: {feedback.email}, Comment: {feedback.comment}")

    return "Отзывы отображены в терминале!"

if __name__ == "__main__":
    app.run(debug=True)
