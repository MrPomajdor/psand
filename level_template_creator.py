with open(input("Enter file name: "), "w") as f:
    x = int(input("Enter width: "))
    y = int(input("Enter height: "))
    for ya in range(y):
        for xa in range(x):
            f.write("O")

        f.write("\n")
    f.close()
    print("Done")

