SELECT hashed_password, salt_code
FROM auth
WHERE user_id = %s