import wx
from wxasync import AsyncBind, WxAsyncApp, StartCoroutine
import asyncio


from .config import connectToGateway
from .devices import get_devices


class MainWindow(wx.Frame):
    def __init__(self):

        super().__init__(parent=None, title='Hello World')
        loop = asyncio.get_event_loop()
        loop.create_task(self.setup_controls())

    async def setup_controls(self):

        self._api, self._gateway, self._api_factory = await connectToGateway()

        sizer = wx.BoxSizer(wx.VERTICAL)

        lights, outlets, groups, _ = await get_devices(self._api,
                                                       self._gateway)

        for aLight in lights:
            my_btn = wx.Button(self, label=aLight.device_name)
            AsyncBind(wx.EVT_BUTTON, self.doExit, my_btn)
            sizer.Add(my_btn, 0, wx.ALIGN_RIGHT)

        # sizer.SetSizeHints(self)
        self.SetSizer(sizer)
        self.Show()

    async def doExit(self, event):
        exit()

    async def button_click(self, event):
        print("Click!")
