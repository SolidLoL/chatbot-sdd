import { useState } from 'react';
import { useChat } from '@/hooks/useChat';
import { MessageBubble } from './MessageBubble';
import { MessageInput } from './MessageInput';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  citations?: any[];
}

export function ChatWindow() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [sessionId, setSessionId] = useState<string | undefined>();

  const { sendMessage, isStreaming, currentMessage, citations } = useChat({
    sessionId,
    onDone: (data: { message_id: string; session_id?: string }) => {
      if (!sessionId && data.session_id) {
        setSessionId(data.session_id);
      }
      setMessages((prev) => [
        ...prev,
        {
          id: data.message_id,
          role: 'assistant',
          content: currentMessage,
          citations,
        },
      ]);
    },
  });

  const handleSend = (message: string) => {
    setMessages((prev) => [
      ...prev,
      {
        id: `temp-${Date.now()}`,
        role: 'user',
        content: message,
      },
    ]);
    sendMessage(message);
  };

  return (
    <div className="flex flex-col h-screen bg-gray-50">
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((msg) => (
          <MessageBubble key={msg.id} message={msg} />
        ))}
        {isStreaming && (
          <MessageBubble
            message={{
              id: 'streaming',
              role: 'assistant',
              content: currentMessage,
              citations,
            }}
            isStreaming
          />
        )}
      </div>
      <div className="border-t bg-white p-4">
        <MessageInput onSend={handleSend} disabled={isStreaming} />
      </div>
    </div>
  );
}