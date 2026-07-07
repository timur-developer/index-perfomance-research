DROP TABLE IF EXISTS student_activity;

CREATE TABLE student_activity (
    activity_id BIGINT NOT NULL,
    student_id INT NOT NULL,
    course_id INT NOT NULL,
    faculty VARCHAR(32) NOT NULL,
    group_code VARCHAR(32) NOT NULL,
    activity_type VARCHAR(32) NOT NULL,
    status VARCHAR(32) NOT NULL,
    score INT NOT NULL,
    created_at DATETIME NOT NULL,
    updated_at DATETIME NOT NULL,
    semester VARCHAR(16) NOT NULL,
    PRIMARY KEY (activity_id)
) ENGINE=InnoDB;
