class log:
    def __init__(self,message):
        with open("log.txt", "a") as myfile:
            myfile.write(message+"\n")

        