import { useParams } from "react-router-dom";

function Specs () {
    const { serialNumber } = useParams();

    //serial number checks against all SN, gives a range of possible guitars.
    //more options: fretboard wood, pickguard type, tuners...
    return (
        <>
            <div>{serialNumber}</div>
        </>
    )
}

export default Specs