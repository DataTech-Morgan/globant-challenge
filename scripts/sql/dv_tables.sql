
create schema dv_gchallenge

go


create table dv_gchallenge.departments(
	department_id int,
	department varchar(30)
)

go


create table dv_gchallenge.hired_employees(
	employee_id int,
	employee varchar(50),
	date_time datetime,
    department_id int,
    job_id int
)

go

create table dv_gchallenge.jobs(
	id varchar(3),
	job varchar(50)
)

