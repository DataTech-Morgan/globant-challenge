CREATE TABLE gc_departments_rv (
id varchar(5) not null,
department varchar(20) not null
)

go

create table gc_hired_employees_rv(
id varchar(5) not null,
name varchar(50) not null,
datetime varchar(50) not null,
department_id varchar(5) not null,
job_id varchar(5) not null
)

go

create table gc_jobs_rv(
id varchar(5) not null,
job varchar(20) not null
)