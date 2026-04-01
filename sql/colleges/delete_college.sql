DELETE colleges
FROM colleges JOIN message_groups
ON colleges.college_id = message_groups.college_id
WHERE message_groups.group_id = %s