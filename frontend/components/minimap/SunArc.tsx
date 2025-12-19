'use client';

// DOCS: docs/infrastructure/tempo/ALGORITHM_Tempo_Controller.md (Future UI: Minimap + Sun Arc)

interface SunArcProps {
  /** Current world tick (1 tick = 5 minutes, 288 ticks/day) */
  tick: number;
  /** Whether time is advancing fast (2x/3x) */
  isFastForward?: boolean;
}

const TICKS_PER_DAY = 288; // 24 hours * 60 minutes / 5 minutes per tick

/**
 * Sun arc display showing time of day.
 *
 * The sun travels along a semicircular arc from dawn (left) to dusk (right).
 * At night, a moon is shown instead.
 */
export function SunArc({ tick, isFastForward = false }: SunArcProps) {
  // Calculate time of day (0 = midnight, 0.5 = noon)
  const dayProgress = (tick % TICKS_PER_DAY) / TICKS_PER_DAY;

  // Dawn at 6am (0.25), dusk at 6pm (0.75)
  const isDaytime = dayProgress >= 0.25 && dayProgress < 0.75;

  // Sun position on arc (0 = dawn/left, 1 = dusk/right)
  // Map 0.25-0.75 to 0-1
  const sunPosition = isDaytime
    ? (dayProgress - 0.25) / 0.5
    : 0;

  // Calculate x,y on semicircle arc
  // Arc goes from left (0°) to right (180°)
  const angle = Math.PI * (1 - sunPosition); // Reverse so sun goes left to right
  const arcRadius = 40; // % of container
  const centerX = 50;
  const arcY = 85; // Arc baseline near bottom

  const sunX = centerX + arcRadius * Math.cos(angle);
  const sunY = arcY - arcRadius * Math.sin(angle);

  // Get time string for display
  const hours = Math.floor(dayProgress * 24);
  const minutes = Math.floor((dayProgress * 24 * 60) % 60);
  const timeStr = `${hours.toString().padStart(2, '0')}:${minutes.toString().padStart(2, '0')}`;

  // Get period name
  const getPeriod = () => {
    if (dayProgress < 0.25) return 'Night';
    if (dayProgress < 0.33) return 'Dawn';
    if (dayProgress < 0.5) return 'Morning';
    if (dayProgress < 0.54) return 'Noon';
    if (dayProgress < 0.67) return 'Afternoon';
    if (dayProgress < 0.75) return 'Dusk';
    return 'Night';
  };

  return (
    <div className="relative w-full h-12 overflow-hidden">
      {/* Arc path (dashed line showing sun's path) */}
      <svg className="absolute inset-0 w-full h-full" viewBox="0 0 100 50" preserveAspectRatio="xMidYMax meet">
        {/* Arc baseline markers */}
        <circle cx="10" cy="42" r="1.5" fill="rgba(217, 119, 6, 0.3)" /> {/* Dawn marker */}
        <circle cx="90" cy="42" r="1.5" fill="rgba(217, 119, 6, 0.3)" /> {/* Dusk marker */}

        {/* Arc path */}
        <path
          d="M 10 42 Q 50 -5 90 42"
          fill="none"
          stroke="rgba(217, 119, 6, 0.15)"
          strokeWidth="0.5"
          strokeDasharray="2,2"
        />

        {/* Sun or Moon */}
        {isDaytime ? (
          <g className={isFastForward ? 'animate-pulse' : ''}>
            {/* Sun glow */}
            <circle
              cx={sunX}
              cy={sunY}
              r="6"
              fill="rgba(251, 191, 36, 0.2)"
            />
            {/* Sun body */}
            <circle
              cx={sunX}
              cy={sunY}
              r="3"
              fill="#fbbf24"
              className={isFastForward ? 'drop-shadow-[0_0_8px_rgba(251,191,36,0.8)]' : ''}
            />
          </g>
        ) : (
          <g>
            {/* Moon glow */}
            <circle
              cx="50"
              cy="25"
              r="5"
              fill="rgba(203, 213, 225, 0.1)"
            />
            {/* Moon body */}
            <circle
              cx="50"
              cy="25"
              r="2.5"
              fill="#cbd5e1"
            />
          </g>
        )}
      </svg>

      {/* Time display */}
      <div className="absolute bottom-0 left-0 right-0 flex justify-between items-end px-1 text-[8px]">
        <span className="text-amber-700/50">dawn</span>
        <span className={`text-amber-200/70 ${isFastForward ? 'animate-pulse' : ''}`}>
          {timeStr} · {getPeriod()}
        </span>
        <span className="text-amber-700/50">dusk</span>
      </div>
    </div>
  );
}
