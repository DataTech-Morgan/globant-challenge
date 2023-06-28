create schema rv_gchallenge

go

DROP TABLE if EXISTS rv_gchallenge.departments
create table rv_gchallenge.departments(
	id varchar(3),
	department varchar(30)
)
go
GRANT INSERT ON rv_gchallenge.departments TO gcsqladminuser;

COPY INTO rv_gchallenge.departments FROM 'https://adlsglobantmaind01.dfs.core.windows.net/data/RV/departments.csv'
WITH
(
FILE_TYPE='CSV',
CREDENTIAL = (IDENTITY= 'Shared Access Signature', 	 SECRET = '?sp=rcwd&st=2023-06-25T23:45:44Z&se=2023-06-26T07:45:44Z&spr=https&sv=2022-11-02&sr=c&sig=BXIRK1XuVvxOemsxUfhK4dVoS4qRXWXrJ%2Fk1IwV2Ykk%3D')
)

SELECT * FROM rv_gchallenge.departments
ORDER BY id
go

drop table rv_gchallenge.hired_employees
create table rv_gchallenge.hired_employees(
	id varchar(10),
	employee varchar(50),
	date_time varchar(50),
    department_id VARCHAR(3),
    job_id VARCHAR(3)
)
go
COPY INTO rv_gchallenge.hired_employees FROM 'https://adlsglobantmaind01.dfs.core.windows.net/data/RV/hired_employees.csv'
WITH
(
FILE_TYPE='CSV',
CREDENTIAL = (IDENTITY= 'Shared Access Signature', 	 SECRET = '?sp=rcwd&st=2023-06-25T23:45:44Z&se=2023-06-26T07:45:44Z&spr=https&sv=2022-11-02&sr=c&sig=BXIRK1XuVvxOemsxUfhK4dVoS4qRXWXrJ%2Fk1IwV2Ykk%3D')
)
SELECT * FROM rv_gchallenge.hired_employees
go
create table rv_gchallenge.jobs(
	id varchar(3),
	job varchar(50)
)
go
COPY INTO rv_gchallenge.jobs FROM 'https://adlsglobantmaind01.dfs.core.windows.net/data/RV/jobs.csv'
WITH
(
FILE_TYPE='CSV',
CREDENTIAL = (IDENTITY= 'Shared Access Signature', 	 SECRET = '?sp=rcwd&st=2023-06-25T23:45:44Z&se=2023-06-26T07:45:44Z&spr=https&sv=2022-11-02&sr=c&sig=BXIRK1XuVvxOemsxUfhK4dVoS4qRXWXrJ%2Fk1IwV2Ykk%3D')
)
SELECT * FROM rv_gchallenge.jobs