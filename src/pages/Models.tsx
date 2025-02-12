import { useState, useEffect } from "react"
import GuitarCard from "../components/GuitarCard"
import { Model } from "../types"

function Models() {
    const [models, setModels] = useState<Model[]>([])

    useEffect(() => {
        fetch("/api/models")
            .then((response) => response.json())
            .then((data: Model[]) => {
                setModels(data)
            })
            .catch((error) => console.error("Error fetching guitars:", error))
    }, [])

    return (
        <>
            <div>User Submissions</div>
            {models.map((item) => (
                <GuitarCard key={item.id} item={item} />
            ))}
        </>
    );
}

export default Models