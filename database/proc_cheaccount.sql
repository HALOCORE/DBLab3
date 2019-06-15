use BankDB;



----------------------------------------------------------------------------------------------支票账户删除
use BankDB;
delimiter $$
DROP PROCEDURE if exists `proc_delete_cheAccount`;
CREATE PROCEDURE `proc_delete_cheAccount` (
	in var_cusA_accountIDX varchar(30),
BEGIN
	DECLARE cusAccount_record varchar(30) DEFAULT null;
    DECLARE account_remain float(8,2) DEFAULT null;
	DECLARE cheAccount_record varchar(30) DEFAULT null;
	DECLARE cus_and_cheAccount_record varchar(30) DEFAULT null;

	select accountIDX,remain into cusAccount_record, account_remain from cusAccount where accountIDX = var_cusA_accountIDX
	select cusA_accountIDX into cheAccount_record from chequeAccount where cusA_accountIDX = var_cusA_accountIDX
	select cheq_cusA_accountIDX into cus_and_cheAccount_record from cus_and_cheAccount where cheq_cusA_accountIDX = var_cusA_accountIDX

	if cusAccount_record is null then
	 	SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: no this record in table cusAccount.', MYSQL_ERRNO = 1001; -- not sure
	end if;
    if account_remain < 0.0 then
        SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: you have not paid the money back yet in this chequeAccount.', MYSQL_ERRNO = 1001; -- not sure
    end if;
    if account_remain > 0.0 then
        SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Warning: you have some money remain in this chequeAccount.', MYSQL_ERRNO = 1001; -- not sure
    end if;
	if cheAccount_record is null then
	 	SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: no this record in table chequeAccount.', MYSQL_ERRNO = 1001; -- not sure
	end if;
	if cus_and_cheAccount_record is null then
	 	SIGNAL SQLSTATE '45000'
		SET MESSAGE_TEXT = 'Error: no this record in table cus_and_cheAccount.', MYSQL_ERRNO = 1001; -- not sure
	end if;

	delete from cus_and_cheAccount where cheq_cusA_accountIDX = var_cusA_accountIDX
	delete from chequeAccount where cusA_accountIDX = var_cusA_accountIDX
	delete from cusAccount where accountIDX = var_cusA_accountIDX

END $$