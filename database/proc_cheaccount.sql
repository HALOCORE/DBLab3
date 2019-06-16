use BankDB;
-- ----------支票账户新增-------------------------------------------------------------------------------------------
/*
1，判断客户身份证和员工ID都在，
2，账户所在银行名字其实就是员工所在银行(非空)，
3，插入顺序：账户，支票账户，客户与支票账户
*/
use BankDB;
delimiter $$
DROP PROCEDURE if exists `proc_new_cheAccount`;
CREATE PROCEDURE `proc_new_cheAccount` (
    --检查所需信息
	in var_staffID          varchar(20),
    in var_customID         varchar(18),
    --新建所需信息
    in var_accountIDX       varchar(30),
    in var_remain           float(8,2))
    --支票账户透支额度在存储过程中设置：初始2000，开户时间每增一年，额度+2000
BEGIN
    DECLARE staff_bran_branchName varchar(20) DEFAULT null;
    DECLARE customID_record varchar(18) DEFAULT null;

    select bran_branchName into staff_bran_branchName from staff where staffID = var_staffID;
    select customID into customID_record from customer where customID = var_customID;
    if staff_bran_branchName is null then
        SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: no this people in table staff.', MYSQL_ERRNO = 1001; -- not sure
    end if;
    if customID_record is null then 
        SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: you have not registered in our branch.', MYSQL_ERRNO = 1001; -- not sure
    end if;
    insert into cusAccount (accountIDX,bran_branchName,staf_staffID,remain,openTime,accountType)
    values (var_accountIDX,staff_bran_branchName,var_staffID,var_remain,sysdate(),"cheque");
    insert into chequeAccount (cusA_accountIDX,neg_limit)
    values (var_accountIDX,2000.00);
    insert into cus_and_cheAccount (cust_customID,cheq_cusA_accountIDX)
    values (var_customID,var_accountIDX);
END $$

---------------支票账户更改----------------------------------------------
/*
1，检查：账户是否存在，是否本人操作(这个检查其实包含了记录检查，因为外键约束)，钱是否超出额度
2，更改顺序：余额，访问时间，额度
*/
use BankDB;
delimiter $$
DROP PROCEDURE if exists `proc_alter_cheAccount`;
CREATE PROCEDURE `proc_alter_cheAccount` (
	in var_accountIDX varchar(30),
    in var_customID varchar(18),
    in var_alter_money float(8,2))
BEGIN
    DECLARE cheAccount_record varchar(30) DEFAULT null;
    DECLARE check_neg_limit float(8,2) DEFAULT null;
    DECLARE check_identity varchar(18) DEFAULT null;
    DECLARE account_remain float(8,2) DEFAULT null;
    DECLARE acc_opentime datetime DEFAULT null;
    DECLARE acc_nowtime datetime DEFAULT null;
    DECLARE account_duration int DEFAULT null;
    
    select cust_customID into check_identity from cus_and_cheAccount where cheq_cusA_accountIDX = var_accountIDX;
    select remain, openTime into account_remain, acc_opentime from cusAccount where accountIDX = var_accountIDX;
    select cusA_accountIDX, neg_limit into cheAccount_record, check_neg_limit 
     from chequeAccount where cusA_accountIDX = var_accountIDX;

    if cheAccount_record is null then
	 	SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: no this record in table chequeAccount.', MYSQL_ERRNO = 1001; -- not sure
	end if;
    if check_identity is null then
	 	SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: you have not registered in our branch.', MYSQL_ERRNO = 1001; -- not sure
	end if;
    if check_identity != var_customID then
	 	SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: this is not your chequeAccount.', MYSQL_ERRNO = 1001; -- not sure
	end if;
    --先看额度是否可增加，再判断是否超出额度
    set acc_nowtime = sysdate();
    set account_duration = TIMESTAMPDIFF(YEAR,acc_opentime,acc_nowtime);
    set check_neg_limit = (account_duration+1)*2000.0
    if account_remain+var_alter_money < (-check_neg_limit) then
        SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: Beyond the limit.', MYSQL_ERRNO = 1001; -- not sure
    end if

    update cusAccount set remain=account_remain+var_alter_money, visitTime=acc_nowtime where accountIDX = var_accountIDX;
    update chequeAccount set neg_limit=check_neg_limit where cusA_accountIDX = var_accountIDX;

END $$

---------------支票账户删除-------------------------------------------------------------------------------
/*检查：是否有此账户，是否本人操作，余额剩否
删除循序：客户与账户，支票账户，账户*/
use BankDB;
delimiter $$
DROP PROCEDURE if exists `proc_delete_cheAccount`;
CREATE PROCEDURE `proc_delete_cheAccount` (
	in var_accountIDX varchar(30),
    in var_customID varchar(18))
BEGIN
	DECLARE cusAccount_record varchar(30) DEFAULT null;
    DECLARE account_remain float(8,2) DEFAULT null;
	DECLARE cheAccount_record varchar(30) DEFAULT null;
    DECLARE check_identity varchar(18) DEFAULT null;

	select accountIDX,remain into cusAccount_record, account_remain from cusAccount where accountIDX = var_accountIDX;
	select cusA_accountIDX into cheAccount_record from chequeAccount where cusA_accountIDX = var_accountIDX;
	select cust_customID into check_identity from cus_and_cheAccount where cheq_cusA_accountIDX = var_accountIDX;

	if cusAccount_record is null then
	 	SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: no this record in table cusAccount.', MYSQL_ERRNO = 1001; -- not sure
	end if;
    if cheAccount_record is null then
	 	SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: no this record in table chequeAccount.', MYSQL_ERRNO = 1001; -- not sure
	end if;
    if check_identity is null then
	 	SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: you have not registered in our branch.', MYSQL_ERRNO = 1001; -- not sure
	end if;
    if check_identity != var_customID then
	 	SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: this is not your chequeAccount.', MYSQL_ERRNO = 1001; -- not sure
	end if;
    if account_remain < 0.0 then
        SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: you have not paid the money back yet in this chequeAccount.', MYSQL_ERRNO = 1001; -- not sure
    end if;
    if account_remain > 0.0 then
        SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Warning: you have some money remain in this chequeAccount.', MYSQL_ERRNO = 1001; -- not sure
    end if;
	
	delete from cus_and_cheAccount where cheq_cusA_accountIDX = var_accountIDX;
	delete from chequeAccount where cusA_accountIDX = var_accountIDX;
	delete from cusAccount where accountIDX = var_accountIDX;

END $$