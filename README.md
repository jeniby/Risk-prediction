# Risk-prediction
Flask server of risk prediction

Usage
===============
````
$ curl -X GET -H "Content-type: application/json" 
--data '{
"mths_since_last_delinq": [null, 4.0, 65.0],
"dti": [12.34, 16.51, 9.03],
"revol_bal": [15962.0, 8627.0, 16349.0],
"inq_last_6mths": [0.0, 1.0, 1.0],
"tot_cur_bal": [91246.0, 35596.0, 622555.0],
"open_acc": [14.0, 12.0, 28.0],
"grade": ["B", "B", "A"],
"tot_coll_amt": [0.0, 0.0, 0.0], 
"sub_grade": ["B2", "B1", "A1"], 
"int_rate": [10.15, 9.67, 6.03], 
"total_acc": [34.0, 22.0, 50.0], 
"earliest_cr_line": ["Jan-1998", "Apr-1998", "Apr-1999"],
"total_rev_hi_lim": [36100.0, 40700.0, 28600.0],
"acc_now_delinq": [0.0, 0.0, 0.0], 
"delinq_2yrs": [0.0, 2.0, 0.0],
"issue_d": ["May-2014", "Jan-2014", "Jul-2014"]}' 
"http://127.0.0.1:5000/api/ml/get_risk"

{"data":[0.7254568227559557,0.7195684912154054,0.7705007690852506]}
````
