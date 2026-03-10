UPDATE posts
SET like_count = like_count + 1
WHERE post_id = %s