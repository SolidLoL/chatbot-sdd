interface Citation {
    id: string;
    title: string;
    url?: string;
    snippet?: string;
    relevance_score?: number;
}
interface Props {
    citation: Citation;
}
export declare function CitationCard({ citation }: Props): import("react").JSX.Element;
export {};
