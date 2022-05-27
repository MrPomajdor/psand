import assets.cell as cell
import assets.grid as grid
from assets.log import log
import time

def main():
    #Create grid
    a=True
    gr = grid.Grid(10, 10)
    gr.set_cell_type(5, 0, cell.Types.water)
    gr.set_cell_type(2, 4, cell.Types.sand)

    while 1:
        print("----------------------------------------")
        if a:
            gr.set_cell_type(2, 0, cell.Types.water)
            #a = not a
        else:
            gr.set_cell_type(4, 0, cell.Types.water)
            #a = not a
        gr.print_grid()
        gr.update_physics()
        time.sleep(0.5)
if __name__ == "__main__":
    main()