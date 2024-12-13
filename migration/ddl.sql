
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
    name VARCHAR(100) NOT NULL,
    occupied_load INT NOT NULL DEFAULT 0,
    max_load INT NOT NULL
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
    name VARCHAR(100) NOT NULL
);

COMMENT ON TABLE competencies IS 'Таблица, содержащая информацию о компетенциях';

-- Промежуточная таблица для связи групп и нагрузок
CREATE TABLE groups_loads (
    group_id INT REFERENCES groups(id) ON DELETE CASCADE,
    loads_id INT REFERENCES loads(id),
    PRIMARY KEY (group_id, loads_id)
--    FOREIGN KEY (group_id) REFERENCES groups(id) ON DELETE CASCADE
);

COMMENT ON TABLE groups_loads IS 'Промежуточная таблица для связи групп и нагрузок';

-- Промежуточная таблица для связи предметов и компетенций
CREATE TABLE competencies_subjects (
    competence_id INT REFERENCES competencies(id) ON DELETE CASCADE,
    subject_id INT REFERENCES subjects(id) ON DELETE CASCADE,
    PRIMARY KEY (competence_id, subject_id)
);

COMMENT ON TABLE competencies_subjects IS 'Промежуточная таблица для связи предметов и компетенций';

-- Промежуточная таблица для связи преподавателей и компетенций
CREATE TABLE competencies_teachers (
    competence_id INT REFERENCES competencies(id) ON DELETE CASCADE,
    teacher_id INT REFERENCES teachers(id) ON DELETE CASCADE,
    PRIMARY KEY (competence_id, teacher_id)
);

COMMENT ON TABLE competencies_teachers IS 'Промежуточная таблица для связи преподавателей и компетенций';

CREATE OR REPLACE PROCEDURE add_subject(
    name_p TEXT,
    semester_number_p INT,
    competence_names TEXT
)
LANGUAGE plpgsql AS $$
DECLARE
    subject_id INT;
    competence_name TEXT;
BEGIN

    INSERT INTO subjects (name, semester_number)
    VALUES (name_p, semester_number_p)
    RETURNING id INTO subject_id;

    FOREACH competence_name IN ARRAY string_to_array(competence_names, ',')
    LOOP
        INSERT INTO competencies_subjects (competence_id, subject_id)
        SELECT id, subject_id FROM competencies WHERE name = competence_name;
    END LOOP;
END;
$$;

CREATE OR REPLACE PROCEDURE add_teacher(
    name_t TEXT,
    available_workload_t INT,
    competence_names TEXT
)
LANGUAGE plpgsql AS $$
DECLARE
    teacher_id INT;
    competence_name TEXT;
BEGIN

    INSERT INTO teachers (name, max_load)
    VALUES (name_t, available_workload_t)
    RETURNING id INTO teacher_id;

    FOREACH competence_name IN ARRAY string_to_array(competence_names, ',')
    LOOP
        INSERT INTO competencies_teachers (competence_id, teacher_id)
        SELECT id, teacher_id FROM competencies WHERE name = competence_name;
    END LOOP;
END;
$$;

