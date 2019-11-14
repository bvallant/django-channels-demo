import asyncio
from datetime import datetime
from channels.generic.websocket import AsyncJsonWebsocketConsumer



class StatusConsumer(AsyncJsonWebsocketConsumer):

    @property
    def _groups(self):
        return ["user-%s" % self.scope['user'].pk]

    async def ping(self):
        await self.send_json({"type": "ping"})

    async def connect(self):
        user = self.scope["user"]

        if not user.is_authenticated:
            await self.send_json({"message": "Not authenticated" })
            await self.close()
            return

        await self.accept()


        for group in self._groups:
            await self.channel_layer.group_add(group, self.channel_name)
            await self.send_json({"message": "Channel %s joined Group %s" % (self.channel_name, group)})

        self.heartbeat = asyncio.ensure_future(self.start_heartbeat())

    async def start_heartbeat(self):
        print("Starting Heartbeat...")
        while True:
            await self.ping()
            await asyncio.sleep(2)

    async def stop_heartbeat(self):
        print("Stopping Heartbeat...")
        self.heartbeat.cancel()


    async def notification(self, message):
        payload = message.get('payload', {})
        print("Sending Notification '%s'." % payload.get("message"))
        await self.send_json(payload)

    async def disconnect(self, close_code):
        print("Disconnecting...")
        await self.stop_heartbeat()
        for group in self._groups:
            await self.channel_layer.group_discard(group, self.channel_name)
            await self.send_json({"message": "Left %s" % group})
        await self.close()
        print("Disconnected.")


    async def receive_json(self, data):
        print("Received message...", data.get('type'))
        self.last_seen = datetime.now()
