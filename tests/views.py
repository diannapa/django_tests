from django.shortcuts import render
import random

# Create your views here.


def shuffle_answers(questions):
    for question in questions:
        random.shuffle(question['answers'])
    return questions


def index(current_question_index=0):
    shuffled_questions = shuffle_answers(questions)
    session.setdefault('incorrect_answers', [])
    session.setdefault('correct_answers', [])
    print("Correct Answers in quiz:", session.get('correct_answers', []))
    print("Incorrect Answers in quiz:", session.get('incorrect_answers', []))

    return render(
        'quiz.html',
        context={
            'questions': shuffled_questions,
            'current_question_index': current_question_index,
            'total_questions': total_questions
        }
    )