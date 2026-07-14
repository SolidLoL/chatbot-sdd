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
export declare function MessageBubble({ message, isStreaming }: Props): import("react").JSX.Element;
export {};
