import { Button } from "@mui/material/";

const ExperimentButton = ({ socket, parameters, setter }) => {
  const handleClick = () => {
    // reset sessionData array
    setter([]);
    // send experiment parameters to server
    socket.current.send(JSON.stringify(parameters));
  }


  return (
    <Button
      variant="contained"
      color="secondary"
      onClick={handleClick}
      
    >
      Start
    </Button>
  );
};

export default ExperimentButton;


