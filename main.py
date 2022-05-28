import assets.cell as cell
import assets.grid as grid
from assets.log import log
import time

def main():
    #Create grid
    a=True
    gr = grid.Grid(10, 20)
    gr.set_cell_type(5, 0, cell.Types.water)
    gr.set_cell_type(0, 0, cell.Types.sand)
    gr.set_cell_type(1, 5, cell.Types.wall)
    gr.set_cell_type(2, 5, cell.Types.wall)
    gr.set_cell_type(3, 5, cell.Types.wall)
    gr.set_cell_type(4, 5, cell.Types.wall)
    gr.set_cell_type(5, 5, cell.Types.wall)
    
    gr.set_cell_type(14, 5, cell.Types.wall)
    gr.set_cell_type(15, 5, cell.Types.wall)
    gr.set_cell_type(16, 5, cell.Types.wall)
    gr.set_cell_type(17, 5, cell.Types.wall)






    while 1:
        gr.set_cell_type(5, 0, cell.Types.water)
        gr.set_cell_type(15,9,cell.Types.smoke)
        print("__"*(gr.width+1))
        gr.print_grid(border="|")
        print("--"*(gr.width+1))
        gr.update_physics()
        time.sleep(0.25)

if __name__ == "__main__":
    main()