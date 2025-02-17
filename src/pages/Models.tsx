import { useState, useEffect } from "react"
import GuitarCard from "../components/GuitarCard"
import { Model } from "../types"

function Models() {
    const [models, setModels] = useState<Model[]>([])
    const [viewMode, setViewMode] = useState<'compact' | 'detailed'>('detailed')

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
            <div className="header-container">
                <div className="page-name">Stratocaster Models</div>
                <button className="toggle-view-btn" onClick={() => setViewMode(viewMode === 'compact' ? 'detailed' : 'compact')}>
                    {viewMode === 'compact' ? 'Switch to Detailed View' : 'Switch to Compact View'}
                </button>
            </div>

            <div className="list-container">
                {models.map((item) => (
                    <GuitarCard key={item.id} item={item} viewMode={viewMode} />
                ))}
            </div>
        </>
    );
}

export default Models