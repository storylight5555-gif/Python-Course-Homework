Student_info={
"id1":{"Name": "Sara", "Class": "V", "Subject": "English, Maths"},
"id2":{"Name": "Sam", "Class": "V", "Subject": "English, Maths"},
"id3":{"Name": "Surya", "Class": "V", "Subject": "English, Maths"},
"id4":{"Name": "Surya", "Class": "V", "Subject": "English, Maths"}
}
result={}
Seen_Keys=[]
for s_id ,detials in Student_info.items():
    unike_key=(detials["Name"], detials["Class"], detials["Subject"])
    if unike_key not in Seen_Keys:
        Seen_Keys.append(unike_key)
        result[s_id]=detials
for k, v in result.items():
    print(k , ":" , v)