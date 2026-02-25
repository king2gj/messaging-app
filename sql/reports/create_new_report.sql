INSERT INTO reports (report_id, reporter_id, post_id, report_content)
VALUES (UUID_SHORT(), %s, %s, %s);