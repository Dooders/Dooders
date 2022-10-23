import * as React from "react";
import { Grid, Card } from "@mui/material/";
import Typography from "@mui/material/Typography";
import CardContent from "@mui/material/CardContent";
// import { useCubeQuery }  from '@cubejs-client/react';

const TopRow = () => {
  // const { data, loading, error } = useQuery(GET_TOP_ROW_DATA);
  // if (loading) return <Loading />;
  // if (error) return <Error />;
  return (
    <Grid item xs={12}>
      <Grid container justifyContent="center" spacing={2}>
        {[0, 1, 2].map((value) => (
          <Grid key={value} item>
            <Card
              variant="outlined"
              sx={{
                height: 130,
                width: 100,
                backgroundColor: (theme) =>
                  theme.palette.mode === "dark" ? "#1A2027" : "#fff",
              }}
            >
              <CardContent>
                <Typography
                  sx={{ fontSize: 14 }}
                  color="text.secondary"
                  gutterBottom
                >
                  Card Title
                </Typography>
                <h1>{value}</h1>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Grid>
  );
};

export default TopRow;
