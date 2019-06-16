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

-- ------------------------------------------------------------------------------------------贷款支付
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

----------------------------------------------------------------------------------------------贷款删除
/*需要检查：是否本人操作，贷款是否发放(其实贷款记录只需要查一次就行，因为外键约束，有子必有父)
删除顺序：客户与贷款 贷款支付 贷款*/
use BankDB;
delimiter $$
DROP PROCEDURE if exists `proc_delete_loan`;
CREATE PROCEDURE `proc_delete_loan` (
	in var_loan_loanIDX      varchar(30))
	-- in var_customID          varchar(18))
BEGIN
	DECLARE loan_record varchar(30) DEFAULT null;
	DECLARE chaeck_loanStatus varchar(30) DEFAULT null;
	DECLARE loanPay_record varchar(30) DEFAULT null;
	DECLARE check_customID varchar(30) DEFAULT null;
	-- DECLARE check_remain

	select loanIDX, loanStatus into loan_record, chaeck_loanStatus from loan where loanIDX = var_loan_loanIDX LIMIT 1;
	select loan_loanIDX into loanPay_record from loanPay where loan_loanIDX = var_loan_loanIDX LIMIT 1;
	-- select cust_customID into check_customID from cus_and_loan where loan_loanIDX = var_loan_loanIDX;

	if loan_record is null then
	 	SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: no this record in table loan.', MYSQL_ERRNO = 1001; -- not sure
	end if;
	if loanPay_record is null then
	 	SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: no this record in table loanPay.', MYSQL_ERRNO = 1001; -- not sure
	end if;
	-- if check_customID is null then
	--  	SIGNAL SQLSTATE '45000'
	-- 	SET MESSAGE_TEXT = 'Error: no this record in table cus_and_loan.', MYSQL_ERRNO = 1001; -- not sure
	-- end if;
	-- if check_customID != var_customID then
	--  	SIGNAL SQLSTATE '45000'
	-- 	SET MESSAGE_TEXT = 'Error: this is not your loan.', MYSQL_ERRNO = 1001; -- not sure
	-- end if;
	if chaeck_loanStatus = 1 or chaeck_loanStatus = 2 then
		SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: the loan has not been paid.', MYSQL_ERRNO = 1001; -- not sure
	end if;

	delete from cus_and_loan where loan_loanIDX = var_loan_loanIDX;
	delete from loanPay where loan_loanIDX = var_loan_loanIDX;
	delete from loan where loanIDX = var_loan_loanIDX;

END $$

