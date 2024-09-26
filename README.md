# Automatic Subjective Answer Checker

This project is a web-based application that uses the Sentence-BERT model to compare student answers against model answers, providing automated grading and feedback. It's built using Flask for the backend and leverages `sentence-transformers` for semantic similarity assessment.
## Table of Contents
- [Features](#features)
- [Demo](#demo)
- [Installation](#installation)
- [Usage](#usage)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Routes](#routes)
- [Future Improvements](#future-improvements)
- [Contributing](#contributing)
- [License](#license)

## Features
- **Semantic Answer Checking:** Uses Sentence-BERT to calculate the similarity between student and model answers.
- **Automated Grading:** Provides grading based on similarity scores with customizable grading thresholds.
- **Admin Panel:** Allows adding and removing questions and model answers.
- **Real-time Feedback:** Displays grades and feedback immediately after submission.
- **Web-based Interface:** User-friendly interface for both students and administrators.

## Demo
A demonstration of the web-based automatic answer checker with different functionalities:

- **User Interface:** Students can answer questions and receive immediate feedback.
- **Admin Interface:** Admins can manage questions and review submitted answers.

## Usage

1. **Run the Flask application:**
   ```bash
   python app.py
   ```

2. **Access the web application:**
   Open your browser and go to `http://127.0.0.1:5000/`.

## Project Structure
```
automatic-answer-checker/
│
├── app.py                 # Main Flask application
├── templates/             # HTML template files for rendering pages
│   ├── home.html
│   ├── index.html
│   ├── result.html
│   ├── admin.html
├── data/
│   ├── questions.txt      # Contains list of questions
│   ├── model_answers.txt  # Contains corresponding model answers
├── requirements.txt       # List of dependencies
└── README.md              # Project description and instructions
```

## How It Works
1. **Loading Questions and Model Answers:** The app reads questions and model answers from `questions.txt` and `model_answers.txt`.
2. **Similarity Calculation:** Uses Sentence-BERT to calculate cosine similarity between student answers and model answers.
3. **Grading:** Grades are assigned based on similarity thresholds, which are customizable within the `grade_answer` function.
4. **Admin Management:** Admins can add or remove questions and answers through the web interface.

## Routes
| Route              | Description                                           |
|--------------------|-------------------------------------------------------|
| `/`                | Home page                                             |
| `/user`            | Displays questions for students to answer             |
| `/submit`          | Handles submission of student answers                 |
| `/result`          | Displays results (currently redirects to `/user`)      |
| `/admin`           | Admin page to manage questions and view statistics    |
| `/add_qa`          | Handles adding new question-answer pairs              |
| `/remove_qa`       | Handles removing question-answer pairs                |

## Future Improvements
- Implement user authentication for separate student and admin accounts.
- Enable uploading question/answer files directly via the admin interface.
- Add detailed grading reports and analysis for students.
- Extend the model to support different question types (e.g., multiple choice).

## Contributing
Contributions are welcome! Please follow these steps:
1. Fork the repository
2. Create a new branch (`git checkout -b feature-branch`)
3. Commit your changes (`git commit -m 'Add feature'`)
4. Push to the branch (`git push origin feature-branch`)
5. Open a Pull Request

## License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---
