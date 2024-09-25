from flask import Flask, render_template, request, redirect, url_for
from sentence_transformers import SentenceTransformer, util
import os

app = Flask(__name__)

# Initialize Sentence-BERT model
model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

# File paths
questions_file_path = 'D:\\ModelTraining\\pythonProject6\\data\\questions.txt'
answers_file_path = 'D:\\ModelTraining\\pythonProject6\\data\\model_answers.txt'

# Function to read questions and model answers
def read_questions_answers():
    with open(questions_file_path, 'r') as file_questions, open(answers_file_path, 'r') as file_answers:
        questions = file_questions.readlines()
        model_answers = file_answers.readlines()
    return questions, model_answers

questions, model_answers = read_questions_answers()

# Function to write questions and model answers back to files
def write_questions_answers(questions, model_answers):
    with open(questions_file_path, 'w') as file_questions, open(answers_file_path, 'w') as file_answers:
        file_questions.writelines(questions)
        file_answers.writelines(model_answers)

# Function to calculate similarity using Sentence-BERT
def calculate_similarity(model_answer, student_answer):
    model_embedding = model.encode(model_answer, convert_to_tensor=True)
    student_embedding = model.encode(student_answer, convert_to_tensor=True)
    similarity = util.pytorch_cos_sim(model_embedding, student_embedding)
    return similarity.item()

# Function to grade answer based on similarity and other heuristics
def grade_answer(student_answer):
    grades = []
    for model_answer in model_answers:
        similarity = calculate_similarity(model_answer, student_answer)
        if similarity > 0.9:
            grades.append(10)
        elif similarity > 0.8:
            grades.append(8)
        elif similarity > 0.7:
            grades.append(7)
        elif similarity > 0.6:
            grades.append(6)
        elif similarity > 0.5:
            grades.append(5)
        else:
            grades.append(0)
    return max(grades) if grades else 0

# Function to count occurrences of each question
def count_question_occurrences():
    question_counts = {}
    for question in questions:
        if question.strip() in question_counts:
            question_counts[question.strip()] += 1
        else:
            question_counts[question.strip()] = 1
    return question_counts

# Route for home page
@app.route('/')
def home():
    return render_template('home.html')

# Route for user panel
@app.route('/user')
def user():
    return render_template('index.html', questions=questions)

# Route for submitting answers
@app.route('/submit', methods=['POST'])
def submit():
    student_answers = []
    for i in range(len(questions)):
        student_answers.append(request.form[f'student_answer_{i}'])

    grades = [grade_answer(answer) for answer in student_answers]
    total_questions = len(questions)
    total_marks_possible = total_questions * 10
    total_marks_obtained = sum(grades)
    percentage_achieved = (total_marks_obtained / total_marks_possible) * 100 if total_marks_possible > 0 else 0

    # Prepare data for result table
    result_table = []
    for i in range(len(questions)):
        result_table.append({
            'question': questions[i].strip(),
            'marks_obtained': grades[i]
        })

    # Append total row to result table
    result_table.append({
        'question': 'Total',
        'marks_obtained': f'{total_marks_obtained}/{total_marks_possible}'
    })

    return render_template('result.html', result_table=result_table, percentage_achieved=percentage_achieved)

# Route for displaying result
@app.route('/result')
def result():
    return redirect(url_for('user'))  # Placeholder for now, can customize based on specific requirements

# Route for admin interface
@app.route('/admin')
def admin():
    question_counts = count_question_occurrences()
    total_questions = len(questions)
    total_marks = sum([10 for _ in range(total_questions)])  # Assuming max grade per question is 10
    percentage_achieved = (sum([10 for _ in range(total_questions)]) / (total_questions * 10)) * 100 if total_questions > 0 else 0

    return render_template('admin.html', questions=questions, question_counts=question_counts,
                           total_questions=total_questions, total_marks=total_marks,
                           percentage_achieved=percentage_achieved)

# Route for handling question and answer submission
@app.route('/add_qa', methods=['POST'])
def add_qa():
    question = request.form['question']
    model_answer = request.form['model_answer']

    # Append the question and answer to their respective lists
    questions.append(question + '\n')
    model_answers.append(model_answer + '\n')

    # Write back to files
    write_questions_answers(questions, model_answers)

    return redirect(url_for('admin'))

# Route for handling question removal
@app.route('/remove_qa', methods=['POST'])
def remove_qa():
    index = int(request.form['index'])

    # Remove question and model answer at specified index
    if 0 <= index < len(questions):
        del questions[index]
        del model_answers[index]

        # Write back to files
        write_questions_answers(questions, model_answers)

    return redirect(url_for('admin'))

if __name__ == '__main__':
    app.run(debug=True)
