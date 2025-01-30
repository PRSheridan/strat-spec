export interface User {
    id: number;
    username: string;
    email: string;
    role: string;
}

export interface Body {
    id: number;
    body_type: string;
    body_wood: string;
    color: string;
    finish_type: string;
}

export interface Neck {
    id: number;
    shape: string;
    wood: string;
    finish: string;
}

export interface Fretboard {
    id: number;
    material: string;
    radius: string;
    frets: string;
}

export interface Model {
    id: number;
    name: string;
    years: string;
    body: Body;
    neck: Neck;
    fretboard: Fretboard;
    nut: { id: number; material: string };
    truss_rod: { id: number; type: string; location: string };
    pickups: { id: number; pickup_configuration: string };
    bridge: { id: number; bridge_type: string };
    tuning_machine: { id: number; machine_type: string };
    string_tree: { id: number; tree_type: string };
    pickguard: { id: number; layers: string; color: string };
    control_knob: { id: number; style: string };
    switch_tip: { id: number; style: string };
    neck_plate: { id: number; style: string };
}

export interface Guitar {
    id: number;
    name: string;
    description: string;
    serial_number: string;
    user: User;
    model: Model;
    images: string[];
}
