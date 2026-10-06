// UI panel-component controls: identifiers that merely start with Panel
// (every toolkit's PanelBottom/InspectionPanel/...) are widgets, not C2
// panel destinations, so no network-destination finding may fire here.
const PanelBottomClose = createLucideIcon("panel-bottom-close", iconNode);
const InspectionPanel = createPanel("inspection-panel", iconNode);
const LayoutPanelLeft = buildPanel("layout-panel-left", iconNode);
