import { useNavigate } from "react-router-dom"

interface CatalogueProps {
    item: {
        id: number;
        name: string;
        serial_number: string;
    };
}

function CatalogueItem ({ item }: CatalogueProps) {
    const navigate = useNavigate()
    return (
        <div key={item.id} className="item-card"
            onClick={() => navigate(`/specs/${item.serial_number}`)}>
            <div className="item-details">{item.name}</div>
            <div className="item-details">{item.serial_number}</div>
        </div>
    )
}

export default CatalogueItem