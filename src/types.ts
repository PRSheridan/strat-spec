export interface User {
    id: number;
    username: string;
    email: string;
    role: 'client' | 'admin';
    is_active: boolean;
    last_login?: string;
    created_at: string;
    updated_at: string;
    user_guitars: UserGuitar[];
}

export interface Image {
    id: number;
    file_name: string;
    caption?: string;
    file_path: string;
    created_at: string;
    updated_at: string;
}

export interface Model {
    id: number;
    brand: string;
    model_name: string;
    year_range: string;
    country: string;
    description?: string;
    scale_length: number;
    relic: 'None' | 'Light' | 'Medium' | 'Heavy' | 'Custom';
    other_controls?: any;
    hardware_finish: string[];
    pickup_configuration: string[];
    created_at: string;
    updated_at: string;
    
    pickups: GuitarPickup[];
    bodies: Body[];
    fretboards: Fretboard[];
    pickguards: Pickguard[];
    switches: Switch[];
    controls: Controls[];
    
    neck: Neck;
    headstock: Headstock;
    nut: Nut;
    frets: Frets;
    inlays: Inlays;
    bridge: Bridge;
    saddles: Saddles;
    tuning_machine: TuningMachine;
    string_tree: StringTree;
    neck_plate: NeckPlate;
    
    user_guitars: UserGuitar[];
}

export interface UserGuitar {
    id: number;
    brand: string;
    name: string;
    serial_number: string;
    serial_number_location: string;
    year?: number;
    country: string; //optional
    description?: string;
    scale_length?: number;
    weight?: string;
    relic: string; // N/A, light, medium, heavy
    other_controls?: string;
    hardware_finish?: string;
    pickup_configuration: string;
    modified: boolean; //optional
    modifications?: string;
    created_at: string;
    updated_at: string;
    
    pickups: GuitarPickup[]; //optional
    model?: Model | null;
    owner: User;
    images: Image[]; //optional
    
    body: Body;
    neck: Neck;
    headstock: Headstock;
    fretboard: Fretboard;
    nut: Nut;
    frets: Frets;
    inlays: Inlays;
    bridge: Bridge;
    saddles: Saddles;
    switch: Switch;
    controls: Controls;
    tuning_machine: TuningMachine;
    string_tree: StringTree;
    neck_plate: NeckPlate;
    pickguard: Pickguard;
}

export interface GuitarPickup {
    id: number;
    brand?: string;
    model?: string;
    position: string[];
    type: string; //Humbucker, Single-coil, P-90, Filtertron, Piezo
    magnet?: string;
    active?: boolean; 
    noiseless?: boolean;
    cover?: string;
}

export interface Body {
    id: number;
    wood?: string;
    contour?: string; //N/A, 
    routing?: string;
    chambering?: boolean;
    binding: boolean;
    finish: string;
    color: string;
}

export interface Neck {
    id: number;
    wood?: string;
    finish: 'Gloss' | 'Satin' | 'Natural';
    shape?: string;
    truss_rod?: 'Modern' | 'Vintage';  //required
}

export interface Headstock {
    id: number;
    shape?: string;
    decal_style?: string;
    reverse: boolean;
}

export interface Fretboard {
    id: number;
    material: string; //optional
    radius?: string;
    fret_count: number;
    binding: boolean;
    scalloped: boolean;
}

export interface Frets {
    id: number;
    material?: string;
    size?: string;
}

export interface Nut {
    id: number;
    width?: string;
    material?: string;
    locking: boolean;
}

export interface Inlays {
    id: number;
    shape?: string;
    material?: string;
    spacing?: string; //narrow wide
}

export interface Bridge {
    id: number;
    model?: string;
    screws: number; //2 4 6
    spacing?: number;
    tremolo: boolean;
}

export interface Saddles {
    id: number;
    style: string; //optional
    material?: string;
}

export interface Switch {
    id: number;
    positions: number;
    color: string;
}

export interface Controls {
    id: number;
    configuration: string;
    color: string;
}

export interface TuningMachine {
    id: number;
    model?: string;
    locking: boolean;
}

export interface StringTree {
    id: number;
    model?: string;
    count: number;
}

export interface NeckPlate {
    id: number;
    style: 'Vintage' | 'Contour';
    bolts: 3 | 4 | 5 | 6; //just 3 or 4
    details?: string;
}

export interface Pickguard {
    id: number;
    ply_count?: 1 | 2 | 3 | 4 | 5;
    screws: number;
    color: string;
}
