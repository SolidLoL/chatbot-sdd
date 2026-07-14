import ReactMarkdown from 'react-markdown';
import { CitationCard } from './CitationCard';

interface Message {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  citations?: any[];
}

interface Props {
  message: Message;
  isStreaming?: boolean;
}

export function MessageBubble({ message, isStreaming }: Props) {
  const isUser = message.role === 'user';

  return (
    <div className={`flex ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div
        className={`max-w-2xl rounded-lg p-4 ${
          isUser
            ? 'bg-primary-600 text-white'
            : 'bg-white border border-gray-200'
        }`}
      >
        <div className="prose prose-sm max-w-none">
          <ReactMarkdown>{message.content}</ReactMarkdown>
          {isStreaming && (
            <span className="inline-block w-2 h-4 bg-gray-400 animate-pulse ml-1" />
          )}
        </div>
        {message.citations && message.citations.length > 0 && (
          <div className="mt-3 pt-3 border-t border-gray-200">
            <p className="text-xs font-semibold text-gray-600 mb-2">
              Fuentes consultadas:
            </p>
            <div className="space-y-2">
              {message.citations.map((citation, idx) => (
                <CitationCard key={idx} citation={citation} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}