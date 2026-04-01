SELECT *
FROM sections JOIN message_groups
ON sections.section_id = message_groups.section_id
WHERE message_groups.group_id = %s