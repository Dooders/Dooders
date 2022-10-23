import { Box, Container, Grid } from "@mui/material";
import { CountCard } from "../CountCard/CountCard";
import { DashboardLayout } from "./dashboard-layout";
import TopRow from "./TopRow";
 
const Dashboard = ({ data }) => {
  const cycleCount = data.CycleCount || 0;
  const dooderCount = data.DooderCount || 0;
  const energyCount = data.EnergyCount || 0;

  // console.log(dooderCount);

  return (
    <>
      <Box
        component="main"
        sx={{
          flexGrow: 1,
          py: 8,
        }}
      >
        <Container maxWidth={false}>
          <Grid container spacing={3}>
            <Grid item lg={3} sm={6} xl={3} xs={12}>
              <CountCard value={cycleCount} title={"CYCLE COUNT"} />
            </Grid>
            <Grid item lg={3} sm={6} xl={3} xs={12}>
              <CountCard value={dooderCount} title={"DOODER COUNT"} />
            </Grid>
            <Grid item lg={3} sm={6} xl={3} xs={12}>
              <CountCard value={energyCount} title={"ENERGY COUNT"} />
            </Grid>
          </Grid>
        </Container>
      </Box>
      <TopRow />
    </>
  );
};

Dashboard.getLayout = (page) => <DashboardLayout>{page}</DashboardLayout>;

export default Dashboard;
