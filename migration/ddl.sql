CREATE TYPE subject_enum AS ENUM ('Математика', 'Физика', 'Информатика');
-- Таблица Группа
CREATE TABLE groups (
    id SERIAL PRIMARY KEY,
    number VARCHAR(10) NOT NULL,
    student_count INT NOT NULL
);

COMMENT ON TABLE groups IS 'Таблица, содержащая информацию о группах студентов';

-- Таблица Предмет
CREATE TABLE subjects (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    semester_number INT NOT NULL
);

COMMENT ON TABLE subjects IS 'Таблица, содержащая информацию о предметах';

-- Таблица Нагрузка
CREATE TABLE load (
    id SERIAL PRIMARY KEY,
    load_type VARCHAR(50) NOT NULL, -- лекции, практические занятия и т.д.
    hours INT NOT NULL
);

COMMENT ON TABLE load IS 'Таблица, содержащая информацию о типах нагрузки и количестве часов';

-- Таблица Преподаватель
CREATE TABLE teachers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

COMMENT ON TABLE teachers IS 'Таблица, содержащая информацию о преподавателях';

-- Таблица Компетенция
CREATE TABLE competencies (
    id SERIAL PRIMARY KEY,
    name subject_enum NOT NULL -- Пример Enum
);

COMMENT ON TABLE competencies IS 'Таблица, содержащая информацию о компетенциях';

-- Промежуточная таблица для связи групп и нагрузок
CREATE TABLE groups_loads (
    group_id INT REFERENCES groups(id),
    load_id INT REFERENCES loads(id),
    PRIMARY KEY (group_id, load_id)
);

COMMENT ON TABLE student_subjects IS 'Промежуточная таблица для связи групп и нагрузок';