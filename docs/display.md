# Display

## Legend

A table can have numerous legends, where each legend has a number of legend items. 

### LegendItem

Each legend item has a label and an icon.

## Formatting

Table Formatting can be applied to the whole row, by altering the style or by adding an icon in front of the row, or it can be applied to a single cell. Applying formatting to a whole row happens through `RowFormatting` and formatting a single cell happens through `ColumnFormatting`.

### RowFormatting

Applying formatting to a whole row through `RowFormatting` is always conditional on the value of a column and accepts two arguments: column and conditions, where column is the name of the column and conditions is a list of conditions, which are either `RowIconCondition` or `RowStyleCondition` and can be used interchangable. Each condition is checked, and if it validates, then it is applied.

### RowIconCondition

The `RowIconCondition` accepts two arguments, icon and condition. Icon is a string that the frontend can use to determine the icon class and condition is a tuple that is checked against the column specified in the `RowFormatting`. (More on conditions below)

### RowStyleCondition

The `RowStyleCondition` works analogous to the `RowIconCondition`, except that it does not accept icon as an argument, but rather a style, which is a dictionairy, which holds css classes and their values. (*Note: If the Frontend is based on React, css class name are written like backgroundColor and not background_color*)

### Conditions

The condition is represented by a tuple of an operator and a value. For example: (">", 5) verifies that the value of the column has to be greater than 5. For convenience all operators are accessible through the `bridger.enums.Operator` enum. The above example can be written as (Operator.GREATER.value, 5) with the enum. A list of all possible operator and how to use them are found below:

| Operator | Values            | Explanation                                                  | Enum                   |
|----------|-------------------|--------------------------------------------------------------|------------------------|
| ∃        | True, False       | Checks wether the column exists or not (e.g. is null or not) | Operator.EXISTS        |
| >        | [int, float]      | Checks wether the column is greater than a value             | Operator.GREATER       |
| >=       | [int, float]      | Checks wether the column is greater or equal than a value    | Operator.GREATER_EQUAL |
| <        | [int, float]      | Checks wether the column is less than a value                | Operator.LESS          |
| <=       | [int, float]      | Checks wether the column is less or equal than a value       | Operator.LESS_EQUAL    |
| ==       | [int, float, str] | Checks wether the column is equal to a value                 | Operator.EQUAL         |
| !=       | [int, float, str] | Checks wether the column is unequal to a value               | Operator.UNEQUAL       |

### Example

The below Example does two things:

1. If `number` is greater than 5, then the row gets a star icon.
2. If `number` is greater than 10, then the row gets a blue background color.

```python
from bridger import display as dp
from bridger.enums import Condition

LIST_DISPLAY = [
    formatting=[
        dp.RowFormatting(
            column="number",
            conditions=[
                dp.RowIconCondition(
                    icon="icon-star", condition=(Condition.GREATER.value, 5)
                ),
                dp.RowStyleCondition(
                    style={"backgroundColor": "rgb(13, 28, 189)",
                    condition=(Condition.GREATER.value, 10)
                )
            ]
        )
    ]
]
```