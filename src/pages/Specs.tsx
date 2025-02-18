import { useParams } from "react-router-dom";
import { useEffect, useState } from "react";
import { useItem } from "../context/ItemContext";
import { Model, UserGuitar } from "../types";

function Specs() {
    const [fetchedItem, setFetchedItem] = useState<Model | UserGuitar | null>(null);
    const { model_name, serialNumber } = useParams();
    const { item } = useItem();

    useEffect(() => {
        if (!item && (model_name || serialNumber)) {
            fetch(`/api/guitar/${model_name || serialNumber}`)
                .then(response => response.json())
                .then((data: Model | UserGuitar) => setFetchedItem(data))
                .catch(error => console.error("Error fetching item:", error));
        }
    }, [item, model_name, serialNumber]);

    const displayItem = item || fetchedItem;

    return (
        <>
            {displayItem ? (
                <div id="guitar-specs">
                    {"serial_number" in displayItem ? (
                        <>
                            <h1>{displayItem.serial_number}</h1>
                            <p>Model: {displayItem.model ? displayItem.model.model_name : "Unknown"}</p>
                        </>
                    ) : (
                        <>
                            <h1>{displayItem.model_name}</h1>
                            <p>Official Model</p>
                        </>
                    )}
                </div>
            ) : (
                <p>Loading...</p>
            )}
        </>
    );
}

export default Specs;
