UPDATE users
SET post_count = post_count + 1
WHERE user_id = %s