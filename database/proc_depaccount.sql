use BankDB;



----------------------------------------------------------------------------------------------储蓄账户删除
use BankDB;
delimiter $$
DROP PROCEDURE if exists `proc_delete_depAccount`;
CREATE PROCEDURE `proc_delete_depAccount` (
	in var_cusA_accountIDX varchar(30),
BEGIN
	DECLARE cusAccount_record varchar(30) DEFAULT null;
    DECLARE account_remain float(8,2) DEFAULT null;
	DECLARE depAccount_record varchar(30) DEFAULT null;
	DECLARE cus_and_depAccount_record varchar(30) DEFAULT null;

	select accountIDX, remain into cusAccount_record, account_remain from cusAccount where accountIDX = var_cusA_accountIDX
	select * into depAccount_record from depositAccount where cusA_accountIDX = var_cusA_accountIDX
	select * into cus_and_depAccount_record from cus_and_depAccount where depo_cusA_accountIDX = var_cusA_accountIDX

	if cusAccount_record is null then
	 	SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: no this record in table cusAccount.', MYSQL_ERRNO = 1001; -- not sure
	end if;
    if account_remain > 0.0 then
        SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Warning: you have some money remain in this depositAccount.', MYSQL_ERRNO = 1001; -- not sure
    end if;
	if depAccount_record is null then
	 	SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: no this record in table depositAccount.', MYSQL_ERRNO = 1001; -- not sure
	end if;
	if cus_and_depAccount_record is null then
	 	SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: no this record in table cus_and_depAccount.', MYSQL_ERRNO = 1001; -- not sure
	end if;

	delete from cus_and_depAccount where depo_cusA_accountIDX = var_cusA_accountIDX
	delete from depositAccount where cusA_accountIDX = var_cusA_accountIDX
	delete from cusAccount where accountIDX = var_cusA_accountIDX

END $$