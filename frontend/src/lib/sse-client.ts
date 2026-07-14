import { apiClient } from './api-client';

export interface SSEEvent {
  type: 'token' | 'citation' | 'thinking' | 'done' | 'error';
  data: any;
}

export async function* streamChat(
  sessionId: string | undefined,
  message: string
): AsyncGenerator<SSEEvent, void, unknown> {
  const response = await apiClient.post(
    '/v1/chat',
    {
      session_id: sessionId,
      message,
      stream: true,
    },
    {
      responseType: 'text',
      headers: {
        Accept: 'text/event-stream',
      },
    }
  );

  const reader = response.data.getReader();
  const decoder = new TextDecoder();
  let buffer = '';

  while (true) {
    const { done, value } = await reader.read();
    if (done) break;

    buffer += decoder.decode(value, { stream: true });

    const lines = buffer.split('\n');
    buffer = lines.pop() || '';

    for (const line of lines) {
      if (line.startsWith('event: ')) {
        const type = line.slice(7).trim() as SSEEvent['type'];
        const dataLine = lines.shift();
        if (dataLine?.startsWith('data: ')) {
          const data = JSON.parse(dataLine.slice(6));
          yield { type, data };
        }
      }
    }
  }
}