SELECT p.post_id, p.name, p.content, p.created_at,
       p.like_count, p.comment_count, u.username
FROM posts p
JOIN users u ON p.user_id = u.user_id
WHERE p.post_id = %s