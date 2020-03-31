# Model Test

The Model Test is an example of a model which incorporates all possible fields and therefore shows how all fields are rendered with their filters, etc.

### The fields are:

| Field Name      | Field Label | Type     | Extra                               |
|-----------------|-------------|----------|-------------------------------------|
| char_field      | Char        | text     |                                     |
| text_field      | Text        | textarea |                                     |
| integer_field   | Integer     | number   | precision=0                         |
| float_field     | Float       | number   |                                     |
| decimal_field   | Decimal     | number   | precision=4,max_digits=7            |
| datetime_field  | DateTime    | datetime |                                     |
| datetime_field1 | DateTime 1  | datetime |                                     |
| date_field      | Date        | date     |                                     |
| time_field      | Time        | time     |                                     |
| boolean_field   | Boolean     | boolean  |                                     |
| choice_field    | Choice      | select   | choices=[A, B]                      |
| status_field    | Status      | select   | choices=[Status1, Status2, Status3] |
| image_field     | Image       | image    |                                     |
| file_field      | File        | file     |                                     |

### The default workflow is:

blockdiag {
    Status1 -> Status2 -> Status3;
    Status2 -> Status3;
}