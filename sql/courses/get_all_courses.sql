SELECT c.course_id, c.course_code, c.name, mg.group_id
FROM courses c
JOIN message_groups mg ON c.course_id = mg.course_id
WHERE mg.group_id NOT IN (
    SELECT group_id FROM group_members WHERE user_id = %s
)
ORDER BY c.course_code ASC