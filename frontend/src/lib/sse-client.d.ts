export interface SSEEvent {
    type: 'token' | 'citation' | 'thinking' | 'done' | 'error';
    data: any;
}
export declare function streamChat(sessionId: string | undefined, message: string): AsyncGenerator<SSEEvent, void, unknown>;
