print("-------ATM CASH DISPENSER------")
total_100=total_50=total_20=total_10=total_5=total_1=0
cust_serv=0
total_disp=0
serv=True
while serv:
    name=input("Enter customer name: ")
    amount=int(input(f"Hello {name} enter withdrawl amount:"))
    if amount<=0:
        print("Invalid amount please try again")
        continue
    print(f"Dispensing {amount} unit for {name}")
    remaining=amount
    idx=1
    while idx<=6:
        if idx==1:
            value=100
        elif idx==2:
            value=50
        elif idx==3:
            value=20
        elif idx==4:
            value=10
        elif idx==5:
            value=5
        else:
            value=1
        count=remaining // value 
        if count>0:
            print(f"{count} x {value} unit notes={count*value}")
            remaining-=count*value
            if value==100:
                total_100+=count
            elif value==50:
                total_50+=count
            elif value==20:
                total_20+=count
            elif value==10:
                total_10+=count
            elif value==5:
                total_5+=count
            else:
                total_1+=count
        idx+=1
    cust_serv+=1
    total_disp+=amount
    print(f"Transaction complete {name}")
    again=input("Next customer (yes/no)")
    if again!="yes":
        serv=False
