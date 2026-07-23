# Navigation Header

## User Stories

**US-01** — Como usuario, quiero ver una barra superior con el nombre de la app para saber dónde estoy.

**US-04** — Como usuario, quiero un menú desplegable en el header con opción "Cerrar sesión" (logout).

## Acceptance Criteria

| ID | Criterio | Estado |
|---|---|---|
| AC-01 | Header visible en `/` con logo "Chatbot SDD" | ✅ |
| AC-05 | Menú hamburguesa (≡) en el header con "Cerrar sesión" | ✅ |
| AC-06 | El menú se cierra al hacer clic fuera (click outside) | ✅ |
| AC-07 | Header responsivo en mobile y desktop | ✅ |

## Architectural Changes

### New Components

| File | Purpose |
|---|---|
| `frontend/src/components/layout/Header.tsx` | Barra superior con logo + menú |
| `frontend/src/components/layout/HeaderMenu.tsx` | Dropdown menú desplegable |

### Modified Components

| File | Change |
|---|---|
| `frontend/src/components/chat/ChatWindow.tsx` | Agregar `<Header>` |

### Removed Components

| File | Reason |
|---|---|
| `frontend/src/components/layout/ConfirmDialog.tsx` | No se necesita sin End Session / New Session |

### Data Flow: Logout

```
User clicks ≡ → "Cerrar sesión" → clearToken() → navigate /login
```
