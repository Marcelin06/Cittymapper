f = open("network_combined.csv", 'r')
next(f)
print("\n")
for line in f :
    items = line.rstrip("\n").split(";")
	
    num_attributes = len(items)
    i = 0 
    insert_line = "INSERT INTO nodes VALUES ( "
	
    while i < num_attributes :
        item = items[i].replace("'", "''")
        if i == 5 :
            lst = item.split(',')[0]
            lst1 = lst.split(':')[0]
            item = lst1            
        insert_line = insert_line + "'" + item + "'"

        if i != num_attributes - 1 :
            insert_line = insert_line + ", "
        i = i + 1
    insert_line = insert_line + ");"
    print(insert_line)
			