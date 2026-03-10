UPDATE courses
SET section_count = section_count + 1
WHERE course_id = %s