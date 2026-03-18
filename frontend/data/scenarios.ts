export interface Scenario {
  id: string;
  name: string;
  tagline: string;
  tone: string;
  location: string;
  starts_with: string[];
}

export const SCENARIOS: Scenario[] = [
  {
    id: 'thornwick_betrayed',
    name: 'The Burned Home',
    tagline: 'Your brother took everything. Aldric stayed.',
    tone: 'Revenge',
    location: 'Thornwick',
    starts_with: [
      'Aldric — your father\'s man, oath-bound',
      'Your father\'s ring',
      'A grievance that won\'t quiet',
    ],
  },
  {
    id: 'york_anonymous',
    name: 'The Anonymous',
    tagline: 'No one knows your name. That\'s how you\'ll survive.',
    tone: 'Intrigue',
    location: 'York',
    starts_with: [
      'A false name',
      'Sigewulf — a thief who knows too much',
      'A sealed letter',
    ],
  },
  {
    id: 'durham_burning',
    name: 'The Witness',
    tagline: 'Cumin\'s cruelty builds a fire. You\'re here to watch it burn.',
    tone: 'Revenge',
    location: 'Durham',
    starts_with: [
      'A grudge against Robert Cumin',
      'Ligulf — a thegn who lost everything',
      'The knowledge that Durham will burn',
    ],
  },
  {
    id: 'whitby_sanctuary',
    name: 'The Penitent',
    tagline: 'The Church offers sanctuary. But God remembers.',
    tone: 'Redemption',
    location: 'Whitby Abbey',
    starts_with: [
      'Sanctuary within these walls',
      'Reinfrid — a Norman who understands',
      'A sword you swore to put down',
    ],
  },
  {
    id: 'norman_service',
    name: 'The Turncoat',
    tagline: 'You serve the enemy. They don\'t know what you are.',
    tone: 'Infiltration',
    location: 'York Castle',
    starts_with: [
      'A position in Malet\'s household',
      'Cynewise — a fellow spy',
      'Orders you haven\'t received yet',
    ],
  },
];
