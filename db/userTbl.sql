Create table userTBL
(userID char(8) not null primary key,
 userName NVARCHAR2(10) not null,
 birthYear number(4) not null,
 addr nchar(2) not null,
 mobile1 char(3),
 mobile2 char(8),
 height number(3),
 mDate date
 );
 
 Insert into usertbl values('LSG','�̽±�',1987,'����','011','11111111',182,'2008-8-8');
Insert into usertbl values('KBS','�����',1979,'�泲','011','22222222',173,'2012-4-4');
Insert into usertbl values('KKH','���ȣ',1971,'����','019','33333333',177,'2007-7-7');
Insert into usertbl values('JYP','������',1950,'���','011','44444444',166,'2009-4-4');
Insert into usertbl values('SSK','���ð�',1979,'����',NULL,NULL,186,'2013-12-12');
Insert into usertbl values('LJB','�����',1963,'����','016','66666666',182,'2009-9-9');
Insert into usertbl values('YJS','������',1969,'�泲',NULL,NULL,170,'2005-5-5');
Insert into usertbl values('EJW','������',1972,'���','011','88888888',174,'2014-3-3');
Insert into usertbl values('JKW','������',1965,'���','018','99999999',172,'2010-10-10');
Insert into usertbl values('BBK','�ٺ�Ŵ',1973,'����','011','00000000',176,'2013-5-5');
 