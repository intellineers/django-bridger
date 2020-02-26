### Row Formatting

**RowFormatting** accepts a column name and a list of conditions.

**RowIconCondition** accepts an icon and a condition, which is a tupe of an operator and a value

**condition**

| Operator | Values | Explanation | Example |
| -------- | ------ | ----------- | ------- |
| ∃       | True, False | Checks wether the column exists or not (e.g. is null or not) | ("∃", True) |
| > | [int] | Checks wether the column is greater than a value| (">", 4) |