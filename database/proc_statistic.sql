select bran_branchName,SUM(loanAmount) AS sum_loanAmount
  from loan
 where gen_where()
 Group by bran_branchName

select bran_branchName,COUNT(*) AS count_loan
  from loan
 where gen_where()
 Group by bran_branchName