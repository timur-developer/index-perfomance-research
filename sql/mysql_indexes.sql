CREATE INDEX idx_mysql_student_id ON student_activity(student_id);
CREATE INDEX idx_mysql_created_at ON student_activity(created_at);
CREATE INDEX idx_mysql_status ON student_activity(status);
CREATE INDEX idx_mysql_status_created_at ON student_activity(status, created_at DESC);
CREATE INDEX idx_mysql_course_score ON student_activity(course_id, score);
ANALYZE TABLE student_activity;
