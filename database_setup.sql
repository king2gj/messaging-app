CREATE DATABASE message_board;
USE message_board;

CREATE TABLE users (
  user_id      BIGINT UNSIGNED PRIMARY KEY,
  username     VARCHAR(32) NOT NULL UNIQUE,
  first_name   VARCHAR(32) NOT NULL,
  last_name    VARCHAR(32) NOT NULL,
  email        VARCHAR(32) NOT NULL UNIQUE,
  bio          VARCHAR(160) NOT NULL,
  is_admin     BOOLEAN NOT NULL,
  time_joined  TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE auth (
  user_id          BIGINT UNSIGNED PRIMARY KEY,
  hashed_password  BINARY(32) NOT NULL,
  salt_code        VARCHAR(32) NOT NULL,
  
  CONSTRAINT fk_auth__user
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE courses (
  course_code       VARCHAR(12) PRIMARY KEY,
  offering_college  VARCHAR(100) NOT NULL,
  name              VARCHAR(100) NOT NULL
);

CREATE TABLE sections (
  section_id      BIGINT UNSIGNED PRIMARY KEY,
  course_code     VARCHAR(12) NOT NULL,
  section_number  INT UNSIGNED NOT NULL,

  CONSTRAINT fk_section__course
    FOREIGN KEY (course_code) REFERENCES courses(course_code)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE message_groups (
  group_id     BIGINT UNSIGNED PRIMARY KEY,
  group_scope  TINYINT UNSIGNED NOT NULL,
  college      VARCHAR(100) NULL,
  course_code  VARCHAR(12) NULL,
  section_id   BIGINT UNSIGNED NULL,

  CONSTRAINT fk_message_group__course
    FOREIGN KEY (course_code) REFERENCES courses(course_code)
    ON DELETE CASCADE ON UPDATE CASCADE,

  CONSTRAINT fk_message_group__section
    FOREIGN KEY (section_id) REFERENCES sections(section_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE group_members (
  group_id  BIGINT UNSIGNED NOT NULL,
  user_id   BIGINT UNSIGNED NOT NULL,
  role      VARCHAR(20) NOT NULL,

  PRIMARY KEY (group_id, user_id),

  CONSTRAINT fk_group_member__group
    FOREIGN KEY (group_id) REFERENCES message_groups(group_id)
    ON DELETE CASCADE ON UPDATE CASCADE,

  CONSTRAINT fk_group_member__user
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE posts (
  post_id         BIGINT UNSIGNED PRIMARY KEY,
  parent_post_id  BIGINT UNSIGNED NULL,
  group_id        BIGINT UNSIGNED NOT NULL,
  user_id         BIGINT UNSIGNED NOT NULL,
  time_posted     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  comment_count   INT UNSIGNED NULL,
  like_count      INT UNSIGNED NOT NULL DEFAULT 0,
  dislike_count   INT UNSIGNED NOT NULL DEFAULT 0,
  report_count    INT UNSIGNED NOT NULL DEFAULT 0,

  CONSTRAINT fk_post__parent
    FOREIGN KEY (parent_post_id) REFERENCES posts(post_id)
    ON DELETE CASCADE ON UPDATE CASCADE,

  CONSTRAINT fk_post__group
    FOREIGN KEY (group_id) REFERENCES message_groups(group_id)
    ON DELETE CASCADE ON UPDATE CASCADE,

  CONSTRAINT fk_post__user
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE media (
  media_id   BIGINT UNSIGNED PRIMARY KEY,
  user_id    BIGINT UNSIGNED NULL,
  post_id    BIGINT UNSIGNED NULL,
  file_name  VARCHAR(100) NOT NULL,
  content    MEDIUMBLOB NOT NULL,

  CONSTRAINT fk_media__user
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE ON UPDATE CASCADE,

  CONSTRAINT fk_media__post
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE liked_posts (
  user_id  BIGINT UNSIGNED NOT NULL,
  post_id  BIGINT UNSIGNED NOT NULL,

  PRIMARY KEY (user_id, post_id),

  CONSTRAINT fk_liked_post__user
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE ON UPDATE CASCADE,

  CONSTRAINT fk_liked_post__post
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE disliked_posts (
  user_id  BIGINT UNSIGNED NOT NULL,
  post_id  BIGINT UNSIGNED NOT NULL,

  PRIMARY KEY (user_id, post_id),

  CONSTRAINT fk_disliked_post__user
    FOREIGN KEY (user_id) REFERENCES users(user_id)
    ON DELETE CASCADE ON UPDATE CASCADE,

  CONSTRAINT fk_disliked_post__post
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE reports (
  report_id       BIGINT UNSIGNED PRIMARY KEY,
  reporter_id     BIGINT UNSIGNED NOT NULL,
  post_id         BIGINT UNSIGNED NOT NULL,
  report_time     TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  report_content  VARCHAR(200) NOT NULL,

  CONSTRAINT fk_report__user
    FOREIGN KEY (reporter_id) REFERENCES users(user_id)
    ON DELETE CASCADE ON UPDATE CASCADE,

  CONSTRAINT fk_report__post
    FOREIGN KEY (post_id) REFERENCES posts(post_id)
    ON DELETE CASCADE ON UPDATE CASCADE
);