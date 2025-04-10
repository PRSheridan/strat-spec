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
  relic: string;
  other_controls?: any;
  hardware_finish: HardwareFinish[];
  plastic_color: PlasticColor[];
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
  country?: string;
  description?: string;
  scale_length?: number;
  weight?: string;
  relic: string;
  other_controls?: string;
  hardware_finish?: HardwareFinish;
  plastic_color?: PlasticColor;
  pickup_configuration: string;
  modified?: boolean;
  modifications?: string;
  created_at: string;
  updated_at: string;

  pickups: GuitarPickup[];
  model?: Model | null;
  owner: User;
  images: Image[];

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
  type: string;
  magnet?: string;
  active?: boolean;
  noiseless?: boolean;
  cover?: string;
}

export interface Body {
  id: number;
  wood?: string;
  contour?: string;
  routing?: string;
  chambering?: boolean;
  binding: boolean;
  finish: string;
  color: string;
}

export interface Neck {
  id: number;
  wood?: string;
  finish: string;
  shape?: string;
  truss_rod: string;
}

export interface Headstock {
  id: number;
  shape?: string;
  decal_style?: string;
  reverse: boolean;
}

export interface Fretboard {
  id: number;
  material?: string;
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
  spacing?: string;
}

export interface Bridge {
  id: number;
  model?: string;
  screws: number;
  spacing?: number;
  tremolo: boolean;
}

export interface Saddles {
  id: number;
  style?: string;
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
  style: string;
  bolts: number;
  details?: string;
}

export interface Pickguard {
  id: number;
  ply_count?: number;
  screws: number;
  color: string;
}

export interface HardwareFinish {
  id: number;
  label: string;
}

export interface PlasticColor {
  id: number;
  label: string;
}
