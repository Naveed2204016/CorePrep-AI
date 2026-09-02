CREATE TABLE IF NOT EXISTS company_exams (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    user_id INTEGER NOT NULL,
    company_slug VARCHAR(100) NOT NULL,
    company_name VARCHAR(200) NOT NULL,
    created_at DATETIME NOT NULL,
    INDEX ix_company_exams_user_id (user_id),
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS company_exam_questions (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    exam_id INTEGER NOT NULL,
    question_text TEXT NOT NULL,
    reference_answer TEXT NULL,
    position INTEGER NOT NULL,
    CONSTRAINT uq_company_exam_question_position UNIQUE (exam_id, position),
    INDEX ix_company_exam_questions_exam_id (exam_id),
    FOREIGN KEY (exam_id) REFERENCES company_exams(id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS company_exam_attempts (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    exam_id INTEGER NOT NULL,
    user_id INTEGER NOT NULL,
    score FLOAT NOT NULL DEFAULT 0,
    submitted_at DATETIME NOT NULL,
    CONSTRAINT uq_company_exam_attempt_user UNIQUE (exam_id, user_id),
    INDEX ix_company_exam_attempts_exam_id (exam_id),
    INDEX ix_company_exam_attempts_user_id (user_id),
    FOREIGN KEY (exam_id) REFERENCES company_exams(id) ON DELETE CASCADE,
    FOREIGN KEY (user_id) REFERENCES users(id)
);

CREATE TABLE IF NOT EXISTS company_exam_answers (
    id INTEGER AUTO_INCREMENT PRIMARY KEY,
    attempt_id INTEGER NOT NULL,
    question_id INTEGER NOT NULL,
    user_answer TEXT NOT NULL,
    score FLOAT NOT NULL,
    status VARCHAR(30) NOT NULL,
    feedback TEXT NOT NULL,
    suggested_answer TEXT NOT NULL,
    is_correct BOOLEAN NOT NULL,
    CONSTRAINT uq_company_exam_answer_question UNIQUE (attempt_id, question_id),
    INDEX ix_company_exam_answers_attempt_id (attempt_id),
    INDEX ix_company_exam_answers_question_id (question_id),
    FOREIGN KEY (attempt_id) REFERENCES company_exam_attempts(id) ON DELETE CASCADE,
    FOREIGN KEY (question_id) REFERENCES company_exam_questions(id) ON DELETE CASCADE
);
