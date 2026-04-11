SELECT c.course_id, c.course_code, c.name, mg.group_id
FROM courses c
JOIN message_groups mg ON c.course_id = mg.course_id
JOIN group_members gm ON mg.group_id = gm.group_id
WHERE gm.user_id = %s
ORDER BY c.course_code ASC