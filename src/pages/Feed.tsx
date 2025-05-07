import GuitarForm from "../components/forms/guitarForm/GuitarForm"
import { useEffect } from "react";

function Feed () {
//testing api calls
  useEffect(() => {
    fetch('/api/pickup_covers')
      .then(response => response.json())
      .then((data: any)  => console.log(data))
  }, []);

    return (
        <div className="guitar-form">
            <div>Guitar Build</div>
            <GuitarForm />
        </div>
    )
}

export default Feed