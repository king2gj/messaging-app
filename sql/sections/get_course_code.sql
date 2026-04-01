SELECT courses.course_code
FROM courses JOIN sections
ON courses.course_id = sections.course_id
WHERE sections.section_id = %s