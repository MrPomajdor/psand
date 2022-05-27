import assets.cell as cell
import assets.grid as grid
from assets.log import log
import time

def main():
    #Create grid
    log("\n\n---------------Creating grid---------------\n")
    gr = grid.Grid(10, 10)
    gr.set_cell_type(2, 0, cell.Types.sand)
    gr.set_cell_type(2, 3, cell.Types.sand)

    while 1:
        print("----------------------------------------")
        gr.print_grid()
        gr.update_physics()
        time.sleep(0.5)
if __name__ == "__main__":
    main()