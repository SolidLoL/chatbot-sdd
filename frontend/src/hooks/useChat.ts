import { useMutation } from '@tanstack/react-query';
import { useState } from 'react';
import { streamChat } from '@/lib/sse-client';

interface UseChatOptions {
  sessionId?: string;
  onToken?: (token: string) => void;
  onCitation?: (citation: any) => void;
  onDone?: (data: any) => void;
  onError?: (error: Error) => void;
}

export function useChat(options: UseChatOptions = {}) {
  const [isStreaming, setIsStreaming] = useState(false);
  const [currentMessage, setCurrentMessage] = useState('');
  const [citations, setCitations] = useState<any[]>([]);

  const mutation = useMutation({
    mutationFn: async (message: string) => {
      setIsStreaming(true);
      setCurrentMessage('');
      setCitations([]);

      try {
        for await (const event of streamChat(options.sessionId, message)) {
          switch (event.type) {
            case 'token':
              setCurrentMessage((prev) => prev + event.data.content);
              options.onToken?.(event.data.content);
              break;
            case 'citation':
              setCitations((prev) => [...prev, event.data]);
              options.onCitation?.(event.data);
              break;
            case 'done':
              options.onDone?.(event.data);
              break;
            case 'error':
              throw new Error(event.data.message);
          }
        }
      } finally {
        setIsStreaming(false);
      }
    },
    onError: (error) => {
      setIsStreaming(false);
      options.onError?.(error);
    },
  });

  return {
    sendMessage: mutation.mutate,
    isStreaming,
    currentMessage,
    citations,
    error: mutation.error,
  };
}