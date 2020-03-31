# Model Test

The Model Test is an example of a model which incorporates all possible fields and therefore shows how all fields are rendered with their filters, etc.

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aliquam hendrerit nisl et sodales convallis. Aenean nec nibh finibus, rhoncus dolor at, sagittis ante. Pellentesque vestibulum varius consectetur. Nam eget nulla mi. Suspendisse potenti. Aliquam fermentum augue purus, porttitor laoreet eros sagittis at. Fusce vitae sapien et elit facilisis gravida vel ut elit. Interdum et malesuada fames ac ante ipsum primis in faucibus. Maecenas porttitor lectus non massa maximus tincidunt. Cras pellentesque tincidunt diam et ultricies. Maecenas tincidunt molestie magna vel aliquet. Phasellus fringilla ante mollis faucibus rutrum. Donec vulputate lacus eu cursus porttitor. Phasellus maximus laoreet metus, eget ultricies neque congue nec. Sed posuere fermentum gravida.

Aliquam quis tempor est. Etiam lorem arcu, pulvinar id mauris eu, pellentesque tincidunt mi. Proin vitae ipsum est. Vestibulum bibendum justo eget metus pharetra lacinia. Suspendisse sed dui id sapien auctor gravida. Suspendisse interdum mi augue, eget mattis quam tincidunt in. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas. Integer id nisi at orci iaculis ultrices a ac ipsum. Morbi tempor libero vel lorem convallis pretium. Nulla facilisi. Aenean a nunc elementum, lobortis quam at, aliquet dui.

Orci varius natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Phasellus ultricies tincidunt sapien ac blandit. Nullam id convallis eros. Fusce fermentum commodo placerat. Maecenas ac arcu blandit, tincidunt massa in, vehicula lacus. Donec sed condimentum ante. Pellentesque feugiat vulputate nunc in consequat. Nam aliquet lectus mollis aliquet aliquam. Duis egestas tempor augue. Nulla dui velit, vehicula eget turpis sed, fermentum mollis augue.

Nam volutpat tellus sem, in maximus dolor tincidunt nec. Praesent eu porta erat. Proin eu volutpat sapien. Donec in elit eu tortor dictum dignissim. Mauris volutpat urna sed ex dictum, eget faucibus lacus pellentesque. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Proin pharetra tristique mollis. Vivamus et pharetra purus. Mauris eu porta libero, nec sagittis dolor. Morbi sed ipsum elementum, pellentesque nisl sed, ullamcorper odio. Vivamus placerat lacus quis mi vehicula, vel laoreet dolor euismod. Integer pellentesque mauris ipsum, a pretium elit facilisis sit amet. Nam id blandit lectus, eget commodo libero.

Vivamus dapibus pulvinar nibh non pulvinar. Pellentesque dui diam, posuere quis diam eu, imperdiet pretium tortor. Interdum et malesuada fames ac ante ipsum primis in faucibus. Maecenas ac nisl nec tortor sollicitudin lobortis ut sit amet sem. Vestibulum ullamcorper iaculis fringilla. Quisque ipsum magna, maximus eget ligula nec, pulvinar pretium nisi. Vestibulum ante ipsum primis in faucibus orci luctus et ultrices posuere cubilia Curae; Aliquam rhoncus ipsum ac tristique aliquet. Morbi auctor volutpat gravida. Nam eget felis vel augue tempor rhoncus in id libero. Donec lorem dui, ornare sit amet diam a, tempor volutpat ante.

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
    Status1 -> Status2;
    Status2 -> Status3;
    Status1 -> Status3;
}