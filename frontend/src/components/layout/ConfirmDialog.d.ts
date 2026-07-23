interface Props {
    open: boolean;
    title: string;
    message: string;
    confirmLabel?: string;
    cancelLabel?: string;
    onConfirm: () => void;
    onCancel: () => void;
}
export declare function ConfirmDialog({ open, title, message, confirmLabel, cancelLabel, onConfirm, onCancel, }: Props): import("react").JSX.Element | null;
export {};
