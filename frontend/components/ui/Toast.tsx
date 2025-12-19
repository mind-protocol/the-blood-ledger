'use client';

// DOCS: docs/frontend/PATTERNS_Presentation_Layer.md

import { createContext, useContext, useState, useCallback, useEffect } from 'react';

interface Toast {
  id: string;
  message: string;
  type: 'error' | 'warning' | 'info';
  duration?: number;
}

interface ToastContextType {
  showToast: (message: string, type?: Toast['type'], duration?: number) => void;
}

const ToastContext = createContext<ToastContextType | null>(null);

// Global toast function for use outside React components
let globalShowToast: ((message: string, type?: Toast['type'], duration?: number) => void) | null = null;

export function showToast(message: string, type: Toast['type'] = 'error', duration = 5000) {
  if (globalShowToast) {
    globalShowToast(message, type, duration);
  } else {
    console.error('[Toast] Provider not mounted:', message);
  }
}

export function useToast() {
  const context = useContext(ToastContext);
  if (!context) {
    throw new Error('useToast must be used within a ToastProvider');
  }
  return context;
}

export function ToastProvider({ children }: { children: React.ReactNode }) {
  const [toasts, setToasts] = useState<Toast[]>([]);

  const showToastFn = useCallback((message: string, type: Toast['type'] = 'error', duration = 5000) => {
    const id = Math.random().toString(36).slice(2);
    setToasts(prev => [...prev, { id, message, type, duration }]);
  }, []);

  const removeToast = useCallback((id: string) => {
    setToasts(prev => prev.filter(t => t.id !== id));
  }, []);

  // Set global toast function
  useEffect(() => {
    globalShowToast = showToastFn;
    return () => {
      globalShowToast = null;
    };
  }, [showToastFn]);

  return (
    <ToastContext.Provider value={{ showToast: showToastFn }}>
      {children}
      {/* Toast container - bottom right */}
      <div className="fixed bottom-4 right-4 z-50 flex flex-col gap-2">
        {toasts.map(toast => (
          <ToastItem
            key={toast.id}
            toast={toast}
            onDismiss={() => removeToast(toast.id)}
          />
        ))}
      </div>
    </ToastContext.Provider>
  );
}

function ToastItem({ toast, onDismiss }: { toast: Toast; onDismiss: () => void }) {
  useEffect(() => {
    if (toast.duration) {
      const timer = setTimeout(onDismiss, toast.duration);
      return () => clearTimeout(timer);
    }
  }, [toast.duration, onDismiss]);

  return (
    <div
      className={`
        px-4 py-3 rounded-lg shadow-lg max-w-sm animate-slideIn
        bg-amber-950/95 border border-amber-900/50 text-amber-100
      `}
    >
      <div className="flex items-start gap-3">
        <span className="text-amber-500 mt-0.5">
          {toast.type === 'error' ? '!' : toast.type === 'warning' ? '!' : 'i'}
        </span>
        <p className="text-sm flex-1">{toast.message}</p>
        <button
          onClick={onDismiss}
          className="text-amber-500/70 hover:text-amber-300 transition-colors"
        >
          x
        </button>
      </div>
    </div>
  );
}
