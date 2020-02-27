# Row Formatting

**RowFormatting** accepts a column name and a list of conditions.

**RowIconCondition** accepts an icon and a condition, which is a tupe of an operator and a value

**condition**

| Operator | Values            | Explanation                                                  | Enum                   |
|----------|-------------------|--------------------------------------------------------------|------------------------|
| ∃        | True, False       | Checks wether the column exists or not (e.g. is null or not) | Operator.EXISTS        |
| >        | [int, float]      | Checks wether the column is greater than a value             | Operator.GREATER       |
| >=       | [int, float]      | Checks wether the column is greater or equal than a value    | Operator.GREATER_EQUAL |
| <        | [int, float]      | Checks wether the column is less than a value                | Operator.LESS          |
| <=       | [int, float]      | Checks wether the column is less or equal than a value       | Operator.LESS_EQUAL    |
| ==       | [int, float, str] | Checks wether the column is equal to a value                 | Operator.EQUAL         |
| !=       | [int, float, str] | Checks wether the column is unequal to a value               | Operator.UNEQUAL       |