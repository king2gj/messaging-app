SELECT p.post_id, p.name, p.content, p.created_at,
       p.like_count, p.comment_count, p.creator_name
FROM posts p
JOIN message_groups mg ON p.group_id = mg.group_id
WHERE mg.course_id = %s
ORDER BY p.created_at DESC