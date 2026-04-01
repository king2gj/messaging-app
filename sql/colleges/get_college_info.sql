SELECT *
FROM colleges JOIN message_groups
ON message_groups.college_id = colleges.college_id
WHERE message_groups.group_id = %s