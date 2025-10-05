from flask import Flask, render_template, request, redirect, url_for, session
import random

app = Flask(__name__)
app.secret_key = "quiz_secret_key"

# 10 Python Questions
flashcards = [
    {"question": "Who created Python?", "options": ["Guido van Rossum", "Dennis Ritchie", "James Gosling", "Bjarne Stroustrup"], "answer": "Guido van Rossum"},
    {"question": "Which keyword is used to create a function in Python?", "options": ["func", "def", "function", "lambda"], "answer": "def"},
    {"question": "What is the output of 3 * 'abc'?", "options": ["abcabcabc", "abc3", "error", "3abc"], "answer": "abcabcabc"},
    {"question": "Which data type is immutable in Python?", "options": ["List", "Set", "Dictionary", "Tuple"], "answer": "Tuple"},
    {"question": "What does PEP stand for?", "options": ["Python Enhancement Proposal", "Programming Easy Practice", "Python Enterprise Project", "Practical Example Program"], "answer": "Python Enhancement Proposal"},
    {"question": "Which keyword is used for exception handling?", "options": ["catch", "error", "try", "exception"], "answer": "try"},
    {"question": "What is the default value of 'end' in print()?", "options": ["\\n", "space", "tab", "none"], "answer": "\\n"},
    {"question": "Which operator is used for floor division?", "options": ["//", "/", "%", "**"], "answer": "//"},
    {"question": "Which of these is not a core data type in Python?", "options": ["List", "Dictionary", "Class", "Tuple"], "answer": "Class"},
    {"question": "Which module in Python supports regular expressions?", "options": ["regex", "pyregex", "re", "regexp"], "answer": "re"}
]

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/start", methods=["POST"])
def start():
    session["nickname"] = request.form["nickname"]
    session["score"] = 0
    session["current_index"] = 0
    session["questions"] = random.sample(flashcards, len(flashcards))  # shuffle questions
    return redirect(url_for("index"))

@app.route("/quiz")
def index():
    if session["current_index"] >= 10:
        return redirect(url_for("result"))

    card = session["questions"][session["current_index"]]
    return render_template("index.html",
                           card=card,
                           score=session["score"],
                           nickname=session["nickname"],
                           current_index=session["current_index"])

@app.route("/answer", methods=["POST"])
def answer():
    question = request.form["question"]
    selected = request.form["option"]
    correct = request.form["correct"]

    is_correct = (selected == correct)
    if is_correct:
        session["score"] += 1

    session["current_index"] += 1

    return render_template("answer.html",
                           question=question,
                           selected=selected,
                           correct=correct,
                           is_correct=is_correct,
                           score=session["score"],
                           nickname=session["nickname"])

@app.route("/result")
def result():
    return render_template("result.html",
                           score=session["score"],
                           total=10,
                           nickname=session["nickname"])

if __name__ == "__main__":
    app.run(debug=True)
