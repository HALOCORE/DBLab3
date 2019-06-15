-- select count(*), sum(loanPayAmount) from loanPay group by loan_loanIDX;
-- call proc_check_loan();

-- call proc_pay_loan('58740452588532331214', '2019-06-13 8:21:00', 3200);

-- select * from loan where loanIDX = '58740452588532331214';
-- select * from loanPay where loan_loanIDX = '58740452588532331214';

select * from loan where loanIDX = '16397893085173404939';
select * from loanPay where loan_loanIDX = '16397893085173404939';
call proc_pay_loan("16397893085173404939", "2019-06-15 17:03:28", 100.0);