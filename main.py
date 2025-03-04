import asyncio

import flet

from bf_studio.memory_container import MemoryContainer
from bf_studio.engine import CodeEvaluator


async def main(page: flet.Page):
    container = MemoryContainer()

    page.title = "bf_studio [0.0.4]"
    page.appbar = flet.AppBar(title=flet.Text('bf_studio'), elevation=1)

    page.add(
        flet.Card(
            content=flet.Container(
                padding=10,
                content=flet.Column(
                    controls=[
                        flet.Text('Program memory:'),
                        container
                    ]
                )
            ),
            elevation=2.5
        )
    )

    text = flet.Text('', size=24)

    page.add(
        flet.Card(
            content=flet.Container(
                padding=10,
                content=flet.Column(
                    controls=[
                        flet.Text('Output text:'),
                        text
                    ]
                )
            ),
            elevation=2.5
        )
    )

    code_field = flet.TextField(
        multiline=True,
        min_lines=3,
        max_lines=6,
        border_color='#333333'
    )

    async def add_character(character: str):
        text.value += character
        text.update()

    async def evaluate(_: flet.ControlEvent = None):
        await container.reset()
        text.value = ''
        text.update()

        evaluator = CodeEvaluator(
            code=code_field.value,
            memory_container=container,
            print_callback=add_character,
            input_callback=...
        )

        async for _ in evaluator.evaluate_stepper():
            await asyncio.sleep(0)

    page.add(
        flet.Card(
            content=flet.Container(
                padding=10,
                content=flet.Column(
                    controls=[
                        flet.Text('Code:'),
                        code_field,
                        flet.Row([
                            flet.ElevatedButton(
                                text='Execute',
                                icon=flet.Icons.PLAY_ARROW_SHARP,
                                on_click=evaluate
                            ),
                            flet.ElevatedButton(
                                text='Pause',
                                icon=flet.Icons.PAUSE_SHARP
                            ),
                            flet.ElevatedButton(
                                text='Step',
                                icon=flet.Icons.ARROW_FORWARD,
                                disabled=True
                            ),
                        ]),
                        flet.Row([
                            flet.Text('Execution speed:'),
                            flet.Slider(
                                min=0.1,
                                max=1,
                                divisions=9,
                                expand=True
                            )
                        ])
                    ]
                )
            ),
            elevation=2.5
        )
    )

if __name__ == '__main__':
    asyncio.run(flet.app_async(main))
