use BankDB;
/*
insert into customer
(customID,customPhone,customAddress,
customName,relName,relPhone,relEmail,relRelation)
values
("421381199811117854","18369238907","siu76",
"Lin","Song","18378905678","sqs@ssmk.com","father");

insert into customer
(customID,customPhone,customAddress,
customName,relName,relPhone,relEmail,relRelation)
values
("425681199812347854","18369248907","siu67276",
"Lin37","Sg","18378912678","syu@ssmk.com","mother");

delete from customer where customID="425681199812347854";

insert into customer
(customID,customPhone,customAddress,
customName,relName,relPhone,relEmail,relRelation)
values
("425681199812347854","18369248907","siu67276",
"Lin37","Sg","18378912678","syu@ssmk.com","mother");

insert into cus_and_cheAccount
(cust_customID,cheq_cusA_accountIDX)
values
("425681199812347854","7900");

insert into cusAccount
(accountIDX,bran_branchName,


insert into chequeAccount
(cusA_accountIDX,neg_limit)
values
("7900",000087.00);

select * from chequeAccount;
select * from cus_and_cheAccount;


insert into branch
(city,branchName)
values
("win","union");

insert into staff
(staffID,bran_branchName)
values
("421381198712345678","union");
*/

insert into cusAccount
(accountIDX,bran_branchName,staf_staffID,remain)
values
("1000","union","421381198712345678",3.56);

select * from cusAccount;
select * from staff;
select * from branch;


