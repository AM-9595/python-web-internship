
CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    age INTEGER NOT NULL
);

CREATE TABLE tasks (
    id SERIAL PRIMARY KEY,
    title VARCHAR(255) NOT NULL,
    status VARCHAR(50) NOT NULL,
    user_id INTEGER REFERENCES users(id)
);


INSERT INTO users (name, email, age) VALUES
('Иван', 'ivan@example.com', 25),
('Мария', 'maria@example.com', 30),
('Петр', 'petr@example.com', 22);

INSERT INTO tasks (title, status, user_id) VALUES
('Завершить проект', 'в работе', 1),
('Написать отчёт', 'новая', 2),
('Обновить документацию', 'новая', 1),
('Создать презентацию', 'завершено', 3),
('Провести ревью кода', 'в работе', 2);


SELECT * FROM users;
SELECT * FROM tasks WHERE user_id = 1;
UPDATE tasks SET status = 'завершено' WHERE id = 1;
DELETE FROM tasks WHERE id = 4;
SELECT users.name, tasks.title, tasks.status
FROM users
JOIN tasks ON users.id = tasks.user_id;

CREATE INDEX idx_tasks_user_id ON tasks(user_id);