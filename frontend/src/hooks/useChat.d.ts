interface UseChatOptions {
    sessionId?: string;
    onToken?: (token: string) => void;
    onCitation?: (citation: any) => void;
    onDone?: (data: any) => void;
    onError?: (error: Error) => void;
}
export declare function useChat(options?: UseChatOptions): {
    sendMessage: import("@tanstack/react-query").UseMutateFunction<void, Error, string, unknown>;
    isStreaming: boolean;
    currentMessage: string;
    citations: any[];
    error: Error | null;
};
export {};
