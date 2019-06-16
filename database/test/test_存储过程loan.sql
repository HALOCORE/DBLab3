-- select count(*), sum(loanPayAmount) from loanPay group by loan_loanIDX;
-- call proc_check_loan();

-- call proc_pay_loan('58740452588532331214', '2019-06-13 8:21:00', 3200);

-- select * from loan where loanIDX = '58740452588532331214';
-- select * from loanPay where loan_loanIDX = '58740452588532331214';


-- select * from loanPay where loan_loanIDX = '16397893085173404939';
-- call proc_pay_loan("16397893085173404939", "2019-06-15 17:03:28", 100.0);

-- select * from loan where loanIDX = '00324367137289128057';
-- select * from cus_and_loan where loan_loanIDX = '00324367137289128057';
-- delete from loanPay where loan_loanIDX = '00449782256351403988';
-- commit;
-- select * from loanPay where loan_loanIDX = '00324367137289128057';
-- call proc_delete_loan('00324367137289128057');
-- select * from loan where loanIDX = '00324367137289128057';
-- select * from loan where loanIDX = '00324367137289128057';
-- select * from cus_and_loan where loan_loanIDX = '00324367137289128057';
-- select * from staff;
-- select * from customer;
-- select * from depositAccount;
-- call proc_new_depAccount('221403198202262547','221403198002143682','10061565741784896116','RMB',1.00,0.00);
-- call proc_alter_depAccount('10061565741784896116','221403198002143682',-20.0);
-- call proc_delete_depAccount('10061565741784896116');

-- call proc_new_cheAccount('221403198202262547','221403198002143682','10061565741784896116',0.00);
-- call proc_alter_cheAccount('10061565741784896116','221403198002143682',-20.0);
call proc_delete_cheAccount('10061565741784896116');
select * from chequeAccount where cusA_accountIDX='10061565741784896116';
select * from cusAccount where accountIDX='10061565741784896116';
select * from cus_and_cheAccount where cheq_cusA_accountIDX='10061565741784896116';
-- call proc_delete_depAccount('00061565741784896119');
-- select * from depositAccount where cusA_accountIDX='00061565741784896119';


