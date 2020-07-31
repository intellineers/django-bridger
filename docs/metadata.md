## Metadata Config

Each part of the metadata is configured through a config class, which inherits from `bridger.metadata.mixins.BridgerViewSetConfig`. This can be a class that is publically or privately declared, which means if the developer who implements a viewset has the possibilities to change things.

## Configurations

There are a couple of configurations that can, and should be set, by the developer that implements a viewset:

* `bridger.buttons.metadata_config.ButtonConfig` to configure the buttons of a viewset
* `bridger.display.metadata_config.DisplayConfig` to configure the display properties of a viewset

### ButtonConfig

Buttons either get defined as string or in form of a `bridger.buttons.<Type>Button`. More information on buttons can be found [here](buttons.md).

blockdiag {
    buttons[label="buttons"];
    instance[label="instance"];
    _instance[label="['type']"];
    list[label="list"];
    _list[label="['type']"];
    create[label="create"];
    _create[label="['type']"];
    custom_instance[label="custom_instance"];
    _custom_instance[label="[Button()]"];
    custom[label="custom"];
    _custom[label="[Button()]"];

    buttons -> instance;
    instance -> _instance;
    buttons -> list;
    list -> _list;
    buttons -> create;
    create -> _create;
    buttons -> custom_instance;
    custom_instance -> _custom_instance;
    buttons -> custom;
    custom -> _custom;
}