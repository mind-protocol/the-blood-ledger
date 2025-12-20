// DOCS: docs/frontend/PATTERNS_Presentation_Layer.md

'use client';

import { useState } from 'react';
import { useRouter } from 'next/navigation';

// Saxon name lists for random generation
const SAXON_NAMES_MALE = [
  'Wulfric', 'Aldric', 'Godwin', 'Leofric', 'Aethelred', 'Osric', 'Eadric',
  'Siward', 'Morcar', 'Tostig', 'Harold', 'Beorn', 'Aelfric', 'Ordgar',
  'Wulfstan', 'Cuthbert', 'Dunstan', 'Aethelwulf', 'Eadmund', 'Oswulf'
];

const SAXON_NAMES_FEMALE = [
  'Aelfgifu', 'Eadgyth', 'Godgifu', 'Hild', 'Wulfhild', 'Aethelflaed',
  'Cwenburh', 'Ealdgyth', 'Leofrun', 'Mildred', 'Osgifu', 'Wynflaed',
  'Aelswith', 'Cyneburh', 'Eadburh', 'Frithugyth', 'Gunnhild', 'Sigrid'
];

export default function StartPage() {
  const router = useRouter();
  const [gender, setGender] = useState<'male' | 'female' | null>(null);
  const [name, setName] = useState('');

  const canBegin = gender !== null && name.trim().length > 0;

  const rollRandomName = () => {
    const names = gender === 'female' ? SAXON_NAMES_FEMALE : SAXON_NAMES_MALE;
    const randomName = names[Math.floor(Math.random() * names.length)];
    setName(randomName);
  };

  const handleBegin = () => {
    if (!canBegin) return;

    // Store character info in sessionStorage for the opening
    sessionStorage.setItem('playerGender', gender!);
    sessionStorage.setItem('playerName', name.trim());

    router.push('/scenarios');
  };

  return (
    <div className="min-h-screen bg-stone-950 flex items-center justify-center p-8">
      {/* Parchment texture overlay */}
      <div
        className="fixed inset-0 opacity-[0.03] pointer-events-none"
        style={{
          backgroundImage: `url("data:image/svg+xml,%3Csvg viewBox='0 0 200 200' xmlns='http://www.w3.org/2000/svg'%3E%3Cfilter id='noise'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.65' numOctaves='3' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='100%' height='100%' filter='url(%23noise)'/%3E%3C/svg%3E")`,
        }}
      />

      <div className="max-w-xl w-full text-center relative">
        {/* Title */}
        <div className="mb-12">
          <div className="text-stone-600 tracking-[0.5em] text-sm mb-2">═══════════════════════════</div>
          <h1 className="text-stone-300 text-2xl tracking-[0.3em] font-light">THE BLOOD LEDGER</h1>
          <div className="text-stone-600 tracking-[0.5em] text-sm mt-2">═══════════════════════════</div>
        </div>

        {/* Intro text */}
        <div className="text-stone-500 text-base leading-relaxed mb-12 max-w-md mx-auto text-left space-y-4">
          <p className="text-stone-400">England, 1067. One year after the battle of Hastings.</p>

          <p>
            Most games give you a story. This one remembers yours.
            The people here don&apos;t forget what you did for them — or to them.
          </p>

          <p>
            You begin with nothing. You rise through people — oaths sworn,
            debts called in, loyalties earned or broken. The world won&apos;t wait
            while you decide. If one day you become lord, you&apos;ll remember
            every step. And so will they.
          </p>

          <p className="text-stone-400">
            The ledger is open. What you write cannot be unwritten.
          </p>
        </div>

        {/* Gender selection */}
        <div className="mb-6">
          <div className="inline-flex border border-stone-700 rounded">
            <label className={`px-6 py-3 cursor-pointer transition-colors ${
              gender === 'male'
                ? 'bg-stone-800 text-stone-300'
                : 'text-stone-500 hover:text-stone-400'
            }`}>
              <input
                type="radio"
                name="gender"
                value="male"
                checked={gender === 'male'}
                onChange={() => setGender('male')}
                className="sr-only"
              />
              <span className="flex items-center gap-2">
                <span className={`w-3 h-3 rounded-full border ${
                  gender === 'male'
                    ? 'border-stone-400 bg-stone-400'
                    : 'border-stone-600'
                }`} />
                Man
              </span>
            </label>
            <label className={`px-6 py-3 cursor-pointer transition-colors border-l border-stone-700 ${
              gender === 'female'
                ? 'bg-stone-800 text-stone-300'
                : 'text-stone-500 hover:text-stone-400'
            }`}>
              <input
                type="radio"
                name="gender"
                value="female"
                checked={gender === 'female'}
                onChange={() => setGender('female')}
                className="sr-only"
              />
              <span className="flex items-center gap-2">
                <span className={`w-3 h-3 rounded-full border ${
                  gender === 'female'
                    ? 'border-stone-400 bg-stone-400'
                    : 'border-stone-600'
                }`} />
                Woman
              </span>
            </label>
          </div>
        </div>

        {/* Name input */}
        <div className="mb-10">
          <div className="inline-flex border border-stone-700 rounded overflow-hidden">
            <input
              type="text"
              value={name}
              onChange={(e) => setName(e.target.value)}
              placeholder="Your name"
              className="bg-transparent text-stone-300 placeholder-stone-600 px-4 py-3 w-48 outline-none text-center"
            />
            <button
              onClick={rollRandomName}
              disabled={gender === null}
              className={`px-4 py-3 border-l border-stone-700 transition-colors ${
                gender === null
                  ? 'text-stone-700 cursor-not-allowed'
                  : 'text-stone-500 hover:text-stone-300 hover:bg-stone-800'
              }`}
              title="Random Saxon name"
            >
              ⚄
            </button>
          </div>
        </div>

        {/* Begin button */}
        <button
          onClick={handleBegin}
          disabled={!canBegin}
          className={`px-8 py-3 border rounded transition-all ${
            canBegin
              ? 'border-stone-600 text-stone-300 hover:bg-stone-800 hover:border-stone-500'
              : 'border-stone-800 text-stone-700 cursor-not-allowed'
          }`}
        >
          BEGIN
        </button>
      </div>
    </div>
  );
}
