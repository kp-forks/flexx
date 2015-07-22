from time import perf_counter
from flexx import ui
from flexx import react

import flexx.ui.app.paired

class Name(ui.app.paired.Paired):
    
    class JS:
        @react.input
        def first_name(n):
            return n
        
        @react.act('foo')
        def bar(v):
            print('hellow from JS, foo =', v)
            # trigger a change in name
            if v==7:
                self.last_name('klein')
            if v==8:
                return self  # to test that we get the Name instance in Py
    
    @react.input
    def last_name(n='doe'):
        return n
    
    @react.watch('first_name', 'last_name')
    def full_name(n1, n2):
        return n1 + ' ' + n2
    
    @react.act('full_name')
    def show_name(n):
        print('name is:', n)
    
    def set_first_name_in_js(self, n):
        self.call_js('first_name(%r)' % n)
    
    @react.input
    def foo(v=42):
        # todo: initial value received by JS is null
        return float(v)
    
    @react.watch('bar')
    def bar_value(v):
        return v


# Create flexx app with a nodejs runtime (you could also use e.g. firefox here)
# todo: ui.run('nodejs') ?
# todo: why does nodejs not work?
app = ui.app.app.Proxy('__default__', 'nodejs')

name = Name(_proxy=app)
name.set_first_name_in_js('almar')