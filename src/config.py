import pcbnew

# baseUrl = 'http://localhost:3000'
baseUrl = 'https://aisler.net'
commentLineIdx = 3
pollingInterval = 0.5
netlistFilename = 'netlist.ipc'
componentsFilename = 'components.json'
odbFilename = 'odb'
magicFilename = '.kicad-push'
plotPlan = [
    ("F_Cu", pcbnew.F_Cu, "Top Layer"),
    ("B_Cu", pcbnew.B_Cu, "Bottom Layer"),
    ("In1_Cu", pcbnew.In1_Cu, "Internal plane 1"),
    ("In2_Cu", pcbnew.In2_Cu, "Internal plane 2"),
    ("In3_Cu", pcbnew.In3_Cu, "Internal plane 3"),
    ("In4_Cu", pcbnew.In4_Cu, "Internal plane 4"),
    ("In5_Cu", pcbnew.In5_Cu, "Internal layer 5"),
    ("In6_Cu", pcbnew.In6_Cu, "Internal layer 6"),
    ("In7_Cu", pcbnew.In7_Cu, "Internal layer 7"),
    ("In8_Cu", pcbnew.In8_Cu, "Internal layer 8"),
    ("In9_Cu", pcbnew.In9_Cu, "Internal layer 9"),
    ("In10_Cu", pcbnew.In10_Cu, "Internal layer 10"),
    ("F_SilkS", pcbnew.F_SilkS, "Top Silkscreen"),
    ("B_SilkS", pcbnew.B_SilkS, "Bottom Silkscreen"),
    ("F_Mask", pcbnew.F_Mask, "Top Soldermask"),
    ("B_Mask", pcbnew.B_Mask, "Bottom Soldermask"),
    ("F_Paste", pcbnew.F_Paste, "Top Paste (Stencil)"),
    ("B_Paste", pcbnew.B_Paste, "Bottom Paste (Stencil)"),
    ("Edge_Cuts", pcbnew.Edge_Cuts, "Board Outline")
]
