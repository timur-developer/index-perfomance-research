db.student_activity.createIndex({ student_id: 1 }, { name: "idx_mongo_student_id" });
db.student_activity.createIndex({ created_at: 1 }, { name: "idx_mongo_created_at" });
db.student_activity.createIndex({ status: 1 }, { name: "idx_mongo_status" });
db.student_activity.createIndex({ status: 1, created_at: -1 }, { name: "idx_mongo_status_created_at" });
db.student_activity.createIndex({ course_id: 1, score: 1 }, { name: "idx_mongo_course_score" });
