import os
import webbrowser
import shutil
import json
import requests
import re
import wx
import time
import tempfile
from threading import Thread
from .result_event import *
from .config import *


class PushThread(Thread):
    def __init__(self, wxObject):
        Thread.__init__(self)
        self.wxObject = wxObject
        self.start()

    def run(self):
        temp_dir = tempfile.mkdtemp()
        _, temp_file = tempfile.mkstemp()
        board = pcbnew.GetBoard()
        title_block = board.GetTitleBlock()
        self.log(f'Pushing %s...' % title_block.GetTitle())
        match = re.match(
            '^AISLER Project ID: ([A-Z]{8})$',
            title_block.GetComment(commentLineIdx))
        if match:
            project_id = match.group(1)
            self.log("Found existing Project ID %s" % project_id)
        else:
            project_id = False

        # Override a few design parameters as our CAM takes care of this
        settings = board.GetDesignSettings()
        settings.m_SolderMaskMargin = 0
        settings.m_SolderMaskMinWidth = 0

        pctl = pcbnew.PLOT_CONTROLLER(board)

        popt = pctl.GetPlotOptions()
        popt.SetOutputDirectory(temp_dir)
        popt.SetPlotFrameRef(False)
        popt.SetSketchPadLineWidth(pcbnew.FromMM(0.1))
        popt.SetAutoScale(False)
        popt.SetScale(1)
        popt.SetMirror(False)
        popt.SetUseGerberAttributes(True)
        popt.SetExcludeEdgeLayer(True)
        popt.SetUseGerberProtelExtensions(False)
        popt.SetUseAuxOrigin(True)
        popt.SetSubtractMaskFromSilk(False)
        popt.SetDrillMarksType(0)  # NO_DRILL_SHAPE

        self.log('Plotting Gerber files...')
        for layer_info in plotPlan:
            if board.IsLayerEnabled(layer_info[1]):
                pctl.SetLayer(layer_info[1])
                pctl.OpenPlotfile(
                    layer_info[0],
                    pcbnew.PLOT_FORMAT_GERBER,
                    layer_info[2])
                pctl.PlotLayer()

        pctl.ClosePlot()

        # Write excellon drill files
        self.log('Plotting Excellon files...')
        drlwriter = pcbnew.EXCELLON_WRITER(board)

        # mirrot, header, offset, mergeNPTH
        drlwriter.SetOptions(
            False,
            True,
            board.GetDesignSettings().GetAuxOrigin(),
            False)
        drlwriter.SetFormat(False)
        drlwriter.CreateDrillandMapFilesSet(pctl.GetPlotDirName(), True, False)

        # # Write netlist to enable Smart Tests
        self.log('Writting IPC Netlist for Smart Tests...')
        netlist_writer = pcbnew.IPC356D_WRITER(board)
        netlist_writer.Write(os.path.join(temp_dir, netlistFilename))

        # # Export component list
        self.log('Writting component list...')
        components = []
        if hasattr(board, 'GetModules'):
            footprints = list(board.GetModules())
        else:
            footprints = list(board.GetFootprints())

        for i, f in enumerate(footprints):
            try:
                footprint_name = str(f.GetFPID().GetFootprintName())
            except AttributeError:
                footprint_name = str(f.GetFPID().GetLibItemName())

            layer = {
                pcbnew.F_Cu: 'top',
                pcbnew.B_Cu: 'bottom',
            }.get(f.GetLayer())

            mount_type = {
                0: 'smt',
                1: 'tht',
                2: 'smt'
            }.get(f.GetAttributes())

            components.append({
                'pos_x': (f.GetPosition()[0] - board.GetDesignSettings().GetAuxOrigin()[0]) / 1000000.0,
                'pos_y': (f.GetPosition()[1] - board.GetDesignSettings().GetAuxOrigin()[1]) * -1.0 / 1000000.0,
                'rotation': f.GetOrientation() / 10.0,
                'side': layer,
                'designator': f.GetReference(),
                'mpn': f.GetProperty('mpn'),
                'pack': footprint_name,
                'value': f.GetValue(),
                'mount_type': mount_type
            })

        with open((os.path.join(temp_dir, componentsFilename)), 'w') as outfile:
            json.dump(components, outfile)

        # # Create ZIP file
        temp_file = shutil.make_archive(temp_file, 'zip', temp_dir)
        files = {'upload[file]': open(temp_file, 'rb')}

        self.log('Pushing data...')
        if project_id:
            data = {}
            data['upload_url'] = baseUrl + '/p/' + project_id + '/uploads.json'
        else:
            rsp = requests.get(baseUrl + '/p/new.json?ref=KiCadPush')
            data = json.loads(rsp.content)
            title_block.SetComment(
                commentLineIdx,
                'AISLER Project ID: ' +
                data['project_id'])
            board.SetTitleBlock(title_block)
            self.log(f'Received new Project ID')

        rsp = requests.post(
            data['upload_url'], files=files, data={
                'upload[title]': title_block.GetTitle()})
        urls = json.loads(rsp.content)
        progress = 0
        while progress < 100:
            time.sleep(pollingInterval)
            progress = json.loads(
                requests.get(
                    urls['callback']).content)['progress']
            self.log("Progress %i / 100" % progress)

        self.log("Redirected to %s, have fun!" % urls['redirect'])
        webbrowser.open(urls['redirect'])

        time.sleep(3)
        self.log(-1)

    def log(self, msg):
        wx.PostEvent(self.wxObject, ResultEvent(msg))
