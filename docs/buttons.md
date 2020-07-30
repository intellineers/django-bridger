# Buttons

There are different kinds of buttons that can be implemented through the bridger, system buttons and custom buttons.

## System Buttons

System buttons are buttons reoccurring buttons with a default behaviour:

* save
    * Saves an instance (`bridger.enums.Button.SAVE`)
* saveandnew
    * Saves an instance and opens a new instance (`bridger.enums.Button.SAVE_AND_NEW`)
* saveandclose
    * Saves an instance and closes the instance (`bridger.enums.Button.SAVE_AND_CLOSE`)
* delete
    * Deletes and instance (`bridger.enums.Button.DELETE`)
* new
    * Opens a new instance (`bridger.enums.Button.NEW`)
* refresh
    * Refreshes a list/instance (`bridger.enums.Button.REFRESH`)
* reset
    * Resets a new instance (`bridger.enums.Button.RESET`)

## Custom Buttons

Custom buttons have a custom behaviour and can be attached to a list or an instance. There are four different custom buttons:

* Hyperlink
    * Creates a hyperlink to an url (`bridger.buttons.HyperlinkButton`)
* Widget
    * Opens a widget (`bridger.buttons.WidgetButton`)
* Dropdown
    * Nests other buttons in a dropdown menu (`bridger.buttons.DropdownButton`)
* Action
    * Creates a custom action (`bridger.buttons.ActionButton`)

The defaulf properties are as following:

| Property | Required                | Value                                    |
|----------|-------------------------|------------------------------------------|
| label    | yes, if icon is None    | A string that is rendered on the button  |
| icon     | yes, if label is None   | A string that represents an icon class   |
| title    | no                      | A string that is used as the hover title |
| key      | yes if endpoint is None | A string that matches against an url     |
| endpoint | yes if key is None      | A url                                    |



