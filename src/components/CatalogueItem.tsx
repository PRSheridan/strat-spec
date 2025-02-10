import { useNavigate } from "react-router-dom";
import { useGuitar } from "../context/GuitarContext";
import { Guitar } from "../types/Guitar";

interface CatalogueProps {
    item: Guitar;
}

function CatalogueItem({ item }: CatalogueProps) {
    const { setGuitar } = useGuitar();
    const navigate = useNavigate();

    function handleSelectGuitar(guitar: Guitar) {
        setGuitar(guitar);
        navigate(`/specs/${guitar.serial_number}`);
    }

    return (
        <div key={item.id} className="item-card" onClick={() => handleSelectGuitar(item)}>
            <div className="item-details">{item.name}</div>
            <div className="item-details">{item.serial_number}</div>
        </div>
    );
}

export default CatalogueItem;
