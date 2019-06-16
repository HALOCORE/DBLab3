use BankDB;
-------------储蓄账户发放利润---------------------------------------------------------------------------------------


-------------储蓄账户新增-------------------------------------------------------------------------------------------
/*
1，判断客户身份证和员工ID都在，
2，账户所在银行名字其实就是员工所在银行(非空)，
3，插入顺序：账户，储蓄账户，客户与储蓄账户
*/
use BankDB;
delimiter $$
DROP PROCEDURE if exists `proc_new_depAccount`;
CREATE PROCEDURE `proc_new_depAccount` (
    --检查所需信息
	in var_staffID          varchar(20),
    in var_customID         varchar(18),
    --新建所需信息
    in var_accountIDX       varchar(30),
    in var_currency         float(8,2),
    in var_interest         decimal(6,3),
    in var_remain           float(8,2))
    --储蓄账户利率需要更新吗，比如可以根据余额或者账户持续时间控制
    --初始利率由后端根据货币种类设置吧
BEGIN
    DECLARE staff_bran_branchName varchar(20) DEFAULT null;
    DECLARE customID_record varchar(18) DEFAULT null;

    select bran_branchName into staff_bran_branchName from staff where staffID = var_staffID
    select customID into customID_record from customer where customID = var_customID
    if staff_bran_branchName is null then
        SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: no this people in table staff.', MYSQL_ERRNO = 1001; -- not sure
    end if;
    if customID_record is null then 
        SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: you have not registered in our branch.', MYSQL_ERRNO = 1001; -- not sure
    end if;
    insert into cusAccount (accountIDX,bran_branchName,staf_staffID,remain,openTime,accountType)
    values (var_accountIDX,staff_bran_branchName,var_staffID,var_remain,sysdate(),"depositAccount");
    insert into depositAccount (cusA_accountIDX,currency,interest)
    values (var_accountIDX,var_currency,var_interest);
    insert into cus_and_depAccount (cust_customID,depo_cusA_accountIDX)
    values (var_customID,var_accountIDX);
END $$

---------------储蓄账户更改----------------------------------------------
/*
1，检查：账户是否存在，是否本人操作，钱是否超出余额
2，更改顺序：余额，访问时间
*/
use BankDB;
delimiter $$
DROP PROCEDURE if exists `proc_alter_depAccount`;
CREATE PROCEDURE `proc_alter_depAccount` (
	in var_accountIDX varchar(30),
    in var_customID varchar(18),
    in var_alter_money float(8,2))
BEGIN
    DECLARE depAccount_record varchar(30) DEFAULT null;
    DECLARE check_identity varchar(18) DEFAULT null;
    DECLARE account_remain float(8,2) DEFAULT null;
    DECLARE acc_opentime datetime DEFAULT null;
    
    select cust_customID into check_identity from cus_and_depAccount where cheq_cusA_accountIDX = var_accountIDX
    select remain, openTime into account_remain, acc_opentime from cusAccount where accountIDX = var_accountIDX
    select cusA_accountIDX into depAccount_record from depositAccount where cusA_accountIDX = var_customID

    if depAccount_record is null then
	 	SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: no this record in table depositAccount.', MYSQL_ERRNO = 1001; -- not sure
	end if;
    if check_identity is null then
	 	SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: you have not registered in our branch.', MYSQL_ERRNO = 1001; -- not sure
	end if;
    if check_identity != var_customID then
	 	SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: this is not your depositAccount.', MYSQL_ERRNO = 1001; -- not sure
	end if;
    if account_remain+var_alter_money < 0 then
        SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: Lack of balance.', MYSQL_ERRNO = 1001; -- not sure
    end if
    update cusAccount set remain=account_remain+var_alter_money, visitTime=sysdate() where accountIDX = var_accountIDX

END $$


------------------储蓄账户删除----------------------------------------------------------------------------
/*检查：是否有此账户，是否本人操作，余额剩否
删除循序：客户与账户，支票账户，账户*/
use BankDB;
delimiter $$
DROP PROCEDURE if exists `proc_delete_depAccount`;
CREATE PROCEDURE `proc_delete_depAccount` (
	in var_accountIDX varchar(30),
    in var_customID varchar(18))
BEGIN
	DECLARE cusAccount_record varchar(30) DEFAULT null;
    DECLARE account_remain float(8,2) DEFAULT null;
	DECLARE depAccount_record varchar(30) DEFAULT null;
	DECLARE check_identity varchar(30) DEFAULT null;

	select accountIDX, remain into cusAccount_record, account_remain from cusAccount where accountIDX = var_accountIDX
	select * into depAccount_record from depositAccount where cusA_accountIDX = var_accountIDX
	select * into check_identity from cus_and_depAccount where depo_cusA_accountIDX = var_accountIDX

	if cusAccount_record is null then
	 	SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: no this record in table cusAccount.', MYSQL_ERRNO = 1001; -- not sure
	end if;
	if depAccount_record is null then
	 	SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: no this record in table depositAccount.', MYSQL_ERRNO = 1001; -- not sure
	end if;
	if check_identity is null then
	 	SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: you have not registered in our branch.', MYSQL_ERRNO = 1001; -- not sure
	end if;
    if check_identity != var_customID then
	 	SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: this is not your depositAccount.', MYSQL_ERRNO = 1001; -- not sure
	end if;
    if account_remain > 0.0 then
        SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Warning: you have some money remain in this depositAccount.', MYSQL_ERRNO = 1001; -- not sure
    end if;

	delete from cus_and_depAccount where depo_cusA_accountIDX = var_accountIDX
	delete from depositAccount where cusA_accountIDX = var_accountIDX
	delete from cusAccount where accountIDX = var_accountIDX

END $$