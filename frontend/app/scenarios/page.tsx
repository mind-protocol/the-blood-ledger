'use client';

import { useState, useEffect } from 'react';
import { useRouter } from 'next/navigation';
import { createPlaythrough } from '@/lib/api';

interface Scenario {
  id: string;
  name: string;
  tagline: string;
  tone: string;
  location: string;
  starts_with: string[];
}

const SCENARIOS: Scenario[] = [
  {
    id: 'thornwick_betrayed',
    name: 'The Burned Home',
    tagline: 'Your brother took everything. Aldric stayed.',
    tone: 'Revenge',
    location: 'Thornwick',
    starts_with: [
      'Aldric — your father\'s man, oath-bound',
      'Your father\'s ring',
      'A grievance that won\'t quiet'
    ]
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
      'A sealed letter'
    ]
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
      'The knowledge that Durham will burn'
    ]
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
      'A sword you swore to put down'
    ]
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
      'Orders you haven\'t received yet'
    ]
  }
];

export default function ScenariosPage() {
  const router = useRouter();
  const [selectedId, setSelectedId] = useState<string | null>(null);
  const [playerName, setPlayerName] = useState<string>('');
  const [playerGender, setPlayerGender] = useState<string>('');

  useEffect(() => {
    // Get player info from previous screen
    const name = sessionStorage.getItem('playerName');
    const gender = sessionStorage.getItem('playerGender');

    if (!name || !gender) {
      router.replace('/start');
      return;
    }

    setPlayerName(name);
    setPlayerGender(gender);
  }, [router]);

  const selected = SCENARIOS.find(s => s.id === selectedId);

  const [isCreating, setIsCreating] = useState(false);

  const handleBegin = async () => {
    if (!selectedId || isCreating) return;

    setIsCreating(true);

    try {
      const data = await createPlaythrough(selectedId, playerName, playerGender);

      // Store playthrough ID for main game
      sessionStorage.setItem('playthroughId', data.playthrough_id);
      sessionStorage.setItem('scenarioId', selectedId);

      // Redirect to main game - scene.json has opening beats
      router.push(`/playthroughs/${data.playthrough_id}`);
    } catch (error) {
      console.error('Failed to create playthrough:', error);
      setIsCreating(false);
    }
  };

  return (
    <div className="min-h-screen bg-stone-950 flex flex-col">
      {/* Noise overlay */}
      <div
        className="fixed inset-0 opacity-[0.03] pointer-events-none"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%' height='100%' filter='url(%23noise)'/%3E%3C/svg%3E")`,
        }}
      />

      {/* Header */}
      <div className="p-8 text-center border-b border-stone-800">
        <p className="text-stone-600 text-sm mb-1">
          {playerName} • {playerGender === 'female' ? 'Woman' : 'Man'}
        </p>
        <h1 className="text-stone-400 text-lg tracking-wide">Where does your story begin?</h1>
      </div>

      <div className="flex-1 flex">
        {/* Scenario list */}
        <div className="w-1/2 border-r border-stone-800 overflow-y-auto">
          {SCENARIOS.map((scenario) => (
            <button
              key={scenario.id}
              onClick={() => setSelectedId(scenario.id)}
              className={`w-full text-left p-6 border-b border-stone-800 transition-colors ${
                selectedId === scenario.id
                  ? 'bg-stone-900'
                  : 'hover:bg-stone-900/50'
              }`}
            >
              <div className="flex items-start justify-between gap-4">
                <div>
                  <h2 className={`text-lg mb-1 ${
                    selectedId === scenario.id ? 'text-stone-200' : 'text-stone-400'
                  }`}>
                    {scenario.location}
                  </h2>
                  <p className="text-stone-500 text-sm">{scenario.name}</p>
                </div>
                <span className={`text-xs px-2 py-1 rounded ${
                  selectedId === scenario.id
                    ? 'bg-stone-700 text-stone-300'
                    : 'bg-stone-800 text-stone-500'
                }`}>
                  {scenario.tone}
                </span>
              </div>
            </button>
          ))}
        </div>

        {/* Selected scenario details */}
        <div className="w-1/2 p-8 flex flex-col">
          {selected ? (
            <>
              <div className="flex-1">
                <h2 className="text-stone-300 text-xl mb-2">{selected.location}</h2>
                <p className="text-stone-500 mb-1">{selected.name}</p>
                <p className="text-stone-400 text-lg italic mb-8">{selected.tagline}</p>

                <div className="mb-8">
                  <h3 className="text-stone-500 text-sm uppercase tracking-wide mb-3">You begin with</h3>
                  <ul className="space-y-2">
                    {selected.starts_with.map((item, i) => (
                      <li key={i} className="text-stone-400 flex items-start gap-2">
                        <span className="text-stone-600">•</span>
                        {item}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <button
                onClick={handleBegin}
                className="w-full py-4 border border-stone-600 text-stone-300 rounded hover:bg-stone-800 hover:border-stone-500 transition-colors"
              >
                BEGIN HERE
              </button>
            </>
          ) : (
            <div className="flex-1 flex items-center justify-center">
              <p className="text-stone-600 italic">Select a starting point</p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
