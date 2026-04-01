UPDATE message_groups
SET member_count = member_count + 1
WHERE group_id = %s