def total_cal(billamount, tippercent):
    tipamount = billamount * tippercent / 100
    totalamount = billamount + tipamount
    print("Please pay ",round(totalamount, 2))
total_cal(100,50)
