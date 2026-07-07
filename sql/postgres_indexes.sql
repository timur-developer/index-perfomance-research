CREATE INDEX IF NOT EXISTS idx_pg_student_id ON student_activity(student_id);
CREATE INDEX IF NOT EXISTS idx_pg_created_at ON student_activity(created_at);
CREATE INDEX IF NOT EXISTS idx_pg_status ON student_activity(status);
CREATE INDEX IF NOT EXISTS idx_pg_status_created_at ON student_activity(status, created_at DESC);
CREATE INDEX IF NOT EXISTS idx_pg_course_score ON student_activity(course_id, score);
ANALYZE student_activity;
