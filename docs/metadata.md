## Metadata Config

Each part of the metadata is configured through a config class, which inherits from `bridger.metadata.mixins.BridgerViewSetConfig`. This can be a class that is publically or privately declared, which means if the developer who implements a viewset has the possibilities to change things.

## Configurations

There are a couple of configurations that can, and should be set, by the developer that implements a viewset:

* `bridger.buttons.metadata_config.ButtonConfig` to configure the buttons of a viewset
* `bridger.display.metadata_config.DisplayConfig` to configure the display properties of a viewset

### ButtonConfig

Buttons get defined in form of a `bridger.buttons.<Type>Button`. More information on buttons can be found [here](buttons.md). The default `ButtonConfigClass` provides three things:

!!! Note
    Default buttons, such as Save, Save and Close, Refresh, Create, Delete, ... are automatically created through inferring actions based on endpoints

1. Transition buttons
1. Remote buttons

The metadata structure should look like the following graph:

blockdiag {
    buttons[label="buttons"];
    custom_instance[label="custom_instance"];
    _custom_instance[label="[Button()]"];
    custom[label="custom"];
    _custom[label="[Button()]"];

    buttons -> custom_instance;
    custom_instance -> _custom_instance;
    buttons -> custom;
    custom -> _custom;
}

#### Transition Buttons

The transition buttons are provided by a set called `fsm_buttons` where buttons are added to. There are a few additional properties that can be set to determine the visualization of the `fsm_buttons`:

| Property           | Default      | Meaning                                                            |
| ------------------ | ------------ | ------------------------------------------------------------------ |
| FSM_LIST           | True         | Show the transition buttons in lists views                         |
| FSM_INSTANCE       | True         | Show the transition buttons in instance views                      |
| FSM_DROPDOWN       | False        | Show the transition buttons inside a dropdown button               |
| FSM_DROPDOWN_ICON  | wb-icon-plus | The icon of the FSM_DROPDOWN                                       |
| FSM_DROPDOWN_LABEL | Transitions  | The label of the FSM_DROPDOWN                                      |
| FSM_WEIGHT         | 100          | The default weight of the transition buttons (or the FSM_DROPDOWN) |

#### Remote Buttons

Remote buttons are created through custom Django Signals by sending them from one app directly into a viewset. [remote buttons](buttons.md#remote-buttons)

#### Custom Instance Buttons

Adding custom buttons onto an instance (both instance and list views) can be achieved in two ways.

**Providing a set**

* For instance views: `CUSTOM_INSTANCE_BUTTONS = {}`
* For list views: `CUSTOM_LIST_INSTANCE_BUTTONS = {}`

**Overriding the method**

For instance views:
```python
def get_custom_instance_buttons(self) -> Set:
```

For list views:
```python
def get_custom_list_instance_buttons(self) -> Set:
```

!!! hint
    The `BridgerViewSetConfig` has access to the following fields by default: `view: View`, `request: Request` and `instance: bool` (indicates whether it is an instance view or a list view)

#### Custom Buttons

Custom buttons behave exactly like Custom Instance Buttons, except that they are not bound to a single instance. (E.g. when defining custom buttons they will show only once in both instance and list views).

!!! important
    Custom buttons may never define `keys` and should only define `endpoints`

### DisplayConfig

The display config is set as `display_config_class` and the default provides empty list_display and instance_display configurations.

In order to set a configuration, override `bridger.display.metadata_config.DisplayConfigClass` and implement the following methods:

* `def get_instance_display(self) -> InstanceDisplay:`
* `def get_list_display(self) -> ListDisplay:`

### TitleConfig

The title config is set as `title_config_class` and the default provides sensible namings for each possible scenario in the following way:

* instance: `<verbose_name>: str(model)`
* list: `<verbose_name_plural>`
* create: `Create <verbose_name>`
* delete: `Delete <verbose_name>: str(model)`

If you wish you override this behaviour, override `bridger.titles.metadata_config.TitleConfigClass` and set it as the config class of the viewset.

### EndpointConfig

The endpoints are set as `endpoint_config_class` in the viewset and can be customized by overriding `bridger.endpoints.metadata_config.EndpointConfigClass`. The default uses the basename of the underlying model by accessing the classmethod `def get_basename(cls):` and using the basename to determine all endpoints. If you want to override this, there are five methods to consider:

* `def get_endpoint(self):` base endpoint that gets used by every other endpoint method if not overriden
* `def get_instance_endpoint(self)`
* `def get_list_endpoint(self)`
* `def get_create_endpoint(self)`
* `def get_delete_endpoint(self)`

The four last methods by default return whatever `def get_endpoint(self)` returns. All of those methods have an underscore methods (e.g. `def _get_instance_endpoint(self):`) to determine permissions and set handlebar-identifiers. This should usually never be overriden.

### PreviewConfig

If a viewset should provide a preview mode, then a `preview_config_class` has to be provided by overriding `bridger.preview.metadata_config.PreviewConfigClass`. At least the method `def get_display(self)` has to be overriden and it needs to return an `InstanceDisplay`. (You can also return HTML when setting `DISPLAY_TYPE="html"`)

Furthermore if you want to display a set of buttons, you need to override `def get_buttons(self):`, which should return a set of buttons.