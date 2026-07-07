DROP INDEX idx_mysql_student_id ON student_activity;
DROP INDEX idx_mysql_created_at ON student_activity;
DROP INDEX idx_mysql_status ON student_activity;
DROP INDEX idx_mysql_status_created_at ON student_activity;
DROP INDEX idx_mysql_course_score ON student_activity;
ANALYZE TABLE student_activity;
