import flet
from bf_studio.memory_cell_state import MemoryCellState
from flet.core.types import FontWeight


class MemoryCell(flet.Container):
    def __init__(self):
        super().__init__()
        self.state = MemoryCellState.NEVER_USED
        self.cell_value = 0
        self.alignment = flet.alignment.center
        self.width = 50
        self.height = 50
        self.bgcolor = flet.Colors.GREY_800
        self.border_radius = 10
        self.content = flet.Text(str(self.cell_value), size=20, weight=FontWeight.BOLD)

    async def set_state(self, state: MemoryCellState):
        if state == MemoryCellState.NEVER_USED:
            self.bgcolor = flet.Colors.GREY_800
            self.cell_value = 0
            self.content = flet.Text(str(self.cell_value), size=20, weight=FontWeight.BOLD)

        elif state == MemoryCellState.STALE:
            self.bgcolor = flet.Colors.BLUE_ACCENT
            self.border = None

        elif state == MemoryCellState.SELECTED:
            self.bgcolor = flet.Colors.BLUE_ACCENT
            self.border = flet.border.all(3, color=flet.Colors.WHITE)

        self.state = state

        return self.update()

    async def set_value(self, new_value: int):
        if self.state == MemoryCellState.NEVER_USED:
            await self.set_state(MemoryCellState.SELECTED)

        self.cell_value = new_value
        self.content.value = str(new_value)

        return self.update()

    async def increment(self):
        return await self.set_value(self.cell_value + 1)

    async def decrement(self):
        if self.cell_value <= 0:
            return await self.set_value(255)

        return await self.set_value(self.cell_value - 1)