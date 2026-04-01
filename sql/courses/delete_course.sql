DELETE courses
FROM courses JOIN message_groups
ON courses.course_id = message_groups.course_id
WHERE message_groups.group_id = %s