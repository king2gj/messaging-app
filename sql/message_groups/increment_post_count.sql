UPDATE message_groups
SET post_count = post_count + 1
WHERE group_id = %s