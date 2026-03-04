UPDATE posts
SET comment_count = comment_count + 1
WHERE post_id = %s;