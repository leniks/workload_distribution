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



-- Таблица Преподаватель
CREATE TABLE teachers (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL
);

COMMENT ON TABLE teachers IS 'Таблица, содержащая информацию о преподавателях';

-- Таблица Нагрузка
CREATE TABLE loads (
    id SERIAL PRIMARY KEY,
    load_type VARCHAR(50) NOT NULL, -- лекции, практические занятия и т.д.
    subject_id INT REFERENCES subjects(id),
    teacher_id INT REFERENCES teachers(id),
    hours INT NOT NULL
);

COMMENT ON TABLE loads IS 'Таблица, содержащая информацию о типах нагрузки и количестве часов';

-- Таблица Компетенция
CREATE TABLE competencies (
    id SERIAL PRIMARY KEY,
    name subject_enum NOT NULL -- Пример Enum
);

COMMENT ON TABLE competencies IS 'Таблица, содержащая информацию о компетенциях';

-- Промежуточная таблица для связи групп и нагрузок
CREATE TABLE groups_loads (
    group_id INT REFERENCES groups(id),
    loads_id INT REFERENCES loads(id),
    PRIMARY KEY (group_id, loads_id)
);

COMMENT ON TABLE groups_loads IS 'Промежуточная таблица для связи групп и нагрузок';

-- Промежуточная таблица для связи предметов и компетенций
CREATE TABLE competencies_subjects (
    competence_id INT REFERENCES competencies(id),
    subject_id INT REFERENCES subjects(id),
    PRIMARY KEY (competence_id, subject_id)
);

COMMENT ON TABLE competencies_subjects IS 'Промежуточная таблица для связи предметов и компетенций';

-- Промежуточная таблица для связи преподавателей и компетенций
CREATE TABLE competencies_teachers (
    competence_id INT REFERENCES competencies(id),
    teacher_id INT REFERENCES teachers(id),
    PRIMARY KEY (competence_id, teacher_id)
);

COMMENT ON TABLE competencies_teachers IS 'Промежуточная таблица для связи преподавателей и компетенций';

