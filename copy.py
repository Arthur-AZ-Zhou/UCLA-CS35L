#python copy.py

with open("/home/arthur/CS35L/Assignment4/who-contributed.txt", "r") as rf:
    print("Success")
    with open("/mnt/c/Users/arthu/OneDrive/Desktop/Code/CS35L/Assignment4/who-contributed.txt", "w") as wf:
        for line in rf:
            wf.write(line)
