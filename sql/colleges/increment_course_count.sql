UPDATE colleges
SET course_count = course_count + 1
WHERE college_id = %s