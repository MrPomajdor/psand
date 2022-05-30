import assets.cell as cell
import assets.grid as grid
from assets.log import log
import time
def main():
    #Create grid
    a=True
    gr = grid.Grid(20, 20)
    gr.load("./grid.txt")



    

    while 1:
        print("__"*(gr.width+1))
        gr.print_grid(border="|")
        print("--"*(gr.width+1))
        gr.update_physics()
        time.sleep(0.1)

if __name__ == "__main__":
    main()