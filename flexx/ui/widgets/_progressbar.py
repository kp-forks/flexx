""" ProgressBar

Simple example:

.. UIExample:: 50
    
    from flexx import app, ui
    
    class Example(ui.HFix):
        def init(self):
            ui.ProgressBar(value=0.7)


Interactive example:

.. UIExample:: 100

    from flexx import app, ui, event
    
    class Example(ui.Widget):
    
        def init(self):
            with ui.HBox():
                self.b1 = ui.Button(flex=0, text='Less')
                self.b2 = ui.Button(flex=0, text='More')
                self.prog = ui.ProgressBar(flex=1, value=0.1, text='{percent} done')
    
        @event.reaction('b1.mouse_down', 'b2.mouse_down')
        def _change_progress(self, *events):
            for ev in events:
                if ev.source is self.b1:
                    self.prog.set_value(self.prog.value - 0.1)
                else:
                    self.prog.set_value(self.prog.value + 0.1)
"""

from ... import event
from .._widget import Widget, create_element


class ProgressBar(Widget):
    """ A widget to show progress.
    """
    
    CSS = """
    
    .flx-ProgressBar {
        min-height: 10px;
        min-width: 40px;
        border-radius: 10px;
        background: rgba(0, 0, 0, 0.1);
    }
    
    .flx-ProgressBar > .progress-bar {
        /* Use flexbox to vertically align label text */
        display: -webkit-flex;
        display: -ms-flexbox;
        display: -ms-flex;
        display: -moz-flex;
        display: flex;
        -webkit-flex-flow: column;
        -ms-flex-flow: column;
        -moz-flex-flow: column;
        flex-flow: column;
        -webkit-justify-content: center;
        -ms-justify-content: center;
        -moz-justify-content: center;
        justify-content: center;
        white-space: nowrap;
        
        background: #8af;
        text-align: center;
        transition: width 0.2s ease;
        }
    
    """
    
    value = event.FloatProp(0, settable=True, doc="""
            The progress value.
            """)
    
    min = event.FloatProp(0, settable=True, doc="""
        The minimum progress value.
        """)
    
    max = event.FloatProp(1, settable=True, doc="""
        The maximum progress value.
        """)
    
    text = event.StringProp('', settable=True, doc="""
        The label to display on the progress bar. Occurances of
        "{percent}" are replaced with the current percentage, and
        "{value}" with the current value.
        """)
    
    @event.action
    def set_value(self, value):
        value = max(self.min, value)
        value = min(self.max, value)
        self._mutate_value(value)
    
    def _render_dom(self):
        global Math
        value = self.value
        mi, ma = self.min, self.max
        perc = 100 * (value - mi) / (ma - mi)
        label = self.text
        label = label.replace('{value}', str(value))
        label = label.replace('{percent}', Math.round(perc) + '%')
        attr = {'style__width': perc+'%',
                'style__height': '100%',
                'className': 'progress-bar'
                }
        return [create_element('div', attr, label)]
