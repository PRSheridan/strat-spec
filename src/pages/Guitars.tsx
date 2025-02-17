import { useState, useEffect } from 'react'
import GuitarCard from '../components/GuitarCard'
import { UserGuitar } from '../types'

function Guitars() {
    const [catalogue, setCatalogue] = useState<UserGuitar[]>([])
    const [viewMode, setViewMode] = useState<'compact' | 'detailed'>('detailed')

    useEffect(() => {
        fetch('/api/guitars')
            .then(response => response.json())
            .then((data: UserGuitar[]) => setCatalogue(data))
            .catch(error => console.error('Error fetching guitars:', error))
    }, [])

    return (
        <>
            <div className="header-container">
                <div className="page-name">User Submitted Stratocasters</div>
                <button className="toggle-view-btn" onClick={() => setViewMode(viewMode === 'compact' ? 'detailed' : 'compact')}>
                    {viewMode === 'compact' ? 'Switch to Detailed View' : 'Switch to Compact View'}
                </button>
            </div>

            <div className="list-container">
                {catalogue.map(item => (
                    <GuitarCard key={item.id} item={item} viewMode={viewMode} />
                ))}
            </div>
        </>
    )
}

export default Guitars

