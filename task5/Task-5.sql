create table department(
id serial primary key,
name varchar(50)
);

create table employee(
id serial primary key,
name varchar(50),
departmentid int references department(id),
salary int,
active int
);

insert into department (name) values
('IT'),
('Admin'),
('HR'),
('Accounts'),
('Health');

insert into employee (name,departmentid,salary,active) values
('John',1,2000,1),
('Sean',1,4000,1),
('Eric',2,2000,1),
('Nancy',2,2000,1),
('Lee',3,3000,1),
('Steven',4,2000,1),
('Matt',1,5000,1),
('Sarah',1,2000,0);

select * from department ;
select * from employee ;


--ascending order by salary
select * from employee order by salary;


--distinct salary
select distinct(salary) as distinct_salary from employee order by salary;


--total active employees
select count(active) from employee where active=1;


--updating department
update employee set departmentid=3 where name='Nancy';


--highest and second highest
select * from employee where
	salary=(select max(salary) from employee);

select * from employee where 
salary=(select max(salary) from employee
		where	
			salary<(select max(salary) from employee));
		
		
--department of each employee
select e.name,d.name 
	from employee e inner join department d
	on e.departmentid=d.id;	


--department with max employee
select name from department where 
	department.id =(select departmentid from employee where
					(departmentid=)
					
					
--department having most employee
select name from department where 
	id =(select departmentid  from employee e group by departmentid order by count(departmentid) desc limit 1);


--department with no employee
select name from department where
	department.id not in 
	(select departmentid from employee);


--same salary
select name,salary from employee 
	where 
	salary=(select salary from employee 
	group by salary having count(salary)>1);



