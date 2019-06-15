use BankDB;

-------------------------------------------------------------- 后端不调用。初始化用。
delimiter $$
DROP PROCEDURE if exists `proc_check_loan`;
CREATE PROCEDURE `proc_check_loan` ()
BEGIN
	DECLARE done BOOLEAN DEFAULT 0 ;

	DECLARE var_idx varchar(30) DEFAULT null;
	DECLARE var_amount float(8,2) DEFAULT null;
	DECLARE var_status tinyint DEFAULT null;
	DECLARE var_paid float(8,2) DEFAULT null;

	DECLARE var_newstatus tinyint DEFAULT null;
	DECLARE var_paycount int DEFAULT null;
	DECLARE var_payreal float(8,2) DEFAULT null;

	DECLARE cur cursor for (select loanIDX, loanAmount, loanStatus, loanPaid from loan);
	DECLARE CONTINUE HANDLER FOR SQLSTATE '02000' SET done = 1;
	OPEN cur ;
	  -- 使用repeat循环语法
		REPEAT
			-- 批读取数据到指定变量上
			FETCH cur INTO var_idx, var_amount, var_status, var_paid ;
			-- 进行逻辑操作
			select count(*), sum(loanPayAmount) into var_paycount, var_payreal from loanPay where var_idx = loan_loanIDX;
			if var_paycount = 0 then 
				set var_newstatus = 1;
			elseif var_payreal < var_amount then 
				set var_newstatus = 2;
			elseif var_payreal = var_amount then
				set var_newstatus = 3;
			else
				set var_newstatus = 11;
			end if;
			update loan set loanStatus=var_newstatus where loanIDX = var_idx;
			update loan set loanPaid=var_payreal where loanIDX = var_idx;
	  -- 循环结束条件
	  UNTIL done 
	  END REPEAT ;
	CLOSE cur ;
END $$

-- ------------------------------------------------------------------------------------------
use BankDB;
delimiter $$
DROP PROCEDURE if exists `proc_pay_loan`;
CREATE PROCEDURE `proc_pay_loan` (
	in var_loan_loanIDX  		varchar(30),
    in var_loanPayDate          datetime,
    in var_loanPayAmount        float(8,2))
BEGIN
	DECLARE var_after_paid float(8,2) DEFAULT null;
	DECLARE var_amount float(8,2) DEFAULT null;
	DECLARE var_status tinyint DEFAULT 0;
	select loanPaid, loanAmount into var_after_paid, var_amount from loan where loanIDX = var_loan_loanIDX;
	set var_after_paid = var_after_paid + var_loanPayAmount;
	if var_after_paid > var_amount then
		SIGNAL SQLSTATE '45000'
		  SET MESSAGE_TEXT = 'Error: more money paid then loanAmount.', MYSQL_ERRNO = 1001; -- not sure
	end if;
	if var_after_paid = var_amount then
		set var_status = 3;
	else
		set var_status = 2;
	end if;
	insert into loanPay(loan_loanIDX, loanPayDate, loanPayAmount) values
		(var_loan_loanIDX, var_loanPayDate, var_loanPayAmount);
	update loan set loanStatus = var_status, loanPaid = var_after_paid where loanIDX = var_loan_loanIDX;
END $$
