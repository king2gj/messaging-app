UPDATE auth
SET hashed_password = %s, salt_code = %s
WHERE user_id = %s