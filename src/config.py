import pcbnew

# baseUrl = 'http://localhost:3000'
baseUrl = 'https://aisler.net'
commentLineIdx = 3
pollingInterval = 0.5
netlistFilename = 'netlist.ipc'
componentsFilename = 'components.json'
plotPlan = [
    ("F.Cu", pcbnew.F_Cu, "Top Layer"),
    ("B.Cu", pcbnew.B_Cu, "Bottom Layer"),
    ("In1.Cu", pcbnew.In1_Cu, "Internal plane 1"),
    ("In2.Cu", pcbnew.In2_Cu, "Internal plane 2"),
    ("In3.Cu", pcbnew.In3_Cu, "Internal plane 3"),
    ("In4.Cu", pcbnew.In4_Cu, "Internal plane 4"),
    ("In5.Cu", pcbnew.In5_Cu, "Internal layer 5"),
    ("In6.Cu", pcbnew.In6_Cu, "Internal layer 6"),
    ("In7.Cu", pcbnew.In7_Cu, "Internal layer 7"),
    ("In8.Cu", pcbnew.In8_Cu, "Internal layer 8"),
    ("In9.Cu", pcbnew.In9_Cu, "Internal layer 9"),
    ("In10.Cu", pcbnew.In10_Cu, "Internal layer 10"),
    ("F.SilkS", pcbnew.F_SilkS, "Top Silkscreen"),
    ("B.SilkS", pcbnew.B_SilkS, "Bottom Silkscreen"),
    ("F.Mask", pcbnew.F_Mask, "Top Soldermask"),
    ("B.Mask", pcbnew.B_Mask, "Bottom Soldermask"),
    ("F.Paste", pcbnew.F_Paste, "Top Paste (Stencil)"),
    ("B.Paste", pcbnew.B_Paste, "Bottom Paste (Stencil)"),
    ("Edge.Cuts", pcbnew.Edge_Cuts, "Board Outline")
]
