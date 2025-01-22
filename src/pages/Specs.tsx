import { useParams } from "react-router-dom";

function Specs () {
    const { serialNumber } = useParams();
    return (
        <>
            <div>{serialNumber}</div>
        </>
    )
}

export default Specs