Create table buytbl
(idNum number(8) not null primary key,
 userID char(8) not null,
 prodName nchar(6) not null,
 groupName nchar(4) ,
 price number(8) not null,
 amount char(3) not null,
 Foreign key (userID) references userTBL(userID)
 );
 
create sequence idSEQ;
insert into buytbl values(idSEQ.NEXTVAL, 'KBS', '�ȭ', NULL, 30, 2);
insert into buytbl values(idSEQ.NEXTVAL, 'KBS', '��Ʈ��', '����', 1000, 1);
insert into buytbl values(idSEQ.NEXTVAL, 'JYP', '�����', '����', 200, 1);
insert into buytbl values(idSEQ.NEXTVAL, 'BBK', '�����', '����', 200, 5);
insert into buytbl values(idSEQ.NEXTVAL, 'KBS', 'û����', '�Ƿ�', 50, 3);
insert into buytbl values(idSEQ.NEXTVAL, 'BBK', '�޸�', '����', 80, 10);
insert into buytbl values(idSEQ.NEXTVAL, 'SSK', 'å', '����', 15, 5);
insert into buytbl values(idSEQ.NEXTVAL, 'EJW', 'å', '����', 15, 2);
insert into buytbl values(idSEQ.NEXTVAL, 'EJW', 'û����', '�Ƿ�', 50, 1);
insert into buytbl values(idSEQ.NEXTVAL, 'BBK', '�ȭ', NULL, 30, 2);
insert into buytbl values(idSEQ.NEXTVAL, 'EJW', 'å', '����', 15, 1);
insert into buytbl values(idSEQ.NEXTVAL, 'BBK', '�ȭ', NULL, 30, 2);

