delete from test where id =1 ;
insert into test values(1,'Sample question','option 1','option 2','option 3','option 4','option 3');
insert into test values(2,'Sample question','option 1','option 2','option 3','option 4','option 1');
insert into test values(3,'Sample question','option 1','option 2','option 3','option 4','option 2');
select * from test;
delete from test where 1=1;

create table test(id int, question varchar(2000),option_1 varchar(500),option_2 varchar(500),option_3 varchar(500),option_4 varchar(500),answer varchar(2000));
desc test;

create table teacher(
email varchar(100),
pa varchar(100)
);
delete from teacher where 1=1;
desc teacher;
insert into teacher values("t3@gmail.com","pa3");
select * from teacher;



create table student( prn varchar(50), pwd varchar(100),marks int);
insert into student values ('31','1234',0);
insert into student values ('37','1234',0);
select * from student;
select marks from student where prn="37";


SET SQL_SAFE_UPDATES = 0;