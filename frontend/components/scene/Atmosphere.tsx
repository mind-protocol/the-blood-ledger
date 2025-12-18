'use client';

interface AtmosphereProps {
  lines: string[];
}

export function Atmosphere({ lines }: AtmosphereProps) {
  return (
    <div className="px-4 py-3 space-y-1">
      {lines.map((line, index) => (
        <p
          key={index}
          className="text-stone-300 text-sm leading-relaxed font-serif italic"
        >
          {line}
        </p>
      ))}
    </div>
  );
}
