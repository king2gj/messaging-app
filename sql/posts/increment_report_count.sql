UPDATE posts
SET report_count = report_count + 1
WHERE post_id = %s;