use LibraryManagementSystemDataModel;
-- Creating Books Table
CREATE TABLE books (
    id INT PRIMARY KEY,
    title VARCHAR(255),
    isbn VARCHAR(20) UNIQUE,
    publication_year INT,
    publisher VARCHAR(255));

-- Sample Data
INSERT INTO books VALUES 
(1, 'Database Systems', '9781234567890', 2020, 'Pearson'),
(2, 'Learning SQL', '9789876543210', 2018, 'O\'Reilly');

-- Creating Authors Table
CREATE TABLE authors (
    id INT PRIMARY KEY,
    first_name VARCHAR(100),
    last_name VARCHAR(100),
    birth_date DATE);
    
-- Sample data
INSERT INTO authors VALUES 
(1, 'John', 'Smith', '1975-06-15'),
(2, 'Jane', 'Doe', '1980-03-22');

-- Creating Book_Authors Table
CREATE TABLE book_authors (
    id INT PRIMARY KEY,
    book_id INT,
    author_id INT,
    FOREIGN KEY (book_id) REFERENCES books(id),
    FOREIGN KEY (author_id) REFERENCES authors(id));

-- Sample data
INSERT INTO book_authors VALUES 
(1, 1, 1),
(2, 2, 2);

CREATE TABLE book_copies (
    id INT PRIMARY KEY,
    book_id INT,
    copy_number INT,
    status VARCHAR(50),
    location VARCHAR(100),
    FOREIGN KEY (book_id) REFERENCES books(id));

-- Sample data
INSERT INTO book_copies VALUES 
(1, 1, 1, 'Available', 'Shelf A1'),
(2, 2, 1, 'Loaned', 'Shelf B2');






