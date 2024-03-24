from flask import Flask, render_template, request, redirect, url_for, session
import json
import random


def load_questions(json_file):
    with open(json_file, 'r', encoding='utf-8') as file:
        questions = json.load(file)
    return questions


app = Flask(__name__)
app.secret_key = 'htencxn0'
json_file = 'output.json'
questions = load_questions(json_file)
total_questions = len(questions)


def shuffle_answers(questions):
    for question in questions:
        random.shuffle(question['answers'])
    return questions


@app.route('/quiz/<int:current_question_index>')
def index(current_question_index=0):

    shuffled_questions = shuffle_answers(questions)
    session.setdefault('incorrect_answers', [])
    session.setdefault('correct_answers', [])
    print("Correct Answers in quiz:", session.get('correct_answers', []))
    print("Incorrect Answers in quiz:", session.get('incorrect_answers', []))

    return render_template(
        'quiz.html',
        questions=shuffled_questions,
        current_question_index=current_question_index,
        total_questions=total_questions
    )


@app.route('/submit/<int:current_question_index>', methods=['POST'])
def submit(current_question_index):
    user_answer = request.form.get('user_answer').strip()
    print(user_answer)
    correct_answer = questions[current_question_index]['right_answer'].strip()
    is_correct = user_answer == correct_answer
    if not is_correct:
        session.setdefault('incorrect_answers', []).append(
            current_question_index + 1)
    else:
        session.setdefault('correct_answers', []).append(
            current_question_index + 1)

    session.modified = True

    print(questions[current_question_index])
    print(user_answer == correct_answer, user_answer, correct_answer, sep=' | ')

    print("Correct Answers:", session.get('correct_answers', []))
    print("Incorrect Answers:", session.get('incorrect_answers', []))

    return render_template(
        'result.html',
        is_correct=is_correct,
        current_question_index=current_question_index,
        question=questions[current_question_index]
    )


@app.route('/next/<int:current_question_index>')
def next_question(current_question_index):
    print(current_question_index, "PREPARING NEXT QUESTION")
    session.modified = True
    if current_question_index + 1 < len(questions):
        return redirect(url_for(
            'index',
            current_question_index=current_question_index + 1,
            total_questions=total_questions
        ))
    else:
        return render_template('quiz_completed.html')


@app.route('/show_answer/<int:current_question_index>', methods=['POST'])
def show_answer(current_question_index):
    return render_template(
        'result.html',
        is_correct=False,
        question=questions[current_question_index],
        show_answer=True,
        current_question_index=current_question_index
    )


@app.route('/hide_answer/<int:current_question_index>', methods=['POST'])
def hide_answer(current_question_index):
    return render_template(
        'result.html',
        is_correct=False,
        question=questions[current_question_index],
        show_answer=False,
        current_question_index=current_question_index
    )


if __name__ == "__main__":
    app.run(debug=True)
