SELECT colleges.name
FROM colleges JOIN courses
ON colleges.college_id = courses.college_id
WHERE courses.course_id = %s