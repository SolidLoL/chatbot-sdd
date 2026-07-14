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

export function CitationCard({ citation }: Props) {
  return (
    <div className="bg-gray-50 rounded p-2 text-sm">
      {citation.url ? (
        <a
          href={citation.url}
          target="_blank"
          rel="noopener noreferrer"
          className="font-medium text-primary-600 hover:underline"
        >
          {citation.title}
        </a>
      ) : (
        <span className="font-medium text-gray-900">{citation.title}</span>
      )}
      {citation.snippet && (
        <p className="text-gray-600 mt-1 line-clamp-2">{citation.snippet}</p>
      )}
      {citation.relevance_score && (
        <div className="mt-1 flex items-center gap-1">
          <div className="h-1 flex-1 bg-gray-200 rounded">
            <div
              className="h-full bg-green-500 rounded"
              style={{ width: `${citation.relevance_score * 100}%` }}
            />
          </div>
          <span className="text-xs text-gray-500">
            {(citation.relevance_score * 100).toFixed(0)}%
          </span>
        </div>
      )}
    </div>
  );
}