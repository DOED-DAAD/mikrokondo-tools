"""
Create a gui using gui-gaga to create a run command.

As guigaga requires a click interface there will have to be some meta-programming
required to create the gui.

Matthew Wells: 2024-10-24
"""
from mikrokondo_tools.tui.schema_parser import SchemaParser
#from textual.app import App, ComposeResult
#from textual.widgets import Header, Footer
#from textual.containers import ScrollableContainer
#from textual.widgets import ListView, Footer, Header, ListItem, Label
#import mikrokondo_tools.utils as u



#class StopwatchApp(App):
#    """A Textual app to manage stopwatches."""
#
#    BINDINGS = [("d", "toggle_dark", "Toggle dark mode")]
#
#    def compose(self) -> ComposeResult:
#        """Create child widgets for the app."""
#        yield Header()
#        yield Footer()
#        yield ScrollableContainer(
#            ListView(ListItem(Label("One")), ListItem(Label("Two"))),
#        )
#
#    def action_toggle_dark(self) -> None:
#        """An action to toggle dark mode."""
#        self.dark = not self.dark



def tui():
    SchemaParser()
    #app = StopwatchApp()
    #app.run()
