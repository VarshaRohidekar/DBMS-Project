import csv 

with open("Old_Student.csv", mode='r') as file, open("Student.csv", mode="w") as valid:
    csvfile = csv.reader(file)
    writing = csv.writer(valid, delimiter=',')
    # i = 1
    for (srn, fname, lname, sem, pswd, cgpa, year, email) in csvfile:
        # print('looping')
        srn = srn[:-1]
        # print(srn)
        # print(len(srn))
        n = len(srn)
        if n != 13:
            continue 
        
        if len(fname) > 15 or len(lname) > 15:
            continue 
        
        if int(sem) not in (1, 2, 3, 4, 5, 6, 7, 8):
            continue
    
        if float(cgpa) <=6 or float(cgpa) > 10:
            continue 
        
        if int(year)+3 not in (2024, 2025, 2026):
            
            continue 
            
        # print(str(i) + '\t' + srn)
        writing.writerow([srn, fname, lname, sem, pswd, cgpa, int(year) + 3, email])
        # i+=1
