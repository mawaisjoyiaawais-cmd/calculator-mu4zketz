from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.textinput import TextInput
from kivy.config import Config

# For desktop testing, to make it look like a phone
Config.set('graphics', 'width', '360')
Config.set('graphics', 'height', '640')

class CalculatorApp(App):
    def build(self):
        self.operators = ["/", "*", "+", "-"]
        self.last_was_operator = None
        self.last_button = None

        main_layout = BoxLayout(orientation='vertical', spacing=5, padding=10)

        # Solution display
        self.solution = TextInput(
            text="",
            font_size=64,
            readonly=True,
            halign='right',
            multiline=False,
            size_hint_y=0.25
        )
        main_layout.add_widget(self.solution)

        # Button grid
        buttons = [
            ['7', '8', '9', '/'],
            ['4', '5', '6', '*'],
            ['1', '2', '3', '-'],
            ['C', '0', '.', '+']
        ]

        grid = GridLayout(cols=4, spacing=5)
        for row in buttons:
            for label in row:
                button = Button(
                    text=label,
                    font_size=40,
                    background_color=(0.25, 0.25, 0.25, 1),
                    color=(1, 1, 1, 1)
                )
                button.bind(on_press=self.on_button_press)
                grid.add_widget(button)
        main_layout.add_widget(grid)

        # Equals button
        equals_button = Button(
            text='=',
            font_size=40,
            size_hint_y=None,
            height=100,
            background_color=(0.2, 0.6, 0.2, 1)
        )
        equals_button.bind(on_press=self.on_solution)
        main_layout.add_widget(equals_button)

        return main_layout

    def on_button_press(self, instance):
        current_text = self.solution.text
        button_text = instance.text

        if button_text == 'C':
            self.solution.text = ''
            self.last_was_operator = None
            self.last_button = None
            return

        # Prevent adding multiple operators in a row
        if self.last_was_operator and button_text in self.operators:
            return
        
        # Prevent starting with an operator (except for a potential negative sign, handled by eval)
        if current_text == '' and button_text in self.operators and button_text != '-':
            return
        
        # Prevent multiple decimal points in one number
        if button_text == '.':
            # Find the last operator to check the current number segment
            last_op_index = -1
            for op in self.operators:
                last_op_index = max(last_op_index, current_text.rfind(op))
            
            if '.' in current_text[last_op_index+1:]:
                return

        self.solution.text += button_text
        self.last_was_operator = button_text in self.operators
        self.last_button = button_text

    def on_solution(self, instance):
        text = self.solution.text
        if text:
            try:
                # Sanitize input: do not end with an operator
                if text[-1] in self.operators:
                    text = text[:-1]

                # The eval function is used for simplicity. 
                # For a production app, a more secure parser is recommended.
                result = str(eval(text))
                self.solution.text = result
            except Exception:
                self.solution.text = 'Error'
        
        self.last_was_operator = False
        self.last_button = None

if __name__ == '__main__':
    CalculatorApp().run()
