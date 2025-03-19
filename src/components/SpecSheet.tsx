import { Model, UserGuitar } from "../types";

interface SpecSheetProps {
    item: Model | UserGuitar;
    type: "model" | "userGuitar";
}

function SpecSheet({ item, type }: SpecSheetProps) {
    if (type === "model") {
        const model = item as Model;
        return (
            <>
            <h1>{model.model_name}</h1>
            <div className="spec-sheet-header">
                <p>Country: {model.country}</p>
                <p>Year Range: {model.year_range}</p>
            </div>
            <div className="spec-sheet-about">
                {model.description}
            </div>
            <div className="spec-sheet">
                <div className="spec-sheet-sub">
                    <h2>Electronics</h2>
                    <p>Pickup Configuration: {model.pickup_configuration.length > 0 ? model.pickup_configuration.join(", ") : "None"}</p>
                    <p>Other Controls: {model.other_controls?.length > 0 ? model.other_controls.join(", ") : "None"}</p>
                </div>

                <div className="spec-sheet-sub">
                    <h2>Finish & Hardware</h2>
                    <p>Hardware Finish: {model.hardware_finish.length > 0 ? model.hardware_finish.join(", ") : "None"}</p>
                    <p>Relic: {model.relic ?? "None"}</p>
                </div>

                <div className="spec-sheet-sub">
                    <h2>Body</h2>
                    <p>Wood: {model.bodies?.map((body) => body.wood || "Unknown").join(", ") || "N/A"}</p>
                    <p>Finish: {model.bodies?.map((body) => body.finish || "Unknown").join(", ") || "N/A"}</p>
                    <p>Color: {model.bodies?.map((body) => body.color || "Unknown").join(", ") || "N/A"}</p>
                </div>

                <div className="spec-sheet-sub">
                    <h2>Neck & Fretboard</h2>
                    <p>Neck Wood: {model.neck.wood ?? "N/A"}</p>
                    <p>Neck Shape: {model.neck.shape ?? "N/A"}</p>
                    <p>Fretboard Material: {model.fretboards?.map((fb) => fb.material || "Unknown").join(", ") || "N/A"}</p>
                    <p>Fretboard Radius: {model.fretboards?.map((fb) => fb.radius || "Unknown").join(", ") || "N/A"}</p>
                </div>

                <div className="spec-sheet-sub">
                    <h2>Bridge & Pickguard</h2>
                    <p>Bridge Model: {model.bridge.model ?? "N/A"}</p>
                    <p>Bridge Spacing: {model.bridge.spacing ? `${model.bridge.spacing} mm` : "N/A"}</p>
                    <p>Pickguard Ply Count: {model.pickguards?.map((pg) => pg.ply_count || "Unknown").join(", ") || "N/A"}</p>
                    <p>Pickguard Color: {model.pickguards?.map((pg) => pg.color || "Unknown").join(", ") || "N/A"}</p>
                </div>
            </div>
            <div>pictures here</div>
            </>
        );
    } else {
        const guitar = item as UserGuitar;
        return (
            <>
            <h1>{guitar.name}</h1>
            <div className="spec-sheet-header">
                <p>Serial Number: {guitar.serial_number}</p>
                <p>Owner: {guitar.owner.username}</p>
                <p>Country: {guitar.country}</p>
                <p>Year: {guitar.year ?? "N/A"}</p>
            </div>
            <div className="spec-sheet-about">
                {guitar.description}
            </div>
            <div className="spec-sheet">
                <div className="spec-sheet-sub">
                    <h2>Ownership & Customization</h2>
                    <p>Serial Number Location: {guitar.serial_number_location}</p>
                    <p>Weight: {guitar.weight ?? "N/A"} lbs</p>
                    <p>Modified: {guitar.modified ? "Yes" : "No"}</p>
                    {guitar.modified && <p>Modifications: {guitar.modifications ?? "N/A"}</p>}
                    {guitar.model && <p>Based on Model: {guitar.model.model_name}</p>}
                </div>

                <div className="spec-sheet-sub">
                    <h2>Electronics</h2>
                    <p>Pickup Configuration: {guitar.pickup_configuration}</p>
                    <p>Other Controls: {guitar.other_controls ?? "None"}</p>
                </div>

                <div className="spec-sheet-sub">
                    <h2>Finish & Hardware</h2>
                    <p>Hardware Finish: {guitar.hardware_finish ?? "N/A"}</p>
                    <p>Relic: {guitar.relic ?? "None"}</p>
                </div>

                <div className="spec-sheet-sub">
                    <h2>Body</h2>
                    <p>Wood: {guitar.body.wood ?? "N/A"}</p>
                    <p>Finish: {guitar.body.finish ?? "N/A"}</p>
                    <p>Color: {guitar.body.color ?? "N/A"}</p>
                </div>

                <div className="spec-sheet-sub">
                    <h2>Neck & Fretboard</h2>
                    <p>Neck Wood: {guitar.neck.wood ?? "N/A"}</p>
                    <p>Neck Shape: {guitar.neck.shape ?? "N/A"}</p>
                    <p>Fretboard Material: {guitar.fretboard.material ?? "N/A"}</p>
                    <p>Fretboard Radius: {guitar.fretboard.radius ?? "N/A"} inches</p>
                </div>

                <div className="spec-sheet-sub">
                    <h2>Bridge & Pickguard</h2>
                    <p>Bridge Model: {guitar.bridge.model ?? "N/A"}</p>
                    <p>Bridge Spacing: {guitar.bridge.spacing ? `${guitar.bridge.spacing} mm` : "N/A"}</p>
                    <p>Pickguard Ply Count: {guitar.pickguard.ply_count ?? "N/A"}</p>
                    <p>Pickguard Color: {guitar.pickguard.color ?? "N/A"}</p>
                </div>
            </div>
            <div>pictures here</div>
            </>
        );
    }
}

export default SpecSheet;

