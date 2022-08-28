import { Card, CardContent, Grid, Typography } from "@mui/material";
import NumberFormat from 'react-number-format';

export const CountCard = (props) => (
  <Card sx={{ height: "100%"}} {...props}>
    <CardContent>
      <Grid container spacing={3} sx={{ justifyContent: "space-between" }}>
        <Grid item>
          <Typography color="textSecondary" gutterBottom variant="overline">
            {props.title}
          </Typography>
          <Typography color="textPrimary" variant="h4">
          <NumberFormat value={props.value} displayType={'text'} thousandSeparator={true} />
          </Typography>
        </Grid>
      </Grid>
    </CardContent>
  </Card>
);
export default CountCard;
