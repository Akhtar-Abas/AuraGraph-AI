import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

# Sahi imports
from .models import ResearchReport
from engine.graph import app 

class ResearchConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, close_code):
        pass

    async def receive(self, text_data):
        try:
            data = json.loads(text_data)
        except Exception:
            return

        task_query = data.get('task')
        
        # 1. Database entry
        report_obj = await sync_to_async(ResearchReport.objects.create)(
            task=task_query, 
            status='processing'
        )

        inputs = {"task": task_query}
        final_report = "" 

        try:
            # 2. Run the graph ONLY ONCE using astream
            async for event in app.astream(inputs):
                for node_name, output in event.items():
                    # Status update extraction
                    status_msg = output.get("status", f"{node_name.capitalize()} in progress...")
                    
                    # Capture report if writer finished
                    if "report" in output:
                        final_report = output["report"]

                    # Live notification send karein
                    await self.send(text_data=json.dumps({
                        'type': 'status_update',
                        'status': status_msg,
                        'node': node_name
                    }))

            # 3. Final cleanup and database save
            if not final_report:
                final_state = await sync_to_async(app.invoke)(inputs)
                final_report = final_state.get("report", "No report content generated.")

            report_obj.report = final_report
            report_obj.status = 'completed'
            await sync_to_async(report_obj.save)()

            # 4. Final signal to frontend
            await self.send(text_data=json.dumps({
                'type': 'final_report',
                'status': 'completed',
                'report': final_report
            }))

        except Exception as e:
            print(f"Graph Error: {e}")
            await self.send(text_data=json.dumps({
                'type': 'error', 
                'message': str(e)
            }))