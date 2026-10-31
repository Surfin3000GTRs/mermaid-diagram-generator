# Mermaid Diagram Families

Selection guide for choosing a Mermaid diagram family. Use this as a selection guide, not as a promise that every Mermaid renderer supports every feature. Mermaid's official documentation and implementation evolve; confirm the target renderer's Mermaid version for version-sensitive syntax.

For flowchart node shapes, see the [flowchart shape catalog](./flowchart-shapes.md).

## Diagram families

Choose a family based on the information being communicated. The official links below lead to Mermaid syntax documentation. An unverified minimum version is marked "Check target renderer"; it does not mean the diagram type is new. Beta syntax may change.

### Process, structure, and interaction

| Diagram | Choose it for | Official syntax | Min version / Status |
| --- | --- | --- | --- |
| Flowchart | Steps, branches, dependencies, and general system relationships | [Flowchart](https://mermaid.js.org/syntax/flowchart.html) | Check target renderer |
| Sequence diagram | Ordered messages between actors, components, or services | [Sequence](https://mermaid.js.org/syntax/sequenceDiagram.html) | Check target renderer |
| State diagram | States, transitions, and lifecycle behavior | [State](https://mermaid.js.org/syntax/stateDiagram.html) | Check target renderer |
| Class diagram | Classes, members, inheritance, and object relationships | [Class](https://mermaid.js.org/syntax/classDiagram.html) | Check target renderer |
| Entity relationship diagram | Entities, attributes, and data cardinalities | [ER](https://mermaid.js.org/syntax/entityRelationshipDiagram.html) | Check target renderer |
| Use case diagram | Actors and their goals/interactions with a system | [Use case](https://mermaid.js.org/syntax/usecase.html) | v12.0.0+ (beta) |
| C4 diagram | System context, containers, components, and deployments | [C4](https://mermaid.js.org/syntax/c4.html) | Check target renderer |
| Architecture diagram | Services, groups, and relationships in an architecture | [Architecture](https://mermaid.js.org/syntax/architecture.html) | Check target renderer |
| Block diagram | Blocks, ports, and directional connections | [Block](https://mermaid.js.org/syntax/block.html) | Check target renderer |
| Packet diagram | Bit fields and packet/header layouts | [Packet](https://mermaid.js.org/syntax/packet.html) | Check target renderer |
| Swimlanes | Activities organized across participants or responsibility lanes | [Swimlanes](https://mermaid.js.org/syntax/swimlanes.html) | Check target renderer |
| Event modeling | Events, commands, and read models in an event-driven domain | [Event modeling](https://mermaid.js.org/syntax/eventmodeling.html) | v11.15.0+ |
| Agent flow | Agent-oriented workflow and handoff representations | [Agent flow](https://mermaid.js.org/syntax/agentflow.html) | v12.0.0+ (beta) |

### Planning, chronology, and concepts

| Diagram | Choose it for | Official syntax | Min version / Status |
| --- | --- | --- | --- |
| Gantt | Tasks, durations, dependencies, and project schedules | [Gantt](https://mermaid.js.org/syntax/gantt.html) | Check target renderer |
| Kanban | Work items organized into columns and cards | [Kanban](https://mermaid.js.org/syntax/kanban.html) | Check target renderer |
| User journey | Stages and user experience across a journey | [User journey](https://mermaid.js.org/syntax/userJourney.html) | Check target renderer |
| Timeline | Events ordered chronologically | [Timeline](https://mermaid.js.org/syntax/timeline.html) | Check target renderer |
| Mindmap | Hierarchical ideas and associations | [Mindmap](https://mermaid.js.org/syntax/mindmap.html) | Check target renderer |
| Tree view | Hierarchical tree structures | [Tree view](https://mermaid.js.org/syntax/treeView.html) | v11.14.0+ (beta) |
| Git graph | Commits, branches, merges, and tags | [Git graph](https://mermaid.js.org/syntax/gitgraph.html) | Check target renderer |
| Requirement diagram | Requirements and their traceable relationships | [Requirements](https://mermaid.js.org/syntax/requirementDiagram.html) | Check target renderer |
| Wardley map | Value-chain components mapped by evolution and visibility | [Wardley](https://mermaid.js.org/syntax/wardley.html) | Check target renderer |
| Cynefin diagram | Domains and decision-making context | [Cynefin](https://mermaid.js.org/syntax/cynefin.html) | Check target renderer |
| Ishikawa diagram | Cause-and-effect analysis | [Ishikawa](https://mermaid.js.org/syntax/ishikawa.html) | Check target renderer |
| Railroad diagram | Grammar and syntax rules | [Railroad](https://mermaid.js.org/syntax/railroad.html) | Check target renderer |
| ZenUML | Sequence-style interactions using concise ZenUML syntax | [ZenUML](https://mermaid.js.org/syntax/zenuml.html) | Check target renderer |

### Charts and set relationships

| Diagram | Choose it for | Official syntax | Min version / Status |
| --- | --- | --- | --- |
| Pie chart | Parts of a whole | [Pie](https://mermaid.js.org/syntax/pie.html) | Check target renderer |
| Quadrant chart | Positioning items across two axes and four quadrants | [Quadrant](https://mermaid.js.org/syntax/quadrantChart.html) | Check target renderer |
| XY chart | Numeric series plotted against X/Y axes | [XY chart](https://mermaid.js.org/syntax/xyChart.html) | Check target renderer |
| Sankey diagram | Weighted flows between categories | [Sankey](https://mermaid.js.org/syntax/sankey.html) | Check target renderer |
| Radar chart | Comparing multiple dimensions across subjects | [Radar](https://mermaid.js.org/syntax/radar.html) | Check target renderer |
| Treemap | Hierarchical proportions and nested categories | [Treemap](https://mermaid.js.org/syntax/treemap.html) | Check target renderer |
| Venn diagram | Overlap and inclusion between sets | [Venn](https://mermaid.js.org/syntax/venn.html) | v11.12.3+ (beta) |
