import wx
import wx.adv
# TODO: warn on unknown props?
from rewx.dispatch import mount, update

from rewx.components import Block, Grid, TextArea


def noop(*args, **kwargs):
    return None


basic_controls = {
    '*': {
    },
    'label': 'SetLabel',
    'value': 'SetValue',
    'background_color': 'SetBackgroundColour',
    'foreground_color': 'SetForegroundColour',
    'font': 'SetFont',
    'helptext': 'SetHelpText',
    'name': 'SetName',
    'minsize': 'SetMinSize',
    'maxsize': 'SetMaxSize',
    'tooltip': 'SetToolTip',
    'show': 'Show',
    'enabled': 'Enable',
    'style': 'SetStyle',
}




def set_basic_props(instance, props):
    for key, val in props.items():
        if key.startswith('on_'):
            continue
        try:
            getattr(instance, basic_controls[key])(val)
        except KeyError:
            # prop which doesn't apply to this control
            pass
    return instance




@mount.register(wx.ActivityIndicator)
def activity_indicator(element, parent):
    return wx.ActivityIndicator(parent)

@update.register(wx.ActivityIndicator)
def activity_indicator(element, instance: wx.ActivityIndicator):
    props = element['props']
    set_basic_props(instance, props)
    if props.get('start'):
        instance.Stop()
    else:
        instance.Stop()
    return instance

@mount.register(wx.Button)
def button(element, parent):
    return update(element, wx.Button(parent))


@update.register(wx.Button)
def button(element, instance: wx.Button):
    props = element['props']
    set_basic_props(instance, props)
    instance.Unbind(wx.EVT_BUTTON)
    if props.get('on_click'):
        instance.Bind(wx.EVT_BUTTON, props['on_click'])
    return instance


@mount.register(wx.ToggleButton)
def togglebutton(element, parent):
    return wx.ToggleButton(parent)


@update.register(wx.ToggleButton)
def togglebutton(element, instance: wx.ToggleButton):
    props = element['props']
    set_basic_props(instance, props)
    instance.Unbind(wx.EVT_TOGGLEBUTTON)
    if props.get('on_click'):
        instance.Bind(wx.EVT_TOGGLEBUTTON, props['on_click'])
    return instance



@mount.register(wx.BitmapButton)
def bitmapbutton(element, parent):
    return update(element, wx.BitmapButton(parent))


@update.register(wx.BitmapButton)
def bitmapbutton(element, instance: wx.BitmapButton):
    props = element['props']
    set_basic_props(instance, props)

    if instance.GetBitmap():
        instance.GetBitmap().Destroy()
    bitmap = wx.Bitmap(props.get('uri'))
    instance.SetBitmap(bitmap)

    instance.Unbind(wx.EVT_BUTTON)
    if props.get('on_click'):
        instance.Bind(wx.EVT_BUTTON, props['on_click'])
    return instance


@mount.register(wx.adv.CalendarCtrl)
def calendarctrl(element, parent):
    return wx.adv.CalendarCtrl(parent)


@update.register(wx.adv.CalendarCtrl)
def calendarctrl(element, instance: wx.adv.CalendarCtrl) -> wx.Object:
    props = element['props']
    set_basic_props(instance, props)
    additions = {
        'selected_date': 'SetDate',
        'display_holidays': 'EnableHolidayDisplay',
        'allow_month_change': 'EnableMonthChange',
    }
    for prop_key, wx_method in additions.items():
        if prop_key in props:
            getattr(instance, wx_method)(props[prop_key])

    instance.Unbind(wx.adv.EVT_CALENDAR_SEL_CHANGED)
    if props.get('on_change'):
        # TODO: verify callable?
        instance.Bind(wx.adv.EVT_CALENDAR_SEL_CHANGED, props['on_change'])
    return instance

@mount.register(wx.CheckBox)
def checkbox(element, parent):
    return wx.CheckBox(parent)


@update.register(wx.CheckBox)
def checkbox(element, instance: wx.CheckBox):
    props = element['props']
    set_basic_props(instance, props)
    instance.Unbind(wx.EVT_CHECKBOX)
    if props.get('on_change'):
        instance.Bind(wx.EVT_CHECKBOX, props['on_change'])
    return instance


@mount.register(wx.CollapsiblePane)
def collapsiblepanel(element, parent):
    return wx.CollapsiblePane(parent)

@update.register(wx.CollapsiblePane)
def collapsiblepanel(element, instance: wx.CollapsiblePane):
    props = element['props']
    set_basic_props(instance, props)
    instance.Collapse(props.get('collapsed', False))
    instance.Unbind(wx.EVT_COLLAPSIBLEPANE_CHANGED)
    if props.get('on_change'):
        instance.Unbind(wx.EVT_COLLAPSIBLEPANE_CHANGED, props['on_change'])
    return instance


@mount.register(wx.ComboBox)
def combobox(element, parent):
    return update(element, wx.ComboBox(parent, choices=element['props'].get('choices', [])))

@update.register(wx.ComboBox)
def combobox(element, instance: wx.ComboBox) -> wx.Object:
    props = element['props']
    instance.Unbind(wx.EVT_COMBOBOX)
    instance.Unbind(wx.EVT_TEXT)
    # rebind as relevant
    if props.get('on_change'):
        instance.Bind(wx.EVT_COMBOBOX, props['on_change'])
    if props.get('on_input'):
        instance.Bind(wx.EVT_TEXT, props['on_input'])

    # set_basic_props(instance, props)
    for _ in instance.GetItems():
        instance.Delete(0)
    instance.AppendItems(props['choices'])
    instance.SetSelection(props['choices'].index(props['value']))
    print('will set value to:', props.get('value'))
    # if props.get('value') and instance.GetValue() != props['value']:
    # instance.ChangeValue(props.get('value', ''))
    # clean up existing handlers (if any)

    # instance.Show(False)
    # instance.SetValue(props.get('value', ''))
    # instance.Show(True)
    return instance


@mount.register(wx.Gauge)
def gauge(element, parent):
    return wx.Gauge(parent)

@update.register(wx.Gauge)
def gauge(element, instance: wx.Gauge) -> wx.Object:
    props = element['props']
    set_basic_props(instance, props)
    if props.get('range'):
        instance.SetRange(props['range'])
    if props.get('pulse', False):
        instance.Pulse()
    return instance


@mount.register(wx.ListBox)
def listbox(element, parent):
    return wx.ListBox(parent)

@update.register(wx.ListBox)
def listbox(element, instance: wx.ListBox):
    props = element['props']
    # TODO:
    pass


@mount.register(wx.ListCtrl)
def listctrl(element, parent):
    return update(element, wx.ListCtrl(parent, style=wx.LC_REPORT))

@update.register(wx.ListCtrl)
def listctrl(element, instance: wx.ListCtrl):
    props = {**element['props']}
    del props['style']
    set_basic_props(instance, props)
    # TODO: what events...?
    instance.DeleteAllColumns()
    instance.DeleteAllItems()
    for e, col in enumerate(props.get('column_defs', [])):
        instance.InsertColumn(e, col['title'])

    for row_idx, item in enumerate(props.get('data', [])):
        instance.InsertItem(row_idx, '')
        for col_idx, coldef in enumerate(props.get('column_defs', [])):
            instance.SetItem(row_idx, col_idx, coldef['column'](item))
    return instance


@mount.register(wx.RadioBox)
def radiobox(element, parent):
    return update(element, wx.RadioBox(parent))

@update.register(wx.RadioBox)
def radiobox(element, instance: wx.RadioBox):
    """
    Note: choices are not possible to change after
    being created when using RadioBox. Thus, they're
    not modified here.
    """
    props = element['props']
    set_basic_props(instance, props)
    if props.get('selected'):
        instance.SetSelection(props['selected'])
    instance.Unbind(wx.EVT_RADIOBOX)
    if props.get('on_change'):
        instance.Bind(wx.EVT_RADIOBOX, props['on_change'])


@mount.register(wx.StaticBox)
def staticbox(element, parent):
    return update(element, wx.StaticBox(parent))

@update.register(wx.StaticBox)
def staticbox(element, instance: wx.StaticBox):
    props = element['props']
    # TODO: does this auto-use a sizer..?
    set_basic_props(instance, props)
    return instance


@mount.register(wx.Slider)
def slider(element, parent):
    return update(element, wx.Slider(parent))

@update.register(wx.Slider)
def slider(element, instance: wx.Slider):
    props = element['props']
    set_basic_props(instance, props)
    instance.SetMax(props.get('max', 100))
    instance.SetMin(props.get('min', 0))
    instance.Unbind(wx.EVT_SLIDER)
    if 'on_change' in props:
        instance.Bind(wx.EVT_SLIDER, props['on_change'])
    return instance


@mount.register(wx.SpinCtrl)
def spinctrl(element, parent):
    return update(element, wx.SpinCtrl(parent))

@update.register(wx.SpinCtrl)
def spinctrl(element, instance: wx.SpinCtrl):
    props = element['props']
    set_basic_props(instance, props)
    instance.SetMax(props.get('max', 100))
    instance.SetMin(props.get('min', 0))
    instance.Unbind(wx.EVT_SPINCTRL)
    if 'on_change' in props:
        instance.Bind(wx.EVT_SLIDER, props['on_change'])
    return instance


@mount.register(wx.SpinCtrlDouble)
def spinctrldouble(element, parent):
    return update(element, wx.SpinCtrlDouble(parent))

@update.register(wx.SpinCtrlDouble)
def spinctrldouble(element, instance: wx.SpinCtrlDouble):
    props = element['props']
    set_basic_props(instance, props)
    instance.SetMax(props.get('max', 100))
    instance.SetMin(props.get('min', 0))
    instance.SetIncrement(props.get('increment', 0))
    if 'digits' in props:
        instance.SetDigits(props['digits'])
    instance.Unbind(wx.EVT_SPINCTRL)
    if 'on_change' in props:
        instance.Bind(wx.EVT_SLIDER, props['on_change'])
    return instance


@mount.register(wx.StaticText)
def statictext(element, parent):
    return update(element, wx.StaticText(parent))

@update.register(wx.StaticText)
def statictext(element, instance: wx.StaticText):
    # TODO: it does NOT response to 'SetValue'
    # this means set_basic needs to accept a map, not use
    # a fixed list.
    props = element['props']
    set_basic_props(instance, props)
    instance.Unbind(wx.EVT_LEFT_DOWN)
    if 'on_click' in props:
        instance.Bind(wx.EVT_LEFT_DOWN, props['on_click'])
    return instance


@mount.register(TextArea)
def textarea(element, parent):
    return update(element, TextArea(parent, style=wx.TE_MULTILINE))

@update.register(TextArea)
def textarea(element, instance: TextArea):
    # TODO: it does NOT response to 'SetValue'
    # this means set_basic needs to accept a map, not use
    # a fixed list.
    props = {**element['props']}
    value = props.get('value','')
    if 'value' in props:
        del props['value']
    if 'style' in props:
        props['style'] = props['style'] | wx.TE_MULTILINE

    set_basic_props(instance, props)
    before = instance.GetInsertionPoint()
    instance.ChangeValue(value)
    instance.SetInsertionPoint(before)
    instance.Unbind(wx.EVT_LEFT_DOWN)
    instance.Unbind(wx.EVT_TEXT)
    if 'on_click' in props:
        instance.Bind(wx.EVT_LEFT_DOWN, props['on_click'])
    if 'on_change' in props:
        instance.Bind(wx.EVT_TEXT, props['on_change'])
    return instance



@mount.register(wx.Panel)
def panel(element, parent):
    return update(element, wx.Panel(parent))


@update.register(wx.Panel)
def panel(element, instance: wx.Panel):
    props = element['props']
    set_basic_props(instance, props)
    instance.Unbind(wx.EVT_LEFT_DOWN)
    if 'on_click' in props:
        instance.Bind(wx.EVT_LEFT_DOWN, props['on_click'])
    return instance


@mount.register(Block)
def block(element, parent):
    panel = update(element, Block(parent))
    sizer = wx.BoxSizer(element['props'].get('orient', wx.VERTICAL))
    panel.SetSizer(sizer)
    return panel

@update.register(Block)
def block(element, instance: Block):
    props = element['props']
    set_basic_props(instance, props)
    instance.Unbind(wx.EVT_LEFT_DOWN)
    if 'on_click' in props:
        instance.Bind(wx.EVT_LEFT_DOWN, props['on_click'])
    return instance



@mount.register(Grid)
def grid(element, parent):
    props = element['props']
    panel = Grid(parent)
    sizer = wx.GridSizer(props.get('cols', 1), gap=props.get('gap', (0, 0)))
    panel.SetSizer(sizer)
    return update(element, panel)


@update.register(Grid)
def grid(element, instance: Grid):
    props = element['props']
    set_basic_props(instance, props)
    instance.Unbind(wx.EVT_LEFT_DOWN)
    if 'on_click' in props:
        instance.Bind(wx.EVT_LEFT_DOWN, props['on_click'])
    return instance



@mount.register(wx.TextCtrl)
def textctrl(element, parent):
    return update(element, wx.TextCtrl(parent))


@update.register(wx.TextCtrl)
def textctrl(element, instance: wx.TextCtrl):
    props = element['props']
    set_basic_props(instance, props)
    if 'editable' in props:
        instance.SetEditable(props['editable'])
    instance.Unbind(wx.EVT_TEXT)
    if 'on_change' in props:
        instance.Bind(wx.EVT_TEXT, props['on_change'])
    return instance


@mount.register(wx.StaticBitmap)
def staticbitmap(element, parent):
    return update(element, wx.StaticBitmap(parent))


@update.register(wx.StaticBitmap)
def staticbitmap(element, instance: wx.StaticBitmap):
    props = element['props']
    if instance.GetBitmap():
        instance.GetBitmap().Destroy()
    if 'uri' in props:
        bitmap = wx.Bitmap(props.get('uri'))
        instance.SetBitmap(bitmap)
    return instance


@mount.register(wx.StaticLine)
def staticline(element, parent):
    return update(element, wx.StaticLine(parent))


@update.register(wx.StaticLine)
def staticline(element, instance: wx.StaticLine):
    set_basic_props(instance, element['props'])
    return instance


@mount.register(wx.RadioBox)
def radiobox(element, parent):
    return update(element, wx.RadioBox(parent, choices=element['props'].get('choices', [])))


@update.register(wx.RadioBox)
def radiobox(element, instance: wx.RadioBox):
    props = element['props']
    set_basic_props(instance, props)
    if 'selected' in props:
        instance.SetSelection(props['selected'])
    if 'enabled_items' in props:
        for item in props['enabled_items']:
            instance.EnableItem(item)
    instance.Unbind(wx.EVT_RADIOBOX)
    if 'on_change' in props:
        instance.Bind(wx.EVT_RADIOBOX, props['on_change'])
    return instance


@mount.register(wx.RadioButton)
def radiobutton(element, parent):
    # we force the style RB_SINGLE here and don't
    # allow it to be overriden so that these individual
    # buttons can act as controlled components
    return update(element, wx.RadioButton(parent, style=wx.RB_SINGLE))


@update.register(wx.RadioButton)
def radiobutton(element, instance: wx.RadioButton):
    # TODO: exclude style prop
    props = element['props']
    set_basic_props(instance, props)
    instance.SetValue(props.get('selected', False))
    instance.Unbind(wx.EVT_RADIOBUTTON)
    if 'on_change' in props:
        instance.Bind(wx.EVT_RADIOBUTTON, props['on_change'])
    return instance





# TODO: keeping this arond to eventually generate prop validation
_supported_props = {
    'wx.Window': {
        'api': {
            'SetLabel': 'label',
            'SetBackgroundColour': 'background_color',
            'SetForegroundColour': 'foreground_color',
            'SetDropTarget': 'on_drop:lambda',
            'SetFont': 'font: wx.Font',
            'SetHelpText': 'help_text: str',
            'SetName': 'name: str', # very useful for debugging via inspector
            'SetMinSize': 'min_size',
            'SetMaxSize': 'max_size',
            'SetToolTip': 'tooltip',
            'Show': 'show',
            'SetStyle': 'style'
        },
        'wx.ActivityIndicator': {
            'start': 'Start'
        },
        'wx.adv.CalendarCtrl': {
            'selected_date': 'SetDate', # ?
            'holiday_display': 'EnableHolidayDisplay',
            'month_change': 'EnableMonthChange',

            'EVT_CALENDAR_SEL_CHANGED': 'on_change: fn',
        },
        'wx.CheckBox': {
            'SetValue': 'checked: boolean',
            'EVT_CHECKBOX': 'on_change',
            'SetLabel': 'label: str'
        },
        'wx.CollapsiblePanel': {
            'SetCollapsed': 'collapsed: bool',
            'EVT_COLLAPSIBLEPANE_CHANGED': 'on_change'
        },
        'wx.Choice': {

        },
        'wx.ComboBox': {
            'EVT_COMBOBOX': 'on_change',
            'EVT_TEXT': 'on_input',
            'choices': 'choices', # update will use AppendItems
            'SetValue': 'value: str'
        },
        'wx.Gauge': {
            'style': 'style',
            'Pulse': 'pulse: bool',
            'SetRange': 'range: int', # sets the maximum value, so just needs an int
            'SetValue': 'value: int'
        },
        'wx.ListBox': {
            'style': 'style',
            'EVT_LISTBOX': 'on_change',
            'choices': 'choices', # update will use InsertItems,
            'SetSelection': 'value:[str]', # ?
        },
        # this one will be a massive departure from
        # its WX API. See: youtube-dl example for usage
        # TODO: general event escape hatch?
        #       e.g. {'event-handler': {'type': wx.EVT_LIST_COL_CLICK, 'fn': lambda x...}}
        'wx.ListCtrl': {
            'style': 'style',
            'DeleteAllColumns/InsertColumn': 'column_def: [ColumnDef]',
            'DeleteAllItems/SetItem': 'data: [Any]',
            'EVT_LIST_ITEM_SELECTED': 'on_selection', # ?
        },
        'wx.RadioBox': {
            'SetSelection': 'selected: Int',
            'choices': 'choices',
            'EnableItem': 'disabled:[n]',
            'EVT_RADIOBOX': 'on_change'
        },
        'wx.RadioButton': {
            'style': 'FORCE ONLY: wx.RB_SINGLE', # this style is forced so that WX doesn't control the clicky clicky
            'SetValue': 'selected:bool',
            'EVT_RADIOBUTTON': 'on_change'
        },
        # this is just a container like block
        'wx.StaticBox': {
            'label': 'label'
        },
        'wx.Slider': {
            'style': 'style',
            'EVT_SLIDER': 'on_change',
            'SetMax': 'max',
            'SetMin': 'min',
            'SetValue': 'value'
        },
        'wx.SpinCtrl': {
            'style': 'style',
            'EVT_SPINCTRL': 'on_change',
            'SetMax': 'max',
            'SetMin': 'min',
            'SetValue': 'value'
        },
        'wx.SpinCtrlDouble': {
            'style': 'style',
            'EVT_SPINCTRLDOUBLE': 'on_change',
            'SetMax': 'max',
            'SetMin': 'min',
            'SetIncrement': 'increment',
            'SetPrecision': 'precision',
            'SetValue': 'value'
        },
        'wx.StaticBitmap': {
            'SetBitmap': 'uri',
        },
        'wx.Button': {
            'EVT_BUTTON': 'on_click',
            # wx.Control stuff label, enabled, etc..
        },
        'wx.BitmapButton': {
            'EVT_BUTTON': 'on_click',
            'SetBitmap': 'uri'
        },
        'wx.ToggleButton': {
            'EVT_TOGGLEBUTTON': 'on_click',
            'SetValue': 'value:bool'
        },
        'wx.StaticLine': {
            'style': 'style',
        },
        'wx.StatusBar': {
            'SetStatusText': 'text:str'
        },
        'textEntry': {
                'SetEditable',
                'SetHint',
                'ChangeValue' # for updates
            },
    }
}


