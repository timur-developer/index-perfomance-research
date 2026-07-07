DROP TABLE IF EXISTS student_activity;

CREATE TABLE student_activity (
    activity_id BIGINT PRIMARY KEY,
    student_id INTEGER NOT NULL,
    course_id INTEGER NOT NULL,
    faculty VARCHAR(32) NOT NULL,
    group_code VARCHAR(32) NOT NULL,
    activity_type VARCHAR(32) NOT NULL,
    status VARCHAR(32) NOT NULL,
    score INTEGER NOT NULL,
    created_at TIMESTAMP NOT NULL,
    updated_at TIMESTAMP NOT NULL,
    semester VARCHAR(16) NOT NULL
);
