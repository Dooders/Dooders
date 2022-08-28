import { Grid, Container, TextField } from "@mui/material/";
import ExperimentButton from "./ExperimentButton";
import ApiButton from "./ApiButton";
import { useState } from "react";

const Toolbar = ({ socket, setter }) => {
  const [parameters, setParameters] = useState({ steps: 100, agents: 10 });

  const handleChange = (event) => {
    setParameters({ ...parameters, [event.target.name]: parseInt(event.target.value) });
  };

  return (
    <Container>
      <Grid container spacing={1}>
        <Grid item xs={0}>
          <ExperimentButton
            socket={socket}
            parameters={parameters}
            setter={setter}
          />
        </Grid>
        <Grid item xs={0}>
          <ApiButton name={"Stop"} />
        </Grid>
        <Grid item xs={0}>
          <ApiButton name={"Reset"} />
        </Grid>
        <Grid item xs={0}>
          <TextField
            id="steps"
            variant="outlined"
            size='small'
            name="steps"
            label="Steps"
            value={parameters.steps}
            onChange={handleChange}
          />
        </Grid>
        <Grid item xs={0}>
          <TextField
            id="agents"
            variant="outlined"
            size='small'
            name="agents"
            label="Agents"
            value={parameters.agents}
            onChange={handleChange}
          />
        </Grid>
      </Grid>
    </Container>
  );
};

export default Toolbar;
