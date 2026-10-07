# Lucid Process Flow Standards

Applies to SDD 4.1, SOW/CO Process Overview, and standalone flow requests. Not for one-pagers.

## Structure
| Rule | Standard |
|---|---|
| Lanes | Horizontal swim lanes, 2 to 4. Default 2 (End User / NetSuite Automation). Add a lane only for a distinct actor or system (e.g., Celigo Integration). |
| Lane type | True `AdvancedSwimLaneBlock` containers. Never plain rectangles standing in for lanes. |
| Lane order | Strict causal adjacency: no connector skips a non-adjacent lane. Reorder or merge lanes if the process bounces. |
| Lane naming | Actor or system only. No verbs. |
| Lane shading | Title bar Lunar #DFE3E8; body stays white (that's how FillColor behaves on a real swimlane block). |
| Lane sizing | Fit the flow, not the page. 40pt margin to first and last box. |
| Box spacing | 60pt between boxes, horizontally and between rows. |
| Direction | Left to right. Vertical only to cross lanes. |
| Terminator | Exactly ONE, labeled "End Process". Every branch, including early exits, routes into it. |

## Shapes
| Shape | Use | Size | Style |
|---|---|---|---|
| Process | Standard step | 160x120pt | White fill, #3A414A border |
| Predefined Process | Documented sub-process (e.g., native NetSuite flow) | 160x120pt | Same |
| Decision | Branch | 160x120pt | Same |
| Terminator | Start / End Process | 160x80pt | Same |

## Text and connectors
- Lane label 10pt Inter or Calibri. Shape label 8pt (7pt only if it won't fit).
- Labels live in the shape's own text field. Never floating text boxes.
- Elbow connectors, 12pt rounding, never diagonal. Arrowhead at target only. Color #3A414A.
- Decision branches labeled Yes/No (bold 8pt #333333) attached to the connector itself.

## Mandatory verification before export
Re-fetch the created doc and confirm: real `AdvancedSwimLaneBlock` containers (check with shape details filtered to that class), embedded labels, correct box sizes, single terminator with no dead-end branches, no non-adjacent lane skips, elbow connectors only. Fix and re-verify before exporting.

## Filing
- Shared "Process Flows" folder, subfolder per client.
- Doc title: `[Client] - [Feature] Process Flow`. Page title = scenario ("Current State", "New Solution"); separate pages for current vs proposed.
- Export PNG, embed at the document placeholder, record the Lucid edit link (SDD: Document Control).
