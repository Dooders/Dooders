# Data Dictionaries

## Dooder Dataframe

|         Name          | Type  | Description                                                 |
| :-------------------: | :---: | ----------------------------------------------------------- |
|          id           |  str  | Unique Dooder identifier                                    |
|        number         |  int  | Order number Dooder was created in                          |
|       position        | tuple | Last position                                               |
|        hunger         |  int  | number of cycles without consuming energy                   |
|          age          |  int  | number of cycles since birth                                |
|      generation       |  int  | generation number of the Dooder                             |
|         birth         |  int  | cycle number the Dooder was born                            |
|         death         |  int  | cycle number the Dooder died                                |
|        status         |  str  | Final Dooder status                                         |
|  reproduction_count   |  int  | number of times the Dooder reproduced                       |
|      move_count       |  int  | number of times the Dooder moved                            |
|    energy_consumed    |  int  | total energy consumed by the Dooder                         |
|          tag          |  str  | Dooder tag assigned by user                                 |
|    encoded_weights    | dict  | Dooder neural network weights                               |
|   inference_record    | dict  | Dooder inference record                                     |
|     age_category      |  str  | Dooder age category (Failed Early, Failed, Succeeded)       |
|    first_encoding     | tuple | First gene encoding                                         |
|     last_encoding     | tuple | Final gene encoding                                         |
|  average_opportunity  | float | Average opportunity of all opportunities Dooder encountered |
| opportunity_variation | float | Variation of opportunities Dooder encountered               |
| avg_first_opportunity | float | Average opportunity of first opportunity Dooder encountered |
| avg_last_opportunity  | float | Average opportunity of last opportunity Dooder encountered  |
|   near_death_count    |  int  | Number of times Dooder was near death                       |
|    near_death_rate    | float | Rate of near death experiences                              |
| starting_probability  | float | Starting probability Dooder was going to live               |
