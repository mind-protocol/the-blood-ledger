'use client';

// DOCS: docs/frontend/IMPLEMENTATION_Frontend_Code_Architecture.md

import { useEffect, useState, useRef } from 'react';

interface MutationEvent {
  type: string;
  timestamp: string;
  data: Record<string, unknown>;
}

interface QueryResult {
  id: string;
  name: string;
  type: string;
  content?: string;
  description?: string;
  wound?: string;
  why_here?: string;
  mood?: string;
  tone?: string;
  similarity: number;
}

interface DebugPanelProps {
  apiUrl?: string;
  collapsed?: boolean;
  playthroughId?: string;
}

export function DebugPanel({ apiUrl = 'http://localhost:8000', collapsed: initialCollapsed = true, playthroughId = 'nlr-1' }: DebugPanelProps) {
  const [events, setEvents] = useState<MutationEvent[]>([]);
  const [connected, setConnected] = useState(false);
  const [collapsed, setCollapsed] = useState(initialCollapsed);
  const [activeTab, setActiveTab] = useState<'mutations' | 'query'>('mutations');
  const [queryInput, setQueryInput] = useState('');
  const [queryResults, setQueryResults] = useState<QueryResult[]>([]);
  const [queryLoading, setQueryLoading] = useState(false);
  const [queryError, setQueryError] = useState<string | null>(null);
  const eventsEndRef = useRef<HTMLDivElement>(null);
  const eventSourceRef = useRef<EventSource | null>(null);

  useEffect(() => {
    // Connect to debug SSE stream
    const connectSSE = () => {
      try {
        const es = new EventSource(`${apiUrl}/api/debug/stream`);
        eventSourceRef.current = es;

        es.addEventListener('connected', () => {
          setConnected(true);
          addEvent({ type: 'connected', timestamp: new Date().toISOString(), data: {} });
        });

        es.addEventListener('apply_start', (e) => {
          const event = JSON.parse(e.data);
          addEvent(event);
        });

        es.addEventListener('node_created', (e) => {
          const event = JSON.parse(e.data);
          addEvent(event);
        });

        es.addEventListener('node_error', (e) => {
          const event = JSON.parse(e.data);
          addEvent(event);
        });

        es.addEventListener('link_created', (e) => {
          const event = JSON.parse(e.data);
          addEvent(event);
        });

        es.addEventListener('link_error', (e) => {
          const event = JSON.parse(e.data);
          addEvent(event);
        });

        es.addEventListener('movement', (e) => {
          const event = JSON.parse(e.data);
          addEvent(event);
        });

        es.addEventListener('apply_complete', (e) => {
          const event = JSON.parse(e.data);
          addEvent(event);
        });

        es.addEventListener('ping', () => {
          // Keepalive, ignore
        });

        es.onerror = () => {
          setConnected(false);
          es.close();
          // Reconnect after 3 seconds
          setTimeout(connectSSE, 3000);
        };
      } catch (err) {
        console.error('Failed to connect to debug stream:', err);
        setTimeout(connectSSE, 3000);
      }
    };

    connectSSE();

    return () => {
      if (eventSourceRef.current) {
        eventSourceRef.current.close();
      }
    };
  }, [apiUrl]);

  // Auto-scroll to bottom when new events arrive
  useEffect(() => {
    if (eventsEndRef.current && !collapsed) {
      eventsEndRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [events, collapsed]);

  const addEvent = (event: MutationEvent) => {
    setEvents(prev => [...prev.slice(-99), event]); // Keep last 100 events
  };

  const clearEvents = () => {
    setEvents([]);
  };

  const getEventColor = (type: string) => {
    switch (type) {
      case 'connected': return 'text-green-400';
      case 'apply_start': return 'text-blue-400';
      case 'node_created': return 'text-emerald-400';
      case 'link_created': return 'text-cyan-400';
      case 'movement': return 'text-amber-400';
      case 'apply_complete': return 'text-purple-400';
      case 'node_error':
      case 'link_error': return 'text-red-400';
      default: return 'text-stone-400';
    }
  };

  const handleQuery = async () => {
    if (!queryInput.trim()) return;

    setQueryLoading(true);
    setQueryError(null);

    try {
      const response = await fetch(`${apiUrl}/api/${playthroughId}/query`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ query: queryInput }),
      });

      if (!response.ok) {
        const errorText = await response.text();
        throw new Error(`Query failed: ${response.status} - ${errorText}`);
      }

      const data = await response.json();
      setQueryResults(data.results || []);
    } catch (err) {
      setQueryError(err instanceof Error ? err.message : 'Query failed');
      setQueryResults([]);
    } finally {
      setQueryLoading(false);
    }
  };

  const getTypeColor = (type: string) => {
    switch (type) {
      case 'character': return 'text-amber-400';
      case 'place': return 'text-emerald-400';
      case 'thing': return 'text-cyan-400';
      case 'narrative': return 'text-purple-400';
      default: return 'text-stone-400';
    }
  };

  const formatEventSummary = (event: MutationEvent) => {
    const data = event.data;
    switch (event.type) {
      case 'connected':
        return 'Connected to debug stream';
      case 'apply_start':
        return `Applying: ${data.node_count || 0} nodes, ${data.link_count || 0} links`;
      case 'node_created':
        return `+ ${data.type}: ${data.name || data.id}`;
      case 'link_created':
        return `+ ${data.type}: ${data._link_id || ''}`;
      case 'movement':
        return `Move: ${data.character} -> ${data.to}`;
      case 'apply_complete':
        return `Done: ${data.persisted_count} ok, ${data.error_count || 0} errors`;
      case 'node_error':
      case 'link_error':
        return `Error: ${data.error}`;
      default:
        return event.type;
    }
  };

  if (collapsed) {
    return (
      <button
        onClick={() => setCollapsed(false)}
        className="fixed bottom-4 left-4 z-50 px-3 py-1.5 bg-stone-900/90 border border-stone-700 rounded text-xs font-mono text-stone-400 hover:text-stone-200 hover:border-stone-600 transition-colors flex items-center gap-2"
      >
        <span className={`w-2 h-2 rounded-full ${connected ? 'bg-green-500' : 'bg-red-500'}`} />
        Debug {events.length > 0 && `(${events.length})`}
      </button>
    );
  }

  return (
    <div className="fixed bottom-4 left-4 z-50 w-96 max-h-[32rem] bg-stone-900/95 border border-stone-700 rounded-lg shadow-xl font-mono text-xs overflow-hidden flex flex-col">
      {/* Header */}
      <div className="flex items-center justify-between px-3 py-2 border-b border-stone-700 bg-stone-800/50">
        <div className="flex items-center gap-2">
          <span className={`w-2 h-2 rounded-full ${connected ? 'bg-green-500' : 'bg-red-500'}`} />
          <span className="text-stone-300 font-medium">Debug</span>
        </div>
        <div className="flex items-center gap-2">
          {activeTab === 'mutations' && (
            <button
              onClick={clearEvents}
              className="text-stone-500 hover:text-stone-300 transition-colors"
              title="Clear"
            >
              Clear
            </button>
          )}
          <button
            onClick={() => setCollapsed(true)}
            className="text-stone-500 hover:text-stone-300 transition-colors"
            title="Collapse"
          >
            _
          </button>
        </div>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-stone-700">
        <button
          onClick={() => setActiveTab('mutations')}
          className={`flex-1 px-3 py-1.5 text-center transition-colors ${
            activeTab === 'mutations'
              ? 'text-stone-200 bg-stone-800/50 border-b-2 border-amber-500'
              : 'text-stone-500 hover:text-stone-300'
          }`}
        >
          Mutations {events.length > 0 && `(${events.length})`}
        </button>
        <button
          onClick={() => setActiveTab('query')}
          className={`flex-1 px-3 py-1.5 text-center transition-colors ${
            activeTab === 'query'
              ? 'text-stone-200 bg-stone-800/50 border-b-2 border-amber-500'
              : 'text-stone-500 hover:text-stone-300'
          }`}
        >
          Query
        </button>
      </div>

      {/* Content */}
      {activeTab === 'mutations' ? (
        <>
          {/* Events list */}
          <div className="flex-1 overflow-y-auto p-2 space-y-1">
            {events.length === 0 ? (
              <div className="text-stone-600 text-center py-4">
                Waiting for mutations...
              </div>
            ) : (
              events.map((event, i) => (
                <div
                  key={i}
                  className="flex items-start gap-2 py-0.5 hover:bg-stone-800/50 px-1 rounded"
                >
                  <span className="text-stone-600 w-12 flex-shrink-0">
                    {new Date(event.timestamp).toLocaleTimeString('en-US', {
                      hour12: false,
                      hour: '2-digit',
                      minute: '2-digit',
                      second: '2-digit'
                    })}
                  </span>
                  <span className={`${getEventColor(event.type)} flex-1 break-all`}>
                    {formatEventSummary(event)}
                  </span>
                </div>
              ))
            )}
            <div ref={eventsEndRef} />
          </div>

          {/* Footer */}
          <div className="px-3 py-1.5 border-t border-stone-700 bg-stone-800/50 text-stone-600">
            {events.length} events
          </div>
        </>
      ) : (
        <>
          {/* Query input */}
          <div className="p-2 border-b border-stone-700">
            <div className="flex gap-2">
              <input
                type="text"
                value={queryInput}
                onChange={(e) => setQueryInput(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && handleQuery()}
                placeholder="Natural language query..."
                className="flex-1 px-2 py-1.5 bg-stone-800 border border-stone-600 rounded text-stone-200 placeholder-stone-500 focus:outline-none focus:border-amber-500"
              />
              <button
                onClick={handleQuery}
                disabled={queryLoading || !queryInput.trim()}
                className="px-3 py-1.5 bg-amber-600 hover:bg-amber-500 disabled:bg-stone-700 disabled:text-stone-500 text-white rounded transition-colors"
              >
                {queryLoading ? '...' : 'Ask'}
              </button>
            </div>
          </div>

          {/* Query results */}
          <div className="flex-1 overflow-y-auto p-2 space-y-2">
            {queryError && (
              <div className="text-red-400 p-2 bg-red-900/20 rounded">
                {queryError}
              </div>
            )}
            {queryResults.length === 0 && !queryError && !queryLoading && (
              <div className="text-stone-600 text-center py-4">
                Ask a question about the world...
              </div>
            )}
            {queryResults.map((result, i) => {
              // Build display text from available fields
              const displayText = result.content
                || result.description
                || result.wound
                || result.why_here
                || null;

              return (
                <div
                  key={result.id || i}
                  className="p-2 bg-stone-800/50 rounded border border-stone-700 hover:border-stone-600"
                >
                  <div className="flex items-center justify-between mb-1">
                    <span className="text-stone-200 font-medium">{result.name}</span>
                    <span className={`${getTypeColor(result.type)} text-[10px] uppercase`}>
                      {result.type}
                    </span>
                  </div>
                  <div className="text-stone-500 text-[10px] mb-1">
                    {result.id} · {(result.similarity * 100).toFixed(0)}% match
                    {result.tone && <span className="ml-2 text-stone-600">({result.tone})</span>}
                    {result.mood && <span className="ml-2 text-stone-600">mood: {result.mood}</span>}
                  </div>
                  {displayText && (
                    <div className="text-stone-400 text-[11px] line-clamp-3">
                      {displayText}
                    </div>
                  )}
                </div>
              );
            })}
          </div>

          {/* Footer */}
          <div className="px-3 py-1.5 border-t border-stone-700 bg-stone-800/50 text-stone-600">
            {queryResults.length} results
          </div>
        </>
      )}
    </div>
  );
}
