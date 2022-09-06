import { Button } from "@mui/material/";

const ApiButton = ({ name }) => {
  return (
    <Button
      variant="contained"
      color="secondary"
      onClick={() => {
        fetch(`http://localhost:8080/${name.toLowerCase()}`)
          .then((res) => res.json())
          .then((data) => console.log(data))
          .catch((err) => console.log(err));
      }}
    >
      {name}
    </Button>
  );
};

export default ApiButton;
