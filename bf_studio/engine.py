from typing import Callable

from bf_studio.memory_container import MemoryContainer


class CodeEvaluator:
    def __init__(
            self,
            code: str,
            memory_container: MemoryContainer,
            print_callback: Callable,
            input_callback: Callable
    ):
        self.memory_container = memory_container
        self.print_callback = print_callback
        self.input_callback = input_callback
        self.code = code
        self.code_pointer = 0
        self.temp_brace_stack = []
        self.bracemap = {}

    def build_bracemap(self):
        for position, token in enumerate(self.code):
            if token == "[":
                self.temp_brace_stack.append(position)
            if token == "]":
                start = self.temp_brace_stack.pop()
                self.bracemap[start] = position
                self.bracemap[position] = start

        return self.bracemap

    async def execute_at_pointer(self):
        token = self.code[self.code_pointer]

        if token == ">":
            await self.memory_container.next()

        elif token == "<":
            await self.memory_container.back()

        elif token == "+":
            await self.memory_container.selected_cell.increment()

        elif token == "-":
            await self.memory_container.selected_cell.decrement()

        elif token == "[" and self.memory_container.selected_cell.cell_value == 0:
            self.code_pointer = self.bracemap[self.code_pointer]

        elif token == "]" and self.memory_container.selected_cell.cell_value != 0:
            self.code_pointer = self.bracemap[self.code_pointer]

        elif token == ".":
            character = chr(self.memory_container.selected_cell.cell_value)
            await self.print_callback(character)

        elif token == ",":
            raise NotImplementedError

    async def evaluate(self):
        self.build_bracemap()
        while self.code_pointer < len(self.code):
            await self.execute_at_pointer()
            self.code_pointer += 1

    async def evaluate_stepper(self):
        self.build_bracemap()
        while self.code_pointer < len(self.code):
            yield await self.execute_at_pointer()
            self.code_pointer += 1
