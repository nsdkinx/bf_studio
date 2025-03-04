import flet
from bf_studio.memory_cell import MemoryCell
from bf_studio.memory_cell_state import MemoryCellState


class MemoryContainer(flet.Row):
    def __init__(self):
        super().__init__()
        self.tight = True
        self.cell_pointer = 0
        self.controls = [MemoryCell()]

    async def next(self):
        await self.controls[self.cell_pointer].set_state(MemoryCellState.STALE)
        self.cell_pointer += 1

        if self.cell_pointer == len(self.controls):
            self.controls.append(MemoryCell())

        cell: MemoryCell = self.controls[self.cell_pointer]

        self.update()
        await cell.set_state(MemoryCellState.SELECTED)
        return cell

    async def back(self):
        if self.cell_pointer <= 0:
            return

        await self.controls[self.cell_pointer].set_state(MemoryCellState.STALE)

        self.cell_pointer -= 1

        try:
            cell: MemoryCell = self.controls[self.cell_pointer]
        except IndexError:
            self.controls.append(MemoryCell())
            cell: MemoryCell = self.controls[self.cell_pointer]

        self.update()
        await cell.set_state(MemoryCellState.SELECTED)
        return cell

    async def reset(self):
        self.cell_pointer = 0
        self.controls = [MemoryCell()]
        self.update()

    @property
    def selected_cell(self):
        return self.controls[self.cell_pointer]
