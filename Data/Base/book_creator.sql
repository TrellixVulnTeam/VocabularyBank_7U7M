CREATE TABLE IF NOT EXISTS somename_of_book
(
    "index"	INTEGER NOT NULL UNIQUE,
    "word"	TEXT NOT NULL UNIQUE,
    "transcription"	TEXT,
    "translate"	TEXT NOT NULL UNIQUE,
    "association"	TEXT,
    "status"	INTEGER NOT NULL,
    PRIMARY KEY("index" AUTOINCREMENT)   
)