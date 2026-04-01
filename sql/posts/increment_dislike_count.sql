UPDATE posts
SET dislike_count = dislike_count + 1
WHERE post_id = %s