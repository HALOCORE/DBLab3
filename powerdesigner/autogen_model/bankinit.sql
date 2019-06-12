/*==============================================================*/
/* DBMS name:      MySQL 5.0                                    */
/* Created on:     2019/6/12 11:03:39                           */
/*==============================================================*/


drop table if exists branch;

drop table if exists chequeAccount;

drop table if exists cusAccount;

drop table if exists cus_and_cheAccount;

drop table if exists cus_and_depAccount;

drop table if exists cus_and_loan;

drop table if exists customer;

drop table if exists depositAccount;

drop table if exists loan;

drop table if exists loanPay;

drop table if exists staff;

/*==============================================================*/
/* Table: branch                                                */
/*==============================================================*/
create table branch
(
   city                 varchar(20),
   branchName           varchar(20) not null,
   primary key (branchName)
);

/*==============================================================*/
/* Table: chequeAccount                                         */
/*==============================================================*/
create table chequeAccount
(
   cusA_accountIDX      varchar(30) not null,
   neg_limit            float(8,2),
   primary key (cusA_accountIDX)
);

/*==============================================================*/
/* Table: cusAccount                                            */
/*==============================================================*/
create table cusAccount
(
   accountIDX           varchar(30) not null,
   bran_branchName      varchar(20) not null,
   staf_staffID         varchar(20) not null,
   remain               float(8,2),
   visitTime            datetime,
   openTime             datetime,
   primary key (accountIDX)
);

/*==============================================================*/
/* Table: cus_and_cheAccount                                    */
/*==============================================================*/
create table cus_and_cheAccount
(
   cust_customID        varchar(18) not null,
   cheq_cusA_accountIDX varchar(30) not null,
   primary key (cust_customID, cheq_cusA_accountIDX)
);

/*==============================================================*/
/* Table: cus_and_depAccount                                    */
/*==============================================================*/
create table cus_and_depAccount
(
   cust_customID        varchar(18) not null,
   depo_cusA_accountIDX varchar(30) not null,
   primary key (cust_customID, depo_cusA_accountIDX)
);

/*==============================================================*/
/* Table: cus_and_loan                                          */
/*==============================================================*/
create table cus_and_loan
(
   cust_customID        varchar(18) not null,
   loan_loanIDX         varchar(30) not null,
   primary key (cust_customID, loan_loanIDX)
);

/*==============================================================*/
/* Table: customer                                              */
/*==============================================================*/
create table customer
(
   customID             varchar(18) not null,
   customPhone          varchar(16),
   customAddress        varchar(30),
   customName           varchar(20) not null,
   relName              varchar(10),
   relPhone             varchar(16),
   relEmail             varchar(30),
   relRelation          varchar(10),
   primary key (customID)
);

/*==============================================================*/
/* Table: depositAccount                                        */
/*==============================================================*/
create table depositAccount
(
   cusA_accountIDX      varchar(30) not null,
   currency             varchar(5),
   interest             decimal(6,3),
   primary key (cusA_accountIDX)
);

/*==============================================================*/
/* Table: loan                                                  */
/*==============================================================*/
create table loan
(
   loanIDX              varchar(30) not null,
   staf_staffID         varchar(20) not null,
   bran_branchName      varchar(20) not null,
   loanDate             datetime,
   loanAmount           float(8,2),
   primary key (loanIDX)
);

/*==============================================================*/
/* Table: loanPay                                               */
/*==============================================================*/
create table loanPay
(
   loan_loanIDX         varchar(30) not null,
   loanPayDate          datetime not null,
   loanPayAmount        float(8,2),
   primary key (loan_loanIDX, loanPayDate)
);

/*==============================================================*/
/* Table: staff                                                 */
/*==============================================================*/
create table staff
(
   staffID              varchar(20) not null,
   bran_branchName      varchar(20) not null,
   startWorkDate        date,
   staffName            varchar(12),
   staffPhone           varchar(16),
   staffAddress         varchar(30),
   primary key (staffID)
);

alter table chequeAccount add constraint FK_account_subtype2 foreign key (cusA_accountIDX)
      references cusAccount (accountIDX) on delete restrict on update restrict;

alter table cusAccount add constraint FK_account_responsible foreign key (staf_staffID)
      references staff (staffID) on delete restrict on update restrict;

alter table cusAccount add constraint FK_bank_and_openAccount foreign key (bran_branchName)
      references branch (branchName) on delete restrict on update restrict;

alter table cus_and_cheAccount add constraint FK_cus_and_cheAccount foreign key (cust_customID)
      references customer (customID) on delete restrict on update restrict;

alter table cus_and_cheAccount add constraint FK_cus_and_cheAccount2 foreign key (cheq_cusA_accountIDX)
      references chequeAccount (cusA_accountIDX) on delete restrict on update restrict;

alter table cus_and_depAccount add constraint FK_cus_and_depAccount foreign key (cust_customID)
      references customer (customID) on delete restrict on update restrict;

alter table cus_and_depAccount add constraint FK_cus_and_depAccount2 foreign key (depo_cusA_accountIDX)
      references depositAccount (cusA_accountIDX) on delete restrict on update restrict;

alter table cus_and_loan add constraint FK_cus_and_loan foreign key (cust_customID)
      references customer (customID) on delete restrict on update restrict;

alter table cus_and_loan add constraint FK_cus_and_loan2 foreign key (loan_loanIDX)
      references loan (loanIDX) on delete restrict on update restrict;

alter table depositAccount add constraint FK_account_subtype foreign key (cusA_accountIDX)
      references cusAccount (accountIDX) on delete restrict on update restrict;

alter table loan add constraint FK_bank_and_loan foreign key (bran_branchName)
      references branch (branchName) on delete restrict on update restrict;

alter table loan add constraint FK_loan_responsible foreign key (staf_staffID)
      references staff (staffID) on delete restrict on update restrict;

alter table loanPay add constraint FK_loan_and_loanPay foreign key (loan_loanIDX)
      references loan (loanIDX) on delete restrict on update restrict;

alter table staff add constraint FK_branch_and_staff foreign key (bran_branchName)
      references branch (branchName) on delete restrict on update restrict;

commit;

